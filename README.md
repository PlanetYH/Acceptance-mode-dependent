# NCPA-to-null leakage: non-executable source-review snapshot

This archive accompanies the submitted manuscript **“Acceptance-mode-dependent
transfer of non-common-path aberrations to null leakage in mid-infrared nulling
interferometry.”**

## Purpose and scope

It is provided only to make the mathematical and statistical implementation legible during editorial and
peer review. The files document:

- free-space and single-mode raw-null propagation;
- non-common-path-aberration (NCPA) and adaptive-optics (AO) phase-screen logic;
- the nested NCPA/AO Monte Carlo hierarchy;
- decomposition of structural and AO-driven variance;
- the radial-only polynomial model and its coefficient of determination;
- the adjusted radial-content association and independent-library slopes.

`MANUSCRIPT_CODE_MAP.md` maps each manuscript figure to the relevant static
source excerpt. `EXTERNAL_SOFTWARE_INTERFACES.md` documents the external
software interfaces used in the full study without distributing the external
implementations.

## Deliberate exclusions

This snapshot does **not** contain:

- simulation data, random libraries, phase screens, cached mode fields, or
  numerical results;
- manuscript figure files or plotting data;
- MAOPPY, ofiber, modesolverpy, or any other third-party source code;
- an environment definition, dependency lock file, installation instructions,
  download links, or executable third-party interfaces;
- command-line entry points, `main` functions, pipeline orchestration,
  checkpointing, parallel execution, file readers/writers, or figure exporters;
- a complete reproduction workflow.

The Python files under `source_review/` are therefore not a runnable software
package. Calls that require omitted inputs or external solvers are represented
only by documented interface contracts and raise `NotImplementedError`.

## Availability status

This pre-acceptance archive supports inspection of the reported methods; it is
not presented as a reproducibility release. The complete versioned code, input
data, numerical outputs, and reproduction workflow are retained by the authors
and are intended for a separate post-acceptance release, subject to the final
journal and institutional requirements.



