"""Static excerpt: propagation from two-arm OPD screens to raw null.

This file documents equations used by the internal implementation. The guided
mode arrays, propagation grid, external solvers, and executable pipeline are
not distributed in this review snapshot.
"""

import numpy as np


def pupil_field(opd_um, pupil_mask, wavelength_um):
    """Complex unit-amplitude pupil field for a phase-only OPD screen."""
    phase = 2.0 * np.pi * opd_um / wavelength_um
    field = np.zeros(opd_um.shape, dtype=complex)
    field[pupil_mask] = np.exp(1j * phase[pupil_mask])
    return field


def external_acceptance_mode_interface(architecture):
    """Return an externally solved focal-plane acceptance field.

    ``architecture`` is either ``houizot_fiber`` or ``labadie_waveguide``.
    The complete study supplied the physical device parameters to ofiber or
    modesolverpy and received a sampled fundamental-mode field. Those fields
    and solvers are not included in this source-review snapshot.
    """
    raise NotImplementedError("External mode field is not distributed.")


def focal_field_from_pupil(pupil_complex_field, padding):
    """Conceptual Fraunhofer propagation used before mode projection.

    The internal workflow zero padded and centered the pupil field, applied a
    two-dimensional FFT, and normalized the resulting focal field and guided
    mode on the same numerical grid. Coordinate-scale optimization and the
    sampled arrays are deliberately omitted.
    """
    raise NotImplementedError("Propagation grid and scale are not distributed.")


def single_mode_coupling(opd_um, pupil_mask, wavelength_um, acceptance_mode, padding):
    """Complex overlap coefficient c(phi) for a single-mode architecture."""
    field_pupil = pupil_field(opd_um, pupil_mask, wavelength_um)
    field_focus = focal_field_from_pupil(field_pupil, padding)
    return np.vdot(acceptance_mode, field_focus)


def raw_null_from_complex_couplings(c1, c2):
    """Raw null before any realization-by-realization phase alignment."""
    numerator = abs(c1 - c2) ** 2
    denominator = abs(c1 + c2) ** 2
    return float(numerator / max(denominator, 1e-300))


def phase_aligned_single_mode_null(c1, c2):
    """Amplitude-only floor after ideal removal of relative coupling phase."""
    a1, a2 = abs(c1), abs(c2)
    return float((a1 - a2) ** 2 / max((a1 + a2) ** 2, 1e-300))


def free_space_raw_null(opd1_um, opd2_um, pupil_mask, wavelength_um):
    """Pupil-integrated dark/bright energy ratio in free space."""
    e1 = pupil_field(opd1_um, pupil_mask, wavelength_um)
    e2 = pupil_field(opd2_um, pupil_mask, wavelength_um)
    dark = np.sum(np.abs(e1[pupil_mask] - e2[pupil_mask]) ** 2)
    bright = np.sum(np.abs(e1[pupil_mask] + e2[pupil_mask]) ** 2)
    return float(dark / max(bright, 1e-300))


def vectorized_free_space_null(phase1, phase2):
    """Equivalent overlap form for arrays of pupil phase realizations."""
    n_pixels = phase1.shape[-1]
    overlap = np.sum(np.exp(1j * (phase1 - phase2)), axis=-1)
    real_overlap = np.real(overlap)
    return (n_pixels - real_overlap) / np.maximum(n_pixels + real_overlap, 1e-300)


def vectorized_single_mode_null(coupling1, coupling2):
    """Raw null for arrays of complex guided-mode coupling coefficients."""
    numerator = np.abs(coupling1 - coupling2) ** 2
    denominator = np.abs(coupling1 + coupling2) ** 2
    return numerator / np.maximum(denominator, 1e-300)

