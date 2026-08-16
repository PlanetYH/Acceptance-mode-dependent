"""Static excerpt: NCPA and AO-residual phase-screen construction logic."""

import numpy as np


def pupil_rms(values, pupil_mask):
    selected = values[pupil_mask]
    return float(np.sqrt(np.mean(selected * selected)))


def remove_piston_and_normalize_unit_rms(screen, pupil_mask):
    """Apply the normalization used before scaling a screen to an OPD RMS."""
    output = np.array(screen, dtype=float, copy=True)
    output[~pupil_mask] = 0.0
    output[pupil_mask] -= float(np.mean(output[pupil_mask]))
    rms = pupil_rms(output, pupil_mask)
    if rms <= 0.0:
        raise ValueError("zero-RMS screen")
    output[pupil_mask] /= rms
    return output


def sample_sauvage_type_modal_coefficients(radial_orders, random_generator, alpha=2.0):
    """Draw NCPA coefficients with variance proportional to (n + 1)^(-alpha).

    The mode list covers the reported Zernike-like indices j=4,...,200, with
    piston, tip, and tilt excluded. In the complete implementation, every basis
    image is first normalized to unit RMS on the actual circular pupil.
    """
    sigma = 1.0 / (np.asarray(radial_orders, dtype=float) + 1.0) ** (alpha / 2.0)
    return random_generator.normal(size=sigma.size) * sigma


def synthesize_ncpa_screen(unit_rms_basis, radial_orders, random_generator):
    coefficients = sample_sauvage_type_modal_coefficients(radial_orders, random_generator)
    screen = np.tensordot(coefficients, unit_rms_basis, axes=(0, 0))
    # The pupil mask and the actual basis arrays are omitted from this archive.
    return screen, coefficients


def external_ao_psd_interface(physical_parameters):
    """Interface to the omitted MAOPPY residual-PSD calculation.

    Parameters supplied in the complete workflow include wavelength, Fried
    parameter, actuator count, pupil diameter, PSD resolution, sampling, and
    instrument parameters. The return values are a two-dimensional phase PSD,
    integrated phase variance, and spatial-frequency sampling.
    """
    raise NotImplementedError("MAOPPY implementation and PSD output are omitted.")


def sample_real_screen_from_psd(psd, physical_extent_m, random_generator):
    """Fourier draw applied after the external PSD has been obtained."""
    psd_amplitude = np.fft.fftshift(np.sqrt(np.maximum(psd, 0.0)))
    white_complex_noise = (
        random_generator.standard_normal(psd.shape)
        + 1j * random_generator.standard_normal(psd.shape)
    )
    fourier_coefficients = psd_amplitude * white_complex_noise / physical_extent_m
    return np.real(np.fft.ifft2(fourier_coefficients)) * np.size(psd)


def scale_unit_ncpa_to_opd(unit_screen, requested_rms_nm):
    """Convert a piston-free unit-RMS NCPA realization to OPD in micrometres."""
    return unit_screen * (requested_rms_nm / 1000.0)


def convert_ao_phase_to_opd_um(phase_rad, wavelength_um):
    """Convert an AO phase screen in radians to optical path difference."""
    return phase_rad * wavelength_um / (2.0 * np.pi)


def radial_modal_energy_fraction(coefficients, azimuthal_orders):
    """Natural fraction of modal coefficient energy in m=0 modes."""
    energy = np.asarray(coefficients, dtype=float) ** 2
    radial = np.asarray(azimuthal_orders) == 0
    return float(energy[radial].sum() / max(energy.sum(), 1e-300))


def two_arm_radial_descriptors(f_rad_arm1, f_rad_arm2, r1_nm, r2_nm):
    """RMS-squared-weighted total radial content and arm imbalance."""
    total_energy_scale = max(r1_nm**2 + r2_nm**2, 1e-300)
    radial_energy1 = r1_nm**2 * f_rad_arm1
    radial_energy2 = r2_nm**2 * f_rad_arm2
    eta_rad = (radial_energy1 + radial_energy2) / total_energy_scale
    delta_rad = abs(radial_energy1 - radial_energy2) / total_energy_scale
    return eta_rad, delta_rad
