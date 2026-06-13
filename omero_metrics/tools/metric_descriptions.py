# =============================================================================
# Microscopy Metric Descriptions
# Professional descriptions for all KKM variables from the
# microscopemetrics schema, organized by analysis type.
# =============================================================================

# Field Illumination metrics — measure uniformity of light distribution
# across the microscope's field of view
FIELD_ILLUMINATION_DESCRIPTIONS = {
    "max_intensity": {
        "label": "Max Intensity",
        "unit": "a.u.",
        "description": (
            "Maximum pixel intensity value recorded across the entire "
            "field of view. Used to assess detector saturation and "
            "signal strength."
        ),
        "category": "Intensity",
    },
    "center_region_intensity_fraction": {
        "label": "Center Region Intensity Fraction",
        "unit": "ratio",
        "description": (
            "Ratio of the mean intensity in the central region to the "
            "mean intensity of the entire field. Values close to 1.0 "
            "indicate uniform illumination; values above 1.0 indicate "
            "a bright center (hot spot)."
        ),
        "category": "Uniformity",
    },
    "center_region_area_fraction": {
        "label": "Center Region Area Fraction",
        "unit": "ratio",
        "description": (
            "Fraction of the total image area occupied by the defined "
            "center region. Provides context for the center region "
            "intensity fraction measurement."
        ),
        "category": "Uniformity",
    },
    "center_of_mass_y_relative": {
        "label": "Center of Mass Y (Relative)",
        "unit": "relative",
        "description": (
            "Y-coordinate of the intensity center of mass, expressed "
            "relative to the image center (0.5 = perfectly centered). "
            "Deviation indicates asymmetric illumination along the "
            "vertical axis."
        ),
        "category": "Center Position",
    },
    "center_of_mass_x_relative": {
        "label": "Center of Mass X (Relative)",
        "unit": "relative",
        "description": (
            "X-coordinate of the intensity center of mass, expressed "
            "relative to the image center (0.5 = perfectly centered). "
            "Deviation indicates asymmetric illumination along the "
            "horizontal axis."
        ),
        "category": "Center Position",
    },
    "center_of_mass_distance_relative": {
        "label": "Center of Mass Distance (Relative)",
        "unit": "relative",
        "description": (
            "Euclidean distance of the intensity center of mass from "
            "the geometric center, normalized to the image diagonal. "
            "Lower values indicate better centered illumination."
        ),
        "category": "Center Position",
    },
    "center_fitted_y_relative": {
        "label": "Fitted Center Y (Relative)",
        "unit": "relative",
        "description": (
            "Y-coordinate of the illumination peak estimated by "
            "Gaussian fitting, relative to image center. More robust "
            "to noise than center of mass."
        ),
        "category": "Center Position",
    },
    "center_fitted_x_relative": {
        "label": "Fitted Center X (Relative)",
        "unit": "relative",
        "description": (
            "X-coordinate of the illumination peak estimated by "
            "Gaussian fitting, relative to image center. More robust "
            "to noise than center of mass."
        ),
        "category": "Center Position",
    },
    "center_fitted_distance_relative": {
        "label": "Fitted Center Distance (Relative)",
        "unit": "relative",
        "description": (
            "Distance of the Gaussian-fitted illumination peak from "
            "the geometric center, normalized to the image diagonal."
        ),
        "category": "Center Position",
    },
    "max_intensity_pos_y_relative": {
        "label": "Max Intensity Y (Relative)",
        "unit": "relative",
        "description": (
            "Y-coordinate of the brightest pixel, relative to image "
            "center. Sensitive to noise; compare with fitted center "
            "for robust assessment."
        ),
        "category": "Center Position",
    },
    "max_intensity_pos_x_relative": {
        "label": "Max Intensity X (Relative)",
        "unit": "relative",
        "description": (
            "X-coordinate of the brightest pixel, relative to image "
            "center."
        ),
        "category": "Center Position",
    },
    "max_intensity_distance_relative": {
        "label": "Max Intensity Distance (Relative)",
        "unit": "relative",
        "description": (
            "Distance of the brightest pixel from the geometric "
            "center, normalized to the image diagonal."
        ),
        "category": "Center Position",
    },
    "top_left_intensity_ratio": {
        "label": "Top-Left Intensity Ratio",
        "unit": "ratio",
        "description": (
            "Mean intensity of the top-left region divided by the "
            "overall mean. Values < 1.0 indicate dimmer corners; "
            "values > 1.0 indicate brighter corners."
        ),
        "category": "Regional Uniformity",
    },
    "top_center_intensity_ratio": {
        "label": "Top-Center Intensity Ratio",
        "unit": "ratio",
        "description": (
            "Mean intensity of the top-center region divided by the "
            "overall mean intensity."
        ),
        "category": "Regional Uniformity",
    },
    "top_right_intensity_ratio": {
        "label": "Top-Right Intensity Ratio",
        "unit": "ratio",
        "description": (
            "Mean intensity of the top-right region divided by the "
            "overall mean intensity."
        ),
        "category": "Regional Uniformity",
    },
    "middle_left_intensity_ratio": {
        "label": "Middle-Left Intensity Ratio",
        "unit": "ratio",
        "description": (
            "Mean intensity of the middle-left region divided by the "
            "overall mean intensity."
        ),
        "category": "Regional Uniformity",
    },
    "middle_center_intensity_ratio": {
        "label": "Middle-Center Intensity Ratio",
        "unit": "ratio",
        "description": (
            "Mean intensity of the center region divided by the "
            "overall mean. Typically the brightest region in "
            "well-aligned systems."
        ),
        "category": "Regional Uniformity",
    },
    "middle_right_intensity_ratio": {
        "label": "Middle-Right Intensity Ratio",
        "unit": "ratio",
        "description": (
            "Mean intensity of the middle-right region divided by "
            "the overall mean intensity."
        ),
        "category": "Regional Uniformity",
    },
    "bottom_left_intensity_ratio": {
        "label": "Bottom-Left Intensity Ratio",
        "unit": "ratio",
        "description": (
            "Mean intensity of the bottom-left region divided by "
            "the overall mean intensity."
        ),
        "category": "Regional Uniformity",
    },
    "bottom_center_intensity_ratio": {
        "label": "Bottom-Center Intensity Ratio",
        "unit": "ratio",
        "description": (
            "Mean intensity of the bottom-center region divided by "
            "the overall mean intensity."
        ),
        "category": "Regional Uniformity",
    },
    "bottom_right_intensity_ratio": {
        "label": "Bottom-Right Intensity Ratio",
        "unit": "ratio",
        "description": (
            "Mean intensity of the bottom-right region divided by "
            "the overall mean intensity."
        ),
        "category": "Regional Uniformity",
    },
}

# PSF Beads metrics — measure optical resolution and point spread function
# quality using sub-resolution fluorescent beads
PSF_BEADS_DESCRIPTIONS = {
    "considered_valid_count": {
        "label": "Valid Beads",
        "unit": "count",
        "description": (
            "Number of beads that passed all quality filters "
            "(edge exclusion, proximity, intensity, fit quality). "
            "Used for resolution statistics."
        ),
        "category": "Bead Detection",
    },
    "total_bead_count": {
        "label": "Total Beads Detected",
        "unit": "count",
        "description": (
            "Total number of beads detected before filtering. "
            "Compare with valid count to assess sample quality."
        ),
        "category": "Bead Detection",
    },
    "fwhm_pixel_x_mean": {
        "label": "FWHM X (px, mean)",
        "unit": "pixels",
        "description": (
            "Mean full width at half maximum of the PSF along the "
            "X-axis in pixels. Lower values indicate better lateral "
            "resolution."
        ),
        "category": "Resolution (Pixels)",
    },
    "fwhm_pixel_y_mean": {
        "label": "FWHM Y (px, mean)",
        "unit": "pixels",
        "description": (
            "Mean full width at half maximum of the PSF along the "
            "Y-axis in pixels."
        ),
        "category": "Resolution (Pixels)",
    },
    "fwhm_pixel_z_mean": {
        "label": "FWHM Z (px, mean)",
        "unit": "pixels",
        "description": (
            "Mean full width at half maximum of the PSF along the "
            "Z-axis (axial) in pixels. Axial resolution is typically "
            "2-3x worse than lateral."
        ),
        "category": "Resolution (Pixels)",
    },
    "fwhm_pixel_x_std": {
        "label": "FWHM X (px, std)",
        "unit": "pixels",
        "description": (
            "Standard deviation of FWHM along X-axis across all "
            "valid beads. High variability may indicate field-dependent "
            "aberrations."
        ),
        "category": "Resolution (Pixels)",
    },
    "fwhm_pixel_y_std": {
        "label": "FWHM Y (px, std)",
        "unit": "pixels",
        "description": (
            "Standard deviation of FWHM along Y-axis across all "
            "valid beads."
        ),
        "category": "Resolution (Pixels)",
    },
    "fwhm_pixel_z_std": {
        "label": "FWHM Z (px, std)",
        "unit": "pixels",
        "description": (
            "Standard deviation of FWHM along Z-axis across all "
            "valid beads."
        ),
        "category": "Resolution (Pixels)",
    },
    "fwhm_micron_x_mean": {
        "label": "FWHM X (mean)",
        "unit": "\u00b5m",
        "description": (
            "Mean full width at half maximum along the X-axis in "
            "micrometers. Requires voxel size calibration. The primary "
            "metric for lateral resolution assessment."
        ),
        "category": "Resolution (Calibrated)",
    },
    "fwhm_micron_y_mean": {
        "label": "FWHM Y (mean)",
        "unit": "\u00b5m",
        "description": (
            "Mean full width at half maximum along the Y-axis in "
            "micrometers."
        ),
        "category": "Resolution (Calibrated)",
    },
    "fwhm_micron_z_mean": {
        "label": "FWHM Z (mean)",
        "unit": "\u00b5m",
        "description": (
            "Mean full width at half maximum along the Z-axis in "
            "micrometers. Key metric for axial resolution."
        ),
        "category": "Resolution (Calibrated)",
    },
    "fwhm_micron_x_std": {
        "label": "FWHM X (std)",
        "unit": "\u00b5m",
        "description": (
            "Standard deviation of calibrated FWHM along X-axis."
        ),
        "category": "Resolution (Calibrated)",
    },
    "fwhm_micron_y_std": {
        "label": "FWHM Y (std)",
        "unit": "\u00b5m",
        "description": (
            "Standard deviation of calibrated FWHM along Y-axis."
        ),
        "category": "Resolution (Calibrated)",
    },
    "fwhm_micron_z_std": {
        "label": "FWHM Z (std)",
        "unit": "\u00b5m",
        "description": (
            "Standard deviation of calibrated FWHM along Z-axis."
        ),
        "category": "Resolution (Calibrated)",
    },
    "fwhm_lateral_asymmetry_ratio_mean": {
        "label": "Lateral Asymmetry (mean)",
        "unit": "ratio",
        "description": (
            "Mean ratio of FWHM_X to FWHM_Y across beads. "
            "Values close to 1.0 indicate symmetric PSF; "
            "deviation suggests astigmatism or optical misalignment."
        ),
        "category": "PSF Shape",
    },
    "fwhm_lateral_asymmetry_ratio_std": {
        "label": "Lateral Asymmetry (std)",
        "unit": "ratio",
        "description": (
            "Standard deviation of the lateral asymmetry ratio "
            "across beads. High variability indicates field-dependent "
            "astigmatism."
        ),
        "category": "PSF Shape",
    },
    "fit_gaussian_r2_z_mean": {
        "label": "Gaussian Fit R\u00b2 Z (mean)",
        "unit": "",
        "description": (
            "Mean coefficient of determination for Gaussian fit "
            "to the axial PSF profile. Values > 0.95 indicate "
            "excellent fit quality."
        ),
        "category": "Fit Quality",
    },
    "fit_gaussian_r2_y_mean": {
        "label": "Gaussian Fit R\u00b2 Y (mean)",
        "unit": "",
        "description": (
            "Mean R\u00b2 for Gaussian fit to Y-axis PSF profile."
        ),
        "category": "Fit Quality",
    },
    "fit_gaussian_r2_x_mean": {
        "label": "Gaussian Fit R\u00b2 X (mean)",
        "unit": "",
        "description": (
            "Mean R\u00b2 for Gaussian fit to X-axis PSF profile."
        ),
        "category": "Fit Quality",
    },
    "fit_airy_r2_z_mean": {
        "label": "Airy Fit R\u00b2 Z (mean)",
        "unit": "",
        "description": (
            "Mean R\u00b2 for Airy disk model fit to Z-axis profile. "
            "The Airy model better represents diffraction-limited PSFs."
        ),
        "category": "Fit Quality",
    },
    "fit_airy_r2_y_mean": {
        "label": "Airy Fit R\u00b2 Y (mean)",
        "unit": "",
        "description": (
            "Mean R\u00b2 for Airy disk model fit to Y-axis profile."
        ),
        "category": "Fit Quality",
    },
    "fit_airy_r2_x_mean": {
        "label": "Airy Fit R\u00b2 X (mean)",
        "unit": "",
        "description": (
            "Mean R\u00b2 for Airy disk model fit to X-axis profile."
        ),
        "category": "Fit Quality",
    },
    "average_bead_fwhm_pixel_z": {
        "label": "Avg Bead FWHM Z (px)",
        "unit": "pixels",
        "description": (
            "FWHM of the averaged PSF bead along Z-axis in pixels. "
            "Averaging reduces noise for a representative resolution "
            "estimate."
        ),
        "category": "Average Bead",
    },
    "average_bead_fwhm_pixel_y": {
        "label": "Avg Bead FWHM Y (px)",
        "unit": "pixels",
        "description": (
            "FWHM of the averaged PSF bead along Y-axis in pixels."
        ),
        "category": "Average Bead",
    },
    "average_bead_fwhm_pixel_x": {
        "label": "Avg Bead FWHM X (px)",
        "unit": "pixels",
        "description": (
            "FWHM of the averaged PSF bead along X-axis in pixels."
        ),
        "category": "Average Bead",
    },
    "average_bead_fwhm_micron_z": {
        "label": "Avg Bead FWHM Z",
        "unit": "\u00b5m",
        "description": (
            "FWHM of the averaged PSF bead along Z-axis in "
            "micrometers. Requires voxel calibration."
        ),
        "category": "Average Bead",
    },
    "average_bead_fwhm_micron_y": {
        "label": "Avg Bead FWHM Y",
        "unit": "\u00b5m",
        "description": (
            "FWHM of the averaged PSF bead along Y-axis in "
            "micrometers."
        ),
        "category": "Average Bead",
    },
    "average_bead_fwhm_micron_x": {
        "label": "Avg Bead FWHM X",
        "unit": "\u00b5m",
        "description": (
            "FWHM of the averaged PSF bead along X-axis in "
            "micrometers."
        ),
        "category": "Average Bead",
    },
    "average_bead_fwhm_lateral_asymmetry_ratio": {
        "label": "Avg Bead Lateral Asymmetry",
        "unit": "ratio",
        "description": (
            "Lateral asymmetry ratio of the averaged PSF bead. "
            "A robust, noise-reduced indicator of optical asymmetry."
        ),
        "category": "Average Bead",
    },
    "average_bead_fit_gaussian_r2_z": {
        "label": "Avg Bead Gaussian R\u00b2 Z",
        "unit": "",
        "description": (
            "Gaussian fit quality for the averaged bead Z-profile."
        ),
        "category": "Average Bead",
    },
    "average_bead_fit_gaussian_r2_y": {
        "label": "Avg Bead Gaussian R\u00b2 Y",
        "unit": "",
        "description": (
            "Gaussian fit quality for the averaged bead Y-profile."
        ),
        "category": "Average Bead",
    },
    "average_bead_fit_gaussian_r2_x": {
        "label": "Avg Bead Gaussian R\u00b2 X",
        "unit": "",
        "description": (
            "Gaussian fit quality for the averaged bead X-profile."
        ),
        "category": "Average Bead",
    },
    "average_bead_fit_airy_r2_z": {
        "label": "Avg Bead Airy R\u00b2 Z",
        "unit": "",
        "description": (
            "Airy fit quality for the averaged bead Z-profile."
        ),
        "category": "Average Bead",
    },
    "average_bead_fit_airy_r2_y": {
        "label": "Avg Bead Airy R\u00b2 Y",
        "unit": "",
        "description": (
            "Airy fit quality for the averaged bead Y-profile."
        ),
        "category": "Average Bead",
    },
    "average_bead_fit_airy_r2_x": {
        "label": "Avg Bead Airy R\u00b2 X",
        "unit": "",
        "description": (
            "Airy fit quality for the averaged bead X-profile."
        ),
        "category": "Average Bead",
    },
}

# Combined lookup by dataset type
METRIC_DESCRIPTIONS = {
    "FieldIlluminationDataset": FIELD_ILLUMINATION_DESCRIPTIONS,
    "PSFBeadsDataset": PSF_BEADS_DESCRIPTIONS,
}


def get_description(dataset_type, metric_key):
    """Get the description dict for a metric, or a fallback if unknown."""
    descriptions = METRIC_DESCRIPTIONS.get(dataset_type, {})
    return descriptions.get(metric_key, {
        "label": metric_key.replace("_", " ").title(),
        "unit": "",
        "description": "",
        "category": "Other",
    })


def get_category_groups(dataset_type, kkm_list):
    """Group KKM keys by category for organized display."""
    descriptions = METRIC_DESCRIPTIONS.get(dataset_type, {})
    groups = {}
    for key in kkm_list:
        desc = descriptions.get(key, {"category": "Other"})
        cat = desc["category"]
        if cat not in groups:
            groups[cat] = []
        groups[cat].append(key)
    return groups
