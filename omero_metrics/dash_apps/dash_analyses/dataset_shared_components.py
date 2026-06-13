import math

import dash_mantine_components as dmc
from dash import dcc, dependencies, html, no_update
from dash_iconify import DashIconify
from linkml_runtime.dumpers import JSONDumper, YAMLDumper

from omero_metrics import views
from omero_metrics.dash_apps.dash_utils import omero_metrics_components
from omero_metrics.styles import (
    BUTTON_STYLE,
    CONTENT_PAPER_STYLE,
    HEADER_PAPER_STYLE,
    TABLE_MANTINE_STYLE,
    THEME,
)
from omero_metrics.tools import load
from omero_metrics.tools.metric_descriptions import get_description
from omero_metrics.tools.serializers import deserialize, deserialize_partial


# COMPONENTS
def notification_provider():
    return dmc.NotificationProvider(position="top-center")


def notifications_container():
    return html.Div(id="notifications_container")


def confirm_delete_modal():
    return dmc.Modal(
        title="Confirm Delete",
        id="confirm-delete-modal",
        children=[
            dmc.Text("Are you sure you want to delete this dataset outputs?"),
            dmc.Space(h=20),
            dmc.Group(
                [
                    dmc.Button(
                        "Delete",
                        id="confirm-delete-button",
                        color="red",
                    ),
                    dmc.Button(
                        "Cancel",
                        id="cancel-delete-button",
                        color="gray",
                        variant="outline",
                    ),
                ],
                justify="flex-end",
            ),
        ],
    )


def dataset_header_paper(title, description, tag, load_buttons=True):
    return dmc.Paper(
        children=[
            dmc.Group(
                [
                    dmc.Group(
                        [
                            html.Img(
                                src="/static/omero_metrics/images/metrics_logo.png",
                                style={
                                    "width": "120px",
                                    "height": "auto",
                                },
                            ),
                            dmc.Stack(
                                [
                                    dmc.Title(
                                        title,
                                        c=THEME["primary"],
                                        size="h2",
                                    ),
                                    dmc.Text(
                                        description,
                                        c=THEME["text"]["secondary"],
                                        size="sm",
                                    ),
                                ],
                                gap="xs",
                            ),
                        ],
                    ),
                    dmc.Group(
                        [
                            download_group,
                            delete_button,
                            dmc.Badge(
                                tag,
                                color=THEME["primary"],
                                variant="dot",
                                size="lg",
                            ),
                        ]
                        if load_buttons
                        else dmc.Badge(
                            tag,
                            color=THEME["primary"],
                            variant="dot",
                            size="lg",
                        )
                    ),
                ],
                justify="space-between",
            ),
        ],
        **HEADER_PAPER_STYLE,
    )


def dataset_table_paper():
    return dmc.Paper(
        children=[
            dmc.Stack(
                [
                    dmc.Group(
                        [
                            dmc.Text(
                                "Key Measurements",
                                fw=500,
                                size="lg",
                            ),
                            dmc.Group(
                                [
                                    omero_metrics_components.download_table,
                                    dmc.Tooltip(
                                        label="Key measurements for all channels. Hover column headers for metric descriptions.",
                                        children=[
                                            omero_metrics_components.get_icon(
                                                icon="material-symbols:info",
                                                color=THEME["primary"],
                                            )
                                        ],
                                        withArrow=True,
                                        multiline=True,
                                        w=280,
                                    ),
                                ]
                            ),
                        ],
                        justify="space-between",
                    ),
                    dmc.ScrollArea(
                        offsetScrollbars=True,
                        children=[
                            dmc.Table(
                                id="kkm_table",
                                striped=True,
                                highlightOnHover=True,
                                withTableBorder=False,
                                withColumnBorders=True,
                                fz="sm",
                                style=TABLE_MANTINE_STYLE,
                            ),
                            dmc.Group(
                                mt="md",
                                children=[
                                    dmc.Pagination(
                                        id="kkm_table_pagination",
                                        total=0,
                                        value=1,
                                        withEdges=True,
                                    )
                                ],
                                justify="center",
                            ),
                        ],
                    ),
                ],
                gap="md",
                justify="space-between",
                h="100%",
            ),
        ],
        **CONTENT_PAPER_STYLE,
    )


download_group = dmc.Group(
    [
        dmc.Menu(
            [
                dmc.MenuTarget(
                    dmc.Button(
                        id="activate_download",
                        children="Download",
                        leftSection=DashIconify(
                            icon="material-symbols:download", width=20
                        ),
                        rightSection=DashIconify(
                            icon="carbon:chevron-down", width=20
                        ),
                        color=THEME["primary"],
                        variant="outline",
                    )
                ),
                dmc.MenuDropdown(
                    [
                        dmc.MenuItem(
                            "YAML",
                            id="download-yaml",
                            leftSection=DashIconify(
                                icon="vscode-icons:file-type-yaml", width=20
                            ),
                        ),
                        dmc.MenuItem(
                            "JSON",
                            id="download-json",
                            leftSection=DashIconify(
                                icon="vscode-icons:file-type-json", width=20
                            ),
                        ),
                        dmc.MenuItem(
                            "Text",
                            id="download-text",
                            leftSection=DashIconify(
                                icon="vscode-icons:file-type-text", width=20
                            ),
                        ),
                    ]
                ),
            ],
            trigger="click",
        ),
        dcc.Download(id="download"),
    ]
)


delete_button = dmc.Button(
    id="delete_data",
    children="Delete",
    color="red",
    variant="filled",
    leftSection=DashIconify(icon="ic:round-delete-forever"),
)


def _stat_card(label, value, unit="", icon=None, color=None):
    """Single statistic display card."""
    color = color or THEME["primary"]
    icon_el = (
        omero_metrics_components.get_icon(icon=icon, size=20, color=color)
        if icon
        else None
    )
    return dmc.Paper(
        children=dmc.Stack(
            [
                dmc.Group(
                    [
                        icon_el,
                        dmc.Text(label, size="xs", c=THEME["text"]["secondary"], fw=500),
                    ] if icon_el else [
                        dmc.Text(label, size="xs", c=THEME["text"]["secondary"], fw=500),
                    ],
                    gap="xs",
                ),
                dmc.Group(
                    [
                        dmc.Text(
                            f"{value}" if not isinstance(value, float) else f"{value:.3f}",
                            size="xl",
                            fw=700,
                            c=THEME["text"]["primary"],
                        ),
                        dmc.Text(unit, size="xs", c=THEME["text"]["muted"]) if unit else None,
                    ],
                    gap=4,
                    align="baseline",
                ),
            ],
            gap=4,
        ),
        p="md",
        radius="md",
        withBorder=True,
        style={
            "borderLeft": f"3px solid {color}",
            "minWidth": "140px",
        },
    )


def summary_statistics_panel(dataset_class=None):
    """Summary statistics panel — populated by callback."""
    return dmc.Paper(
        id="summary-stats-panel",
        children=[
            dmc.Group(
                [
                    dmc.Text(
                        "Summary",
                        fw=600,
                        size="lg",
                    ),
                    dmc.Tooltip(
                        label="Key performance indicators at a glance",
                        children=[
                            omero_metrics_components.get_icon(
                                icon="material-symbols:info",
                                color=THEME["primary"],
                            )
                        ],
                    ),
                ],
                justify="space-between",
                mb="md",
            ),
            dmc.SimpleGrid(
                id="summary-stat-cards",
                cols={"base": 2, "sm": 3, "lg": 5},
                spacing="sm",
            ),
        ],
        **CONTENT_PAPER_STYLE,
    )


def metric_info_accordion(dataset_class, kkm_list):
    """Accordion showing metric descriptions grouped by category."""
    from omero_metrics.tools.metric_descriptions import get_category_groups

    groups = get_category_groups(dataset_class, kkm_list)
    items = []
    for category, keys in groups.items():
        rows = []
        for key in keys:
            desc = get_description(dataset_class, key)
            rows.append(
                dmc.Group(
                    [
                        dmc.Stack(
                            [
                                dmc.Group(
                                    [
                                        dmc.Text(
                                            desc["label"],
                                            fw=600,
                                            size="sm",
                                        ),
                                        dmc.Badge(
                                            desc["unit"],
                                            size="xs",
                                            variant="light",
                                            color="gray",
                                        ) if desc["unit"] else None,
                                    ],
                                    gap="xs",
                                ),
                                dmc.Text(
                                    desc["description"],
                                    size="xs",
                                    c=THEME["text"]["secondary"],
                                ),
                            ],
                            gap=2,
                        ),
                    ],
                    p="xs",
                    style={
                        "borderBottom": f"1px solid {THEME['border_light']}",
                    },
                )
            )
        items.append(
            dmc.AccordionItem(
                [
                    dmc.AccordionControl(
                        dmc.Group(
                            [
                                dmc.Text(category, fw=600, size="sm"),
                                dmc.Badge(
                                    str(len(keys)),
                                    size="xs",
                                    variant="filled",
                                    color=THEME["primary"],
                                    circle=True,
                                ),
                            ],
                            gap="sm",
                        )
                    ),
                    dmc.AccordionPanel(children=rows),
                ],
                value=category,
            )
        )
    return dmc.Paper(
        children=[
            dmc.Group(
                [
                    dmc.Text("Metric Reference", fw=600, size="lg"),
                    omero_metrics_components.get_icon(
                        icon="material-symbols:library-books",
                        color=THEME["primary"],
                    ),
                ],
                justify="space-between",
                mb="md",
            ),
            dmc.Accordion(
                children=items,
                variant="separated",
                radius="md",
            ),
        ],
        **CONTENT_PAPER_STYLE,
    )


# CALLBACKS
def register_delete_dataset_callback(app):
    @app.expanded_callback(
        dependencies.Output("confirm-delete-modal", "opened"),
        dependencies.Output("notifications_container", "children"),
        dependencies.Output("confirm-delete-button", "loading"),
        [
            dependencies.Input("delete_data", "n_clicks"),
            dependencies.Input("confirm-delete-button", "n_clicks"),
            dependencies.Input("cancel-delete-button", "n_clicks"),
            dependencies.State("confirm-delete-modal", "opened"),
        ],
        prevent_initial_call=True,
    )
    def delete_dataset_callback(
        delete_data_clicks,
        confirm_delete_button_clicks,
        cancel_delete_button_clicks,
        confirm_delete_modal_opened,
        **kwargs,
    ):
        triggered_button = kwargs["callback_context"].triggered[0]["prop_id"]
        dataset_id = kwargs["session_state"]["context"]["dataset_id"]
        request = kwargs["request"]
        opened = not confirm_delete_modal_opened
        if (
            triggered_button == "confirm-delete-button.n_clicks"
            and delete_data_clicks > 0
        ):
            response_type, response_msg = views.delete_dataset(
                request, dataset_id=dataset_id
            )

            return omero_metrics_components.notification_handler(
                response_type, response_msg, opened
            )
        else:
            return opened, None, False


def register_download_datasets_callback(app):
    @app.expanded_callback(
        dependencies.Output("download", "data"),
        [
            dependencies.Input("download-yaml", "n_clicks"),
            dependencies.Input("download-json", "n_clicks"),
            dependencies.Input("download-text", "n_clicks"),
        ],
        prevent_initial_call=True,
    )
    def download_dataset_callback(
        dl_yaml_n_clicks, dl_json_n_clicks, dl_text_n_clicks, **kwargs
    ):
        if not kwargs["callback_context"].triggered:
            return no_update

        triggered_id = (
            kwargs["callback_context"].triggered[0]["prop_id"].split(".")[0]
        )
        context = deserialize_partial(
            kwargs["session_state"]["context"], "mm_dataset"
        )
        mm_dataset = context["mm_dataset"]
        file_name = mm_dataset.name
        yaml_dumper = YAMLDumper()
        json_dumper = JSONDumper()
        if triggered_id == "download-yaml":
            return dict(
                content=yaml_dumper.dumps(mm_dataset), filename=f"{file_name}.yaml"
            )

        elif triggered_id == "download-json":
            return dict(
                content=json_dumper.dumps(mm_dataset), filename=f"{file_name}.json"
            )

        elif triggered_id == "download-text":
            return dict(
                content=yaml_dumper.dumps(mm_dataset), filename=f"{file_name}.txt"
            )

        return no_update


def _build_header_with_tooltip(col_key, dataset_class):
    """Build a table header element with a tooltip showing the metric description."""
    desc = get_description(dataset_class, col_key)
    display_name = col_key.replace("_", " ").title()
    if desc["description"]:
        return dmc.Tooltip(
            dmc.Text(
                display_name,
                size="xs",
                fw=600,
                style={"cursor": "help", "borderBottom": "1px dotted #8a9b8e"},
            ),
            label=desc["description"],
            withArrow=True,
            multiline=True,
            w=300,
            position="top",
        )
    return display_name


def register_update_kkm_table_callback(app):
    @app.expanded_callback(
        dependencies.Output("kkm_table", "data"),
        dependencies.Output("kkm_table_pagination", "total"),
        [
            dependencies.Input("kkm_table_pagination", "value"),
        ],
    )
    def update_kkm_table_callback(pagination_value, **kwargs):
        try:
            page = int(pagination_value)
            context = deserialize_partial(
                kwargs["session_state"]["context"], "key_measurements_df"
            )
            kkm = kwargs["session_state"]["context"]["kkm"]
            dataset_class = kwargs["session_state"]["context"].get("dataset_class", "")
            table_km = context["key_measurements_df"]
            start_idx = (page - 1) * 4
            end_idx = start_idx + 4
            columns = ["channel_name"] + [
                k for k in kkm if k in table_km.columns
            ]
            metrics_df = table_km[columns]
            metrics_df = metrics_df.round(3)

            # Build headers with tooltips
            headers = ["Channel"]
            for col in columns[1:]:
                headers.append(_build_header_with_tooltip(col, dataset_class))

            page_data = metrics_df.iloc[start_idx:end_idx]
            return {
                "head": headers,
                "body": page_data.values.tolist(),
                "caption": "Hover column headers for metric descriptions",
            }, math.ceil(len(metrics_df) / 4)
        except Exception as e:
            return {
                "head": ["Error"],
                "body": [[str(e)]],
                "caption": "Error loading measurements",
            }, 1


def register_download_table_callback(app):
    @app.expanded_callback(
        dependencies.Output("table-download", "data"),
        [
            dependencies.Input("table-download-csv", "n_clicks"),
            dependencies.Input("table-download-xlsx", "n_clicks"),
            dependencies.Input("table-download-json", "n_clicks"),
        ],
        prevent_initial_call=True,
    )
    def download_table_callback(
        tb_dw_csv_clicks, tb_dw_xlsx_clicks, tb_dw_json_clicks, **kwargs
    ):
        if not kwargs["callback_context"].triggered:
            return no_update

        triggered_id = (
            kwargs["callback_context"].triggered[0]["prop_id"].split(".")[0]
        )
        context = deserialize_partial(
            kwargs["session_state"]["context"], "key_measurements_df"
        )
        table_km = context["key_measurements_df"]
        kkm = kwargs["session_state"]["context"]["kkm"]
        columns = ["channel_name"] + [k for k in kkm if k in table_km.columns]
        table_kkm = table_km[columns]
        table_kkm = table_kkm.round(3)
        table_kkm.columns = table_kkm.columns.str.replace("_", " ").str.title()
        if triggered_id == "table-download-csv":
            return dcc.send_data_frame(table_kkm.to_csv, "km_table.csv")
        elif triggered_id == "table-download-xlsx":
            return dcc.send_data_frame(table_kkm.to_excel, "km_table.xlsx")
        elif triggered_id == "table-download-json":
            return dcc.send_data_frame(table_kkm.to_json, "km_table.json")

        return no_update


def register_summary_stats_callback(app):
    """Populate summary statistics cards from key measurements."""

    @app.expanded_callback(
        dependencies.Output("summary-stat-cards", "children"),
        [dependencies.Input("kkm_table_pagination", "value")],
    )
    def update_summary_stats(_, **kwargs):
        try:
            context = deserialize_partial(
                kwargs["session_state"]["context"], "key_measurements_df"
            )
            dataset_class = kwargs["session_state"]["context"].get("dataset_class", "")
            kkm = kwargs["session_state"]["context"]["kkm"]
            table_km = context["key_measurements_df"]
            cards = []

            # Pick highlight metrics based on dataset type
            if "FieldIllumination" in dataset_class:
                highlights = [
                    ("center_region_intensity_fraction", "material-symbols:center-focus-strong", THEME["primary"]),
                    ("max_intensity", "material-symbols:brightness-high", THEME["accent"]),
                    ("center_of_mass_distance_relative", "material-symbols:my-location", "#d69e2e"),
                    ("middle_center_intensity_ratio", "material-symbols:grid-on", THEME["secondary"]),
                    ("center_fitted_distance_relative", "material-symbols:target", "#3182ce"),
                ]
            elif "PSFBeads" in dataset_class:
                highlights = [
                    ("considered_valid_count", "material-symbols:check-circle", THEME["primary"]),
                    ("total_bead_count", "material-symbols:scatter-plot", THEME["accent"]),
                    ("fwhm_pixel_x_mean", "material-symbols:width", "#d69e2e"),
                    ("fwhm_pixel_y_mean", "material-symbols:height", "#3182ce"),
                    ("fwhm_pixel_z_mean", "material-symbols:layers", THEME["secondary"]),
                ]
            else:
                highlights = [(k, "material-symbols:analytics", THEME["primary"]) for k in kkm[:5]]

            for metric_key, icon, color in highlights:
                if metric_key in table_km.columns:
                    desc = get_description(dataset_class, metric_key)
                    mean_val = table_km[metric_key].mean()
                    cards.append(
                        _stat_card(
                            label=desc["label"],
                            value=mean_val,
                            unit=desc["unit"],
                            icon=icon,
                            color=color,
                        )
                    )
            return cards
        except Exception:
            return []
