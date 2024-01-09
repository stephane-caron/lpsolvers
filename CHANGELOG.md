# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added

- PDLP solver interface

### Changed

- Rename optional deps for open source solvers

### Removed

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

[unreleased]: https://github.com/qpsolvers/qpsolvers/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/qpsolvers/qpsolvers/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/qpsolvers/qpsolvers/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/qpsolvers/qpsolvers/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/qpsolvers/qpsolvers/compare/v0.9.0...v1.0.0
[0.9.0]: https://github.com/qpsolvers/qpsolvers/releases/tag/v0.9.0
