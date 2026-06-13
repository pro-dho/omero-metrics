import dash
import dash_mantine_components as dmc
from dash import html
from django_plotly_dash import DjangoDash

from omero_metrics.dash_apps.dash_analyses import dataset_shared_components as dsc
from omero_metrics.styles import (
    COLORS_CHANNELS,
    CONTAINER_STYLE,
    CONTENT_PAPER_STYLE,
    MANTINE_THEME,
    THEME,
)
from omero_metrics.tools.data_type import KKM_MAPPINGS
from omero_metrics.tools.serializers import deserialize_partial

dashboard_name = "omero_dataset_psf_beads"

omero_dataset_psf_beads = DjangoDash(
    name=dashboard_name,
    serve_locally=True,
)


omero_dataset_psf_beads.layout = dmc.MantineProvider(
    theme=MANTINE_THEME,
    children=[
        dsc.notification_provider(),
        dsc.notifications_container(),
        dsc.confirm_delete_modal(),
        dsc.dataset_header_paper(
            "PSF Beads",
            "Point Spread Function Analysis Dashboard",
            "PSF Beads Analysis",
        ),
        dmc.Container(
            children=[
                # Summary Statistics
                dsc.summary_statistics_panel("PSFBeadsDataset"),
                dmc.Space(h="md"),
                # Resolution Charts
                dmc.Grid(
                    gutter="md",
                    align="stretch",
                    children=[
                        # Left Column - FWHM Bar Chart
                        dmc.GridCol(
                            span=6,
                            children=[
                                dmc.Paper(
                                    children=[
                                        dmc.Text(
                                            "Resolution (FWHM) by Axis",
                                            fw=500,
                                            size="lg",
                                            mb="md",
                                        ),
                                        dmc.BarChart(
                                            id="fwhm_bar_chart",
                                            h=300,
                                            dataKey="channel",
                                            data=[],
                                            series=[
                                                {"name": "X", "color": "red.6"},
                                                {"name": "Y", "color": "green.6"},
                                                {"name": "Z", "color": "blue.6"},
                                            ],
                                            xAxisLabel="Channel",
                                            yAxisLabel="FWHM (pixels)",
                                            withLegend=True,
                                            legendProps={
                                                "horizontalAlign": "top",
                                                "left": 50,
                                            },
                                            tickLine="y",
                                            gridAxis="y",
                                        ),
                                    ],
                                    **CONTENT_PAPER_STYLE,
                                ),
                            ],
                        ),
                        # Right Column - Fit Quality Radar
                        dmc.GridCol(
                            span=6,
                            children=[
                                dmc.Paper(
                                    children=[
                                        dmc.Text(
                                            "Gaussian Fit Quality (R\u00b2)",
                                            fw=500,
                                            size="lg",
                                            mb="md",
                                        ),
                                        dmc.BarChart(
                                            id="fit_quality_chart",
                                            h=300,
                                            dataKey="channel",
                                            data=[],
                                            series=[
                                                {"name": "X", "color": "pink.6"},
                                                {"name": "Y", "color": "cyan.6"},
                                                {"name": "Z", "color": "violet.6"},
                                            ],
                                            xAxisLabel="Channel",
                                            yAxisLabel="R\u00b2",
                                            withLegend=True,
                                            legendProps={
                                                "horizontalAlign": "top",
                                                "left": 50,
                                            },
                                            tickLine="y",
                                            gridAxis="y",
                                        ),
                                    ],
                                    **CONTENT_PAPER_STYLE,
                                ),
                            ],
                        ),
                    ],
                ),
                dmc.Space(h="md"),
                # Key Measurements Table
                dsc.dataset_table_paper(),
                dmc.Space(h="md"),
                # Metric Reference
                dsc.metric_info_accordion(
                    "PSFBeadsDataset",
                    KKM_MAPPINGS["PSFBeadsDataset"],
                ),
            ],
            style=CONTAINER_STYLE,
        ),
        # Hidden element for callbacks
        html.Div(id="blank-input"),
    ],
)


# Register shared callbacks
dsc.register_delete_dataset_callback(omero_dataset_psf_beads)
dsc.register_download_datasets_callback(omero_dataset_psf_beads)
dsc.register_update_kkm_table_callback(omero_dataset_psf_beads)
dsc.register_download_table_callback(omero_dataset_psf_beads)
dsc.register_summary_stats_callback(omero_dataset_psf_beads)


@omero_dataset_psf_beads.expanded_callback(
    dash.dependencies.Output("fwhm_bar_chart", "data"),
    dash.dependencies.Output("fit_quality_chart", "data"),
    [dash.dependencies.Input("blank-input", "children")],
)
def update_psf_charts(*args, **kwargs):
    try:
        context = deserialize_partial(
            kwargs["session_state"]["context"], "key_measurements_df"
        )
        table_km = context["key_measurements_df"]

        # Build FWHM bar chart data per channel
        fwhm_data = []
        for _, row in table_km.iterrows():
            entry = {"channel": row.get("channel_name", "?")}
            for axis, col in [("X", "fwhm_pixel_x_mean"), ("Y", "fwhm_pixel_y_mean"), ("Z", "fwhm_pixel_z_mean")]:
                entry[axis] = round(row[col], 3) if col in row and row[col] is not None else 0
            fwhm_data.append(entry)

        # Build fit quality chart data per channel
        fit_data = []
        for _, row in table_km.iterrows():
            entry = {"channel": row.get("channel_name", "?")}
            for axis, col in [("X", "fit_gaussian_r2_x_mean"), ("Y", "fit_gaussian_r2_y_mean"), ("Z", "fit_gaussian_r2_z_mean")]:
                entry[axis] = round(row[col], 4) if col in row and row[col] is not None else 0
            fit_data.append(entry)

        return fwhm_data, fit_data
    except Exception:
        return [], []


omero_dataset_psf_beads.clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks > 0) {
            return true;
        }
        return false;
    }
    """,
    dash.dependencies.Output(
        "confirm-delete-button", "loading", allow_duplicate=True
    ),
    dash.dependencies.Input("confirm-delete-button", "n_clicks"),
    prevent_initial_call=True,
)
