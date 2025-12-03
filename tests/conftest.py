"""Pytest configuration and shared fixtures."""

import pytest
from pathlib import Path
import tempfile
import shutil


@pytest.fixture(scope="session")
def test_data_dir():
    """Create a temporary directory for test data."""
    temp_dir = tempfile.mkdtemp(prefix="agri_toolkit_test_")
    yield Path(temp_dir)
    # Cleanup after all tests
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture(scope="function")
def clean_test_dir(tmp_path):
    """Provide a clean temporary directory for each test."""
    yield tmp_path
    # Cleanup happens automatically with tmp_path
