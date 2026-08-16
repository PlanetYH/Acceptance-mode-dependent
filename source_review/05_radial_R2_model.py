"""Static excerpt: radial-only fourth-degree polynomial and R-squared."""

import numpy as np


def radial_only_model(rms_grid_nm, mean_raw_null_surface, degree=4):
    """Fit log10(mean raw null) as a function only of combined two-arm RMS.

    The fitted function is

        f(R) = beta_0 + beta_1*x + ... + beta_4*x**4,

    where R = sqrt(r1**2 + r2**2) and x = R / max(R). Scaling R does not alter
    the fitted fourth-degree polynomial space or R-squared; it improves numerical
    conditioning of the least-squares design matrix.
    """
    r1, r2 = np.meshgrid(rms_grid_nm, rms_grid_nm, indexing="ij")
    R = np.sqrt(r1**2 + r2**2)

    surface = np.asarray(mean_raw_null_surface, dtype=float)
    valid = np.isfinite(surface) & (surface > 0.0)
    x = R[valid] / max(float(np.max(R)), 1.0)
    y = np.log10(surface[valid])

    design = np.column_stack([x**power for power in range(degree + 1)])
    beta, *_ = np.linalg.lstsq(design, y, rcond=None)
    fitted = design @ beta

    residual_sum_of_squares = float(np.sum((y - fitted) ** 2))
    total_sum_of_squares = float(np.sum((y - np.mean(y)) ** 2))
    R_squared = 1.0 - residual_sum_of_squares / max(total_sum_of_squares, 1e-300)

    return beta, R_squared


def interpretation():
    return (
        "R-squared is the fraction of variation in the two-dimensional "
        "log10 mean-null surface described by combined NCPA RMS alone. It does "
        "not prove that arm allocation or spatial structure has no effect."
    )

