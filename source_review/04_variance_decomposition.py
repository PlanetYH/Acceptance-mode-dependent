"""Static excerpt: conditional variance decomposition used for Fig. 10."""

import numpy as np


def variance_components(null_depth_by_ncpa_and_ao):
    """Separate NCPA-structure dispersion from AO-driven fluctuation.

    Parameters
    ----------
    null_depth_by_ncpa_and_ao : array, shape (n_ncpa, n_ao)
        A row holds one NCPA candidate fixed while AO realizations change.

    Returns
    -------
    conditional_mean : array, shape (n_ncpa,)
        E_AO[N | NCPA_i].
    conditional_ao_variance : array, shape (n_ncpa,)
        Var_AO[N | NCPA_i].
    V_struct : float
        Sample variance across the conditional NCPA means.
    V_AO : float
        Mean of the conditional AO sample variances.
    V_total : float
        Sample variance of all candidate/AO null values pooled together.
    """
    nulls = np.asarray(null_depth_by_ncpa_and_ao, dtype=float)
    conditional_mean = np.mean(nulls, axis=1)
    conditional_ao_variance = np.var(nulls, axis=1, ddof=1)

    V_struct = float(np.var(conditional_mean, ddof=1))
    V_AO = float(np.mean(conditional_ao_variance))
    V_total = float(np.var(nulls.reshape(-1), ddof=1))

    return {
        "conditional_mean": conditional_mean,
        "conditional_ao_variance": conditional_ao_variance,
        "V_struct": V_struct,
        "V_AO": V_AO,
        "V_total": V_total,
        "S_struct": np.sqrt(max(V_struct, 0.0)),
        "S_AO": np.sqrt(max(V_AO, 0.0)),
        "closure_relative_error": (V_struct + V_AO - V_total)
        / max(V_total, 1e-300),
    }


def interpretation():
    """Interpretive labels used in the manuscript."""
    return {
        "V_struct": "dispersion of conditional mean raw null across NCPA structures",
        "V_AO": "mean AO variance at fixed NCPA structure",
        "V_total": "pooled raw-null variance across NCPA and AO realizations",
        "finite_sample_note": (
            "All three terms are separately estimated with ddof=1. Their small "
            "closure residual is therefore an estimator-normalization effect, "
            "not a claimed exact numerical identity."
        ),
    }

