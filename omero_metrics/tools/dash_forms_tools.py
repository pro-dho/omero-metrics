import re
from dataclasses import fields
from typing import Union, get_args, get_origin

import dash_mantine_components as dmc
from dash_iconify import DashIconify

# TODO: Modify the schema to make this a mm_schema class
from linkml_runtime.utils.metamodelcore import XSDDateTime
from microscopemetrics_schema.datamodel.microscopemetrics_schema import ProtocolUrl

# These mappings must be ordered by priority
FIELD_TYPE_MAPPING = {
    XSDDateTime: [dmc.DateTimePicker, "carbon:calendar"],
    ProtocolUrl: [dmc.TextInput, "carbon:copy-link"],
    float: [dmc.NumberInput, "carbon:character-decimal"],
    int: [dmc.NumberInput, "carbon:character-whole-number"],
    bool: [dmc.Switch, "carbon:switch-disabled"],
    str: [dmc.TextInput, "carbon:string-text"],
}

# Help text shown below each form field via the `description` prop.
# Keys follow the pattern "ClassName:field_name" or just "field_name"
# for fields shared across multiple parameter classes.
FIELD_DESCRIPTIONS = {
    # FieldIlluminationInputParameters
    "saturation_threshold": (
        "Fraction of the detector dynamic range considered saturated (0-1). "
        "Pixels above this threshold are flagged."
    ),
    "corner_fraction": (
        "Fraction of the image width/height used to define corner regions "
        "for uniformity analysis (e.g. 0.1 = 10%)."
    ),
    "sigma": (
        "Standard deviation of the Gaussian filter applied to smooth the "
        "illumination image before analysis (in pixels)."
    ),
    "bit_depth": (
        "Bit depth of the input images (e.g. 8, 12, 16). "
        "Leave empty to auto-detect from the image data."
    ),
    # PSFBeadsInputParameters
    "min_lateral_distance_factor": (
        "Minimum distance between beads as a factor of the PSF FWHM. "
        "Beads closer than this are excluded to avoid overlap."
    ),
    "sigma_min": (
        "Minimum sigma for Gaussian fitting of the PSF (in pixels). "
        "Defines the lower bound of the expected PSF width."
    ),
    "sigma_max": (
        "Maximum sigma for Gaussian fitting of the PSF (in pixels). "
        "Defines the upper bound of the expected PSF width."
    ),
    "snr_threshold": (
        "Minimum signal-to-noise ratio for a bead to be considered valid. "
        "Beads below this are excluded from statistics."
    ),
    "fitting_gaussian_r2_threshold": (
        "Minimum R-squared for the Gaussian fit. "
        "Beads with Gaussian fits below this threshold are rejected."
    ),
    "fitting_airy_r2_threshold": (
        "Minimum R-squared for the Airy disk fit. "
        "Beads with Airy fits below this threshold are rejected."
    ),
    "intensity_robust_z_score_threshold": (
        "Z-score threshold for robust intensity outlier detection. "
        "Beads with intensity z-scores above this are excluded."
    ),
    # Sample fields
    "name": "Name identifier for this sample or configuration.",
    "description": "Free-text description providing additional context.",
    "manufacturer": "Manufacturer or vendor of the reference sample.",
    "preparation_protocol": "URL or reference to the sample preparation protocol.",
    "preparation_datetime": "Date and time when the sample was prepared.",
    "bead_diameter_micron": (
        "Diameter of the fluorescent beads in micrometers. "
        "Typically 0.1 \u00b5m (100 nm) for sub-resolution PSF measurements."
    ),
}


def extract_form_data(form_content):
    return {
        i["props"]["id"].split(":")[1]: i["props"]["value"] for i in form_content
    }


def disable_all_fields_dash_form(form):
    for i, t in enumerate(form):
        form[i]["props"]["disabled"] = True
    return form


def clean_field_name(field: str):
    return field.replace("_", " ").title()


def get_field_types(field):
    data_type = {
        "field_name": field.name,
        "type": None,
        "optional": False,
        "default": field.default,
    }
    if get_origin(field.type) is Union:
        args = get_args(field.type)
        # Check if it's Optional (Union with None)
        if type(None) in args:
            data_type["optional"] = True
            args = [arg for arg in args if arg is not type(None)]

        # Select type by priority based on FIELD_TYPE_MAPPING order
        selected_type = None
        for priority_type in FIELD_TYPE_MAPPING.keys():
            if priority_type in args:
                selected_type = priority_type
                break

        data_type["type"] = selected_type
    elif field.type in FIELD_TYPE_MAPPING.keys():
        data_type["type"] = field.type

    return data_type


def _get_field_description(class_name, field_name):
    """Look up help text for a form field."""
    # Try class-specific key first, then generic field name
    return FIELD_DESCRIPTIONS.get(
        f"{class_name}:{field_name}",
        FIELD_DESCRIPTIONS.get(field_name, None),
    )


def get_dmc_field_input(field, mm_object, disabled=False):
    field_info = get_field_types(field)
    input_field_name = FIELD_TYPE_MAPPING[field_info["type"]][0]
    input_field = input_field_name()
    input_field.id = f"{mm_object.class_name}:{field_info['field_name']}"
    input_field.label = clean_field_name(field_info["field_name"])
    input_field.placeholder = f"Enter {clean_field_name(field_info['field_name'])}"
    input_field.value = (
        field_info["default"]
        if getattr(mm_object, field.name) is None
        else getattr(mm_object, field.name)
    )
    input_field.w = "100%"
    input_field.disabled = disabled
    input_field.required = not field_info["optional"]
    input_field.leftSection = DashIconify(
        icon=FIELD_TYPE_MAPPING[field_info["type"]][1]
    )
    input_field.mb = "sm"

    # Add a help icon in the right section that shows a tooltip on hover
    help_text = _get_field_description(mm_object.class_name, field_info["field_name"])
    if help_text:
        input_field.rightSection = dmc.Tooltip(
            dmc.ActionIcon(
                DashIconify(icon="material-symbols:help-outline", height=16),
                variant="subtle",
                color="gray",
                size="sm",
            ),
            label=help_text,
            multiline=True,
            w=280,
            withArrow=True,
            position="left",
        )
        input_field.rightSectionPointerEvents = "auto"

    return input_field


def validate_form(state):
    return all(
        i["props"]["id"] == "submit_id"
        or not (
            i["props"]["required"]
            and (i["props"]["value"] is None or i["props"]["value"] == "")
        )
        for i in state
    )


def add_space_between_capitals(s: str) -> str:
    label = re.sub(r"(?<!^)(?=[A-Z])", " ", s)
    label = label.replace("P S F", "PSF")
    return label


def get_form(mm_object, disabled=False, form_id="form_content"):
    form_content = dmc.Fieldset(
        id=form_id,
        children=[],
        # TODO: we have to rather rely on the title of the class
        legend=add_space_between_capitals(mm_object.class_name),
        variant="filled",
        radius="md",
    )
    for field in fields(mm_object):
        form_content.children.append(
            get_dmc_field_input(field, mm_object, disabled=disabled)
        )
    return form_content
