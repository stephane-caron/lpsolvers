# Changelog

All notable changes to this project will be documented in this file.

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
