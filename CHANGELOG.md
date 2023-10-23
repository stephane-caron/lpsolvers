# Changelog

All notable changes to this project will be documented in this file.

## Unreleased

### Added

- Continuous integration: ruff
- ProxQP (LP variant) solver interface

### Changed

- Bumped pycddlib dependency to 2.1.7

## [1.1.0] - 2022/03/17

### Changed

- Relicense the project to LPGL-3.0

### Fixed

- Add CVXPY to test environment

## [1.0.1] - 2022/03/16

### Added

- Links and keywords to project description for PyPI

### Fixed

- Add license to project config

## [1.0.0] - 2022/03/16

### Added

- CVXPY solver interface
- Type annotations

### Fixed

- Remove dependency on quadprog

## [0.9.0] - 2022/03/07

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
