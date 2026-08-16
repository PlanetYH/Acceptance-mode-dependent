# External software interfaces

This file records only the interface contracts used by the complete internal
workflow. Third-party source code, binaries, installation instructions, download
locations, and generated mode/PSD arrays are not distributed in this review
snapshot.

## MAOPPY

- Version information: local source snapshot used in the study; the exact
  upstream revision was not recorded in the archived directory.
- Role: evaluate the Fétick-type adaptive-optics residual phase power spectral
  density with the selected instrument parameterization.
- Principal interface used: an instrument description and a `Psfao` model whose
  PSD evaluator accepts the wavelength-scaled model parameters.
- Inputs supplied by the internal workflow: wavelength, Fried parameter,
  actuator count/cutoff, pupil diameter, PSD-grid size, phase sampling, and
  instrument parameters.
- Outputs consumed by the internal workflow: a two-dimensional residual phase
  PSD, its integrated variance, and the spatial-frequency sampling.

## ofiber

- Version: 0.9.1.
- Role: solve the scalar circular step-index LP01 mode for the Houizot
  chalcogenide fiber.
- Inputs supplied by the internal workflow: wavelength, core radius, core
  refractive index, and cladding refractive index.
- Quantities consumed by the internal workflow: normalized frequency `V`,
  normalized propagation constant `b`, radial LP01 complex-amplitude profile,
  and mode-size diagnostics.

## modesolverpy

- Version: 0.4.4.
- Role: solve the fundamental semi-vectorial transverse-electric-like mode of
  the Labadie-type integrated waveguide.
- Inputs supplied by the internal workflow: wavelength, rectangular
  cross-sectional refractive-index distribution, spatial grid, number of
  requested eigenmodes, and eigensolver tolerance.
- Quantities consumed by the internal workflow: effective index and the sampled
  transverse fundamental-mode field.

## Boundary between external and original code

The external tools provide physical mode fields or an AO residual PSD. The
original study code then performs the coordinate normalization, overlap
projection, two-arm null calculation, Monte Carlo hierarchy, variance
decomposition, radial model, and regression analysis described in
`source_review/`.

