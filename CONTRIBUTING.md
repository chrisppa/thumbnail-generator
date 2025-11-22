# Contributing to thumbnail-generator

Thanks for your interest in improving the project! This document explains how to propose changes and get involved.

## Code of conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md). By participating you agree to abide by its guidelines.

## Getting started

1. Fork the repository and create a branch from `main`.
2. Set up a virtual environment with Python 3.9+
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -e .[dev,vips,video]
   ```
3. Run the quick checks:
   ```bash
   python -m thumbnail_generator.cli --help
   pytest
   ```

## Making changes

- Keep pull requests focused. If you plan a big change, open an issue first to discuss the approach.
- Follow the existing code style (PEP 8). Use Ruff (`ruff check`) for linting and `pytest` for tests.
- Add or update tests when fixing bugs or adding features. Include fixtures for new remote URLs when practical.
- Document user-facing changes in the README.

## Commit messages

Use conventional prefixes when practical:
- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation changes
- `chore:` maintenance, tooling, meta

## Pull requests

1. Rebase your branch on the latest `main`.
2. Confirm `pytest` passes and the CLI works locally.
3. Update the changelog/README if behavior changed. Mention any new dependencies.
4. Submit the PR with a clear description of the change and link to related issues.

## Releasing

Maintainers ship releases with:
```bash
hatch version <part>
hatch build
hatch publish
```
Ensure the version bump commits are included and tags are pushed (`git push origin vX.Y.Z`).

## Questions?

Open a GitHub issue or reach out via crisppy.codes+support@gmail.com.
