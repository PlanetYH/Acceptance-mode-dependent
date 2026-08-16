"""Static excerpt: adjusted radial-content association and library slopes."""

import numpy as np


def natural_radial_fraction(coefficients, azimuthal_orders):
    """Coefficient-energy fraction carried by m=0 modes in one NCPA screen."""
    energy = np.asarray(coefficients, dtype=float) ** 2
    radial = np.asarray(azimuthal_orders) == 0
    return float(energy[radial].sum() / max(energy.sum(), 1e-300))


def two_arm_radial_descriptors(f_rad_arm1, f_rad_arm2, r1_nm, r2_nm):
    """Definitions of eta_rad and delta_rad used in the regression."""
    denominator = max(r1_nm**2 + r2_nm**2, 1e-300)
    energy1 = r1_nm**2 * f_rad_arm1
    energy2 = r2_nm**2 * f_rad_arm2
    eta_rad = (energy1 + energy2) / denominator
    delta_rad = abs(energy1 - energy2) / denominator
    return eta_rad, delta_rad


def center_within_working_point(values, group_index):
    """Subtract the mean within each library/architecture/R/theta stratum."""
    values = np.asarray(values, dtype=float)
    centered = np.empty_like(values)
    for group in np.unique(group_index):
        selected = group_index == group
        centered[selected] = values[selected] - np.mean(values[selected])
    return centered


def adjusted_radial_regression(centered_outcome, centered_eta, centered_delta):
    """Fit Y~=beta_eta*eta~+beta_delta*delta~+epsilon.

    `eta` is the natural two-arm radial-content descriptor and `delta` is the
    arm-to-arm radial-content imbalance. The adjusted ordinate shown in the
    association plot removes only the fitted imbalance contribution.
    """
    y = np.asarray(centered_outcome, dtype=float)
    X = np.column_stack([centered_eta, centered_delta])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    beta_eta, beta_delta = float(beta[0]), float(beta[1])
    adjusted_outcome = y - beta_delta * np.asarray(centered_delta)
    return {
        "beta_eta": beta_eta,
        "beta_delta": beta_delta,
        "adjusted_outcome": adjusted_outcome,
    }


def independent_library_slopes(table):
    """Conceptual grouping used for the reproducibility panel.

    One `beta_eta` is estimated separately for each independent random library,
    architecture, and outcome. The first set of independently seeded libraries
    is labelled discovery and the second set validation. Both sets come from the
    same generative physical/statistical model.

    The input table and the resulting numerical slopes are omitted from this
    review snapshot.
    """
    raise NotImplementedError("Regression data and fitted slopes are not distributed.")


def interpretation():
    return {
        "scatter_line": (
            "The plotted line is the fitted association with eta_rad after "
            "controlling the centered arm-imbalance descriptor delta_rad."
        ),
        "negative_adjusted_values": (
            "The ordinate is a centered/adjusted outcome, not a physical raw "
            "null depth; values below zero are therefore permitted."
        ),
        "causality": (
            "eta_rad was observed in naturally generated screens rather than "
            "experimentally injected, so the analysis supports association, "
            "not causal proof."
        ),
    }
