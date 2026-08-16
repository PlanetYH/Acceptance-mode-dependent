# Model parameters disclosed for method review

These values document the manuscript calculation but do not provide the omitted
mode fields, phase-screen libraries, PSD arrays, or numerical result tables.

## Common optical setting

- Wavelength: 10.6 micrometres.
- Pupil: ideal circular pupil in the reported comparison.
- AO case used for the principal comparison: `N_act = 41`.

## Houizot step-index fiber

- Core radius: 11 micrometres.
- Core refractive index: 2.927.
- Cladding refractive index: 2.924.
- Numerical aperture: approximately 0.133.
- Normalized frequency at 10.6 micrometres: approximately 0.864.
- External mode model: scalar LP01 solution through ofiber 0.9.1.

## Labadie-type integrated waveguide

- Substrate thickness: 4.5 micrometres.
- Substrate refractive index: 2.38.
- Guiding-film thickness: 3.8 micrometres.
- Guiding-film base refractive index: 2.78.
- Laser-written stripe width: 6.5 micrometres.
- Index increase in the written stripe: 0.05.
- Upper cladding refractive index: 1.0.
- External mode model: semi-vectorial finite-difference TE-like solution through
  modesolverpy 0.4.4.

## NCPA ensemble

- Zernike-like mode-index range: 4–200.
- Coefficient variance scaling: proportional to `(n + 1)^(-2)`; equivalently,
  the coefficient standard deviation is proportional to `(n + 1)^(-1)` for
  the reported `sauvage_alpha = 2` implementation.
- Each generated screen is piston removed and normalized to unit pupil RMS
  before multiplication by the requested arm RMS.

## Statistical hierarchy

- Independent libraries: 20.
- NCPA pairs per library: 1000.
- AO-residual pairs per library: 1000.
- Mean-null-map pair sampling: 50000 paired indices per library.
- Combined two-arm descriptor:
  `R_NCPA = sqrt(r1**2 + r2**2)`.

The random seeds and the generated random arrays are deliberately omitted from
this pre-acceptance static review snapshot.
