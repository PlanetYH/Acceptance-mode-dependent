"""Static excerpt: the nested NCPA/AO Monte Carlo hierarchy.

The actual random arrays, architecture kernels, data stores, parallel workers,
and executable configuration are deliberately omitted.
"""

import numpy as np


ARCHITECTURES = ("free_space", "houizot_fiber", "labadie_waveguide")


def draw_ncpa_pair_interface(library, candidate, r1_nm, r2_nm):
    raise NotImplementedError("NCPA random libraries are not distributed.")


def draw_ao_pair_interface(library, ao_realization):
    raise NotImplementedError("AO-residual random libraries are not distributed.")


def propagate_interface(architecture, ncpa_pair, ao_pair):
    raise NotImplementedError("Architecture kernels and fields are not distributed.")


def nested_library_logic(
    library_indices,
    working_points,
    number_of_ncpa_pairs,
    number_of_ao_pairs,
):
    """Readable representation of the statistical hierarchy used in the study.

    For one library and one two-arm RMS working point, each outer NCPA pair is
    held fixed while the inner AO pair changes. Consequently every NCPA
    candidate has a conditional AO mean and a conditional AO variance.

    This function is intentionally non-executable because all three interface
    calls above require omitted research assets.
    """
    results = {}
    for library in library_indices:
        for r1_nm, r2_nm in working_points:
            conditional_means = {key: [] for key in ARCHITECTURES}
            conditional_ao_variances = {key: [] for key in ARCHITECTURES}

            for candidate in range(number_of_ncpa_pairs):
                # One NCPA pair is shared by all architecture evaluations.
                ncpa_pair = draw_ncpa_pair_interface(
                    library, candidate, r1_nm, r2_nm
                )
                inner_nulls = {key: [] for key in ARCHITECTURES}
                for ao_index in range(number_of_ao_pairs):
                    # The same AO pair is also shared across architectures.
                    ao_pair = draw_ao_pair_interface(library, ao_index)
                    for architecture in ARCHITECTURES:
                        inner_nulls[architecture].append(
                            propagate_interface(architecture, ncpa_pair, ao_pair)
                        )

                for architecture in ARCHITECTURES:
                    conditional_means[architecture].append(
                        np.mean(inner_nulls[architecture])
                    )
                    conditional_ao_variances[architecture].append(
                        np.var(inner_nulls[architecture], ddof=1)
                    )

            for architecture in ARCHITECTURES:
                results[(library, r1_nm, r2_nm, architecture)] = {
                    "conditional_mean_by_ncpa": np.asarray(
                        conditional_means[architecture]
                    ),
                    "conditional_ao_variance_by_ncpa": np.asarray(
                        conditional_ao_variances[architecture]
                    ),
                }
    return results


def mean_raw_null_surface_logic(pair_indices, rms_grid_nm, phase_scale, unit_ncpa, ao_fields, kernels):
    """Describe the paired sampling used for the two-dimensional mean surfaces.

    Each sampled index selects one NCPA pair and one AO pair. For every point
    `(r1,r2)` on the grid, the selected unit NCPA screens are scaled by the two
    arm RMS values, combined with either no AO or the selected AO fields, and
    propagated through all three architecture kernels. The raw nulls are then
    averaged over pair indices.

    The implementation subsequently applies arm-exchange averaging
    `0.5 * (surface + surface.T)` to the paired mean surface. The arrays required
    for this calculation are intentionally absent here.
    """
    raise NotImplementedError("Mean-surface input arrays are not distributed.")


def combined_two_arm_rms(r1_nm, r2_nm):
    return np.sqrt(np.asarray(r1_nm) ** 2 + np.asarray(r2_nm) ** 2)
