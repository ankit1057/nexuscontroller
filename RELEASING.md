# Releasing NexusController to PyPI

This guide explains how to release the NexusController package to PyPI.

## Prerequisites

1. Ensure you have an account on [PyPI](https://pypi.org/)
2. Install required tools:
   ```bash
   pip install build twine
   ```
3. Make sure you have the latest version of the code:
   ```bash
   git pull
   ```

## Build Process

1. Update version number in `nexuscontroller/__init__.py`
2. Clean up any build artifacts:
   ```bash
   rm -rf build/ dist/ *.egg-info/
   ```
3. Build the package:
   ```bash
   python -m build
   ```
   This will create both source distribution (`.tar.gz`) and wheel (`.whl`) files in the `dist/` directory.

## Test the Build

1. Install the package locally to test:
   ```bash
   pip install dist/nexuscontroller-*.whl
   ```
2. Run basic tests to ensure the package works:
   ```bash
   python -c "from nexuscontroller import AndroidController; print(AndroidController.__doc__)"
   ```

## Upload to PyPI

1. First, upload to Test PyPI to verify everything works:
   ```bash
   python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
   ```
2. Install from Test PyPI to verify:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ nexuscontroller
   ```
3. If everything looks good, upload to the real PyPI:
   ```bash
   python -m twine upload dist/*
   ```

## After Release

1. Create a new git tag for the release:
   ```bash
   git tag -a v1.0.0 -m "Version 1.0.0 release"
   git push origin v1.0.0
   ```
2. Update the README.md with the latest version and features
3. Create a GitHub release with release notes

## Troubleshooting

### Common Issues

1. **Package name already exists**
   - Check if the package name is available on PyPI
   - You may need to rename the package

2. **Invalid classifiers**
   - Ensure all classifiers in `setup.py` are valid according to PyPI

3. **Missing dependencies**
   - Verify all dependencies are correctly listed in `pyproject.toml`

4. **Authentication failure**
   - Use a PyPI API token instead of password
   - Set up a `~/.pypirc` file with your credentials

### Using API Tokens

For secure uploads, use API tokens instead of passwords:

1. Generate a token on PyPI website (Account Settings > API tokens)
2. Use the token as your password with twine
3. Or add to your `~/.pypirc` file:
   ```
   [pypi]
   username = __token__
   password = pypi-xxxxx...
   ```

## Continuous Integration

To automate releases using GitHub Actions:

1. Create a `.github/workflows/publish.yml` file
2. Store PyPI API token as a GitHub secret
3. Configure the workflow to build and publish on new tags or releases 