# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [2.1.0] - 2025-04-09

### Added

- Python 3.11 is now supported

### Changed

- CICD: Switch from Black to the Ruff Formatter
- CICD: Update checkout action to v4
- Update to pycddlib 3.0 API

### Removed

- Python 3.7 is not supported any more

## [2.0.0] - 2024-01-09

### Added

- PDLP solver interface

### Changed

- Rename optional deps for open source solvers

### Removed

- ProxQP: Unused ``initvals`` argument in interface
- Remove top-level ``__init__.py``

## [1.2.0] - 2023-10-23

### Added

- Continuous integration: ruff
- ProxQP (LP variant) solver interface

### Changed

- Bumped pycddlib dependency to 2.1.7
- The ``solver`` keyword argument is now mandatory

## [1.1.0] - 2022-03-17

### Changed

- Relicense the project to LPGL-3.0

### Fixed

- Add CVXPY to test environment

## [1.0.1] - 2022-03-16

### Added

- Links and keywords to project description for PyPI

### Fixed

- Add license to project config

## [1.0.0] - 2022-03-16

### Added

- CVXPY solver interface
- Type annotations

### Fixed

- Remove dependency on quadprog

## [0.9.0] - 2022-03-07

### Added

- Documentation
- GitHub CI actions
- Start this changelog
- Unit tests

### Changed

- Function now raises ``SolverNotFound`` when the solver is not available
- Improve code coverage to 84%
- Improve linter code rating to 10/10
- Switch from ``setup.py`` to ``pyproject.toml``

[unreleased]: https://github.com/qpsolvers/qpsolvers/compare/v2.1.0...HEAD
[2.1.0]: https://github.com/qpsolvers/qpsolvers/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/qpsolvers/qpsolvers/compare/v1.2.0...v2.0.0
[1.2.0]: https://github.com/qpsolvers/qpsolvers/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/qpsolvers/qpsolvers/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/qpsolvers/qpsolvers/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/qpsolvers/qpsolvers/compare/v0.9.0...v1.0.0
[0.9.0]: https://github.com/qpsolvers/qpsolvers/releases/tag/v0.9.0
