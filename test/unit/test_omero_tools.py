"""Tests for omero_tools, focused on _label_channels."""

from unittest.mock import MagicMock

import pytest
from omero.model import LogicalChannelI
from omero.rtypes import rstring

from omero_metrics.tools.omero_tools import _label_channels


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_logical_channel(lc_id, name=None):
    """Create a real LogicalChannelI with a given id and optional name."""
    lc = LogicalChannelI()
    lc._id = lc_id
    if name is not None:
        lc.setName(rstring(name))
    return lc


def _make_channel(logical_channel, channel_id=None):
    """Return a (wrapper, lc) pair.  The wrapper mocks ChannelWrapper and
    exposes the LC for inspection. channel_id is the OMERO Channel row id."""
    wrapper = MagicMock()
    wrapper.getLogicalChannel.return_value = MagicMock(
        wraps=logical_channel,
        getId=MagicMock(return_value=logical_channel._id),
        setName=logical_channel.setName,
        getName=logical_channel.getName,
    )
    # _obj.id.val is read by _label_channels to reload the channel
    wrapper._obj = MagicMock()
    wrapper._obj.id.val = channel_id if channel_id is not None else id(wrapper)
    return wrapper, logical_channel


def _make_image(channels, conn):
    """Build a mock ImageWrapper."""
    image = MagicMock()
    image.getSizeC.return_value = len(channels)
    image.getChannels.return_value = [ch for ch, _ in channels]
    image._conn = conn
    return image


def _make_conn():
    """Build a mock BlitzGateway with update and query services.

    * saveAndReturnObject assigns auto-incrementing IDs to new LCs.
    * getQueryService().get() returns a fresh MagicMock (simulating a
      reloaded Channel) that the test can inspect via ``setLogicalChannel``.
    """
    conn = MagicMock()
    _next_id = [1000]

    def _save_and_return(obj, *args, **kwargs):
        obj._id = _next_id[0]
        _next_id[0] += 1
        return obj

    conn.getUpdateService().saveAndReturnObject.side_effect = _save_and_return

    # Each call to get() returns a distinct MagicMock (the "reloaded" channel)
    reloaded_channels = []

    def _query_get(cls_name, obj_id, *args, **kwargs):
        ch = MagicMock(name=f"reloaded_Channel_{obj_id}")
        reloaded_channels.append(ch)
        return ch

    conn.getQueryService().get.side_effect = _query_get
    # Attach the list so tests can inspect which LCs were assigned
    conn._reloaded_channels = reloaded_channels

    return conn


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestLabelChannels:
    """Tests for _label_channels."""

    def test_labels_length_mismatch_raises(self):
        """Passing wrong number of labels must raise ValueError."""
        conn = _make_conn()
        ch1, _ = _make_channel(_make_logical_channel(1))
        image = _make_image([(ch1, None)], conn)

        with pytest.raises(ValueError, match="same size"):
            _label_channels(image, ["a", "b"])

    def test_all_channels_get_new_logical_channels(self):
        """Every channel must receive a brand-new LogicalChannel, even when
        the existing LCs are unique (not shared within the image)."""
        conn = _make_conn()
        labels = ["DAPI", "FITC", "TRITC", "CY5"]
        channels = [
            _make_channel(_make_logical_channel(i, name=f"old_{i}"), channel_id=i)
            for i in range(4)
        ]
        image = _make_image(channels, conn)

        _label_channels(image, labels)

        update = conn.getUpdateService()
        # 4 new LCs created, 4 reloaded channels saved
        assert update.saveAndReturnObject.call_count == 4
        assert update.saveObject.call_count == 4

        # Each reloaded channel must have setLogicalChannel called with
        # an LC carrying the correct name
        for reloaded_ch, label in zip(conn._reloaded_channels, labels):
            reloaded_ch.setLogicalChannel.assert_called_once()
            new_lc = reloaded_ch.setLogicalChannel.call_args[0][0]
            assert new_lc.getName().val == label

    def test_channels_are_reloaded_before_save(self):
        """_label_channels must reload each Channel via getQueryService().get()
        to avoid OptimisticLockException when saving multiple channels on the
        same image sequentially."""
        conn = _make_conn()
        channels = [
            _make_channel(_make_logical_channel(i), channel_id=100 + i)
            for i in range(3)
        ]
        image = _make_image(channels, conn)

        _label_channels(image, ["A", "B", "C"])

        query = conn.getQueryService()
        assert query.get.call_count == 3
        # Verify each channel was reloaded by its OMERO id
        reloaded_ids = [c.args[1] for c in query.get.call_args_list]
        assert reloaded_ids == [100, 101, 102]

    def test_shared_lc_no_cross_contamination(self):
        """When all channels share one LogicalChannel (as OMERO does by
        default for createImageFromNumpySeq), each channel must still get
        its own independent LC."""
        conn = _make_conn()
        shared_lc = _make_logical_channel(99, name="default")
        channels = [_make_channel(shared_lc, channel_id=i) for i in range(3)]
        image = _make_image(channels, conn)

        _label_channels(image, ["A", "B", "C"])

        update = conn.getUpdateService()
        assert update.saveAndReturnObject.call_count == 3

        # All 3 reloaded channels got distinct new LCs
        assigned_lcs = [
            ch.setLogicalChannel.call_args[0][0]
            for ch in conn._reloaded_channels
        ]
        assigned_ids = [lc._id for lc in assigned_lcs]
        assert len(set(assigned_ids)) == 3

    def test_source_image_lcs_not_mutated(self):
        """Regression test for the channel-shift bug: when an output image
        is created with sourceImageId, OMERO shares the source image's
        LogicalChannels.  _label_channels on the output must NOT rename
        the source's LCs.

        Scenario (PSF Beads):
          - Input image:  4 channels [DAPI, FITC, TRITC, CY5]
          - Output image: 3 channels [FITC, TRITC, CY5]  (DAPI dropped)
          - Output's LCs point to the input's first 3 LCs

        Old bug: _label_channels renamed the shared LCs in-place →
        input became [FITC, TRITC, CY5, CY5].
        """
        conn = _make_conn()

        # Source (input) image: 4 channels with unique LCs
        source_lcs = [
            _make_logical_channel(10, "DAPI"),
            _make_logical_channel(11, "FITC"),
            _make_logical_channel(12, "TRITC"),
            _make_logical_channel(13, "CY5"),
        ]

        # Output image: 3 channels that SHARE the source's first 3 LCs
        output_channels = [
            _make_channel(source_lcs[0], channel_id=200),
            _make_channel(source_lcs[1], channel_id=201),
            _make_channel(source_lcs[2], channel_id=202),
        ]
        output_image = _make_image(output_channels, conn)

        _label_channels(output_image, ["FITC", "TRITC", "CY5"])

        # The source LCs must NOT have been mutated
        assert source_lcs[0].getName().val == "DAPI"
        assert source_lcs[1].getName().val == "FITC"
        assert source_lcs[2].getName().val == "TRITC"
        assert source_lcs[3].getName().val == "CY5"

    def test_single_channel(self):
        """Edge case: single-channel image."""
        conn = _make_conn()
        ch, lc = _make_channel(_make_logical_channel(1), channel_id=50)
        image = _make_image([(ch, lc)], conn)

        _label_channels(image, ["GFP"])

        new_lc = conn._reloaded_channels[0].setLogicalChannel.call_args[0][0]
        assert new_lc.getName().val == "GFP"

    def test_empty_labels(self):
        """Zero-channel image with empty labels should be a no-op."""
        conn = _make_conn()
        image = _make_image([], conn)
        _label_channels(image, [])
        conn.getUpdateService().saveAndReturnObject.assert_not_called()
        conn.getQueryService().get.assert_not_called()
