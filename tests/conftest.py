"""
Pytest configuration and fixtures for pyplots tests.
"""

import pytest
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for CI


@pytest.fixture
def sample_data():
    """Provide sample data for plot tests."""
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    return pd.DataFrame({
        'x': np.random.randn(50),
        'y': np.random.randn(50),
        'category': np.random.choice(['A', 'B', 'C'], 50),
        'size': np.random.uniform(10, 100, 50)
    })


@pytest.fixture
def temp_output_dir(tmp_path):
    """Provide a temporary directory for plot outputs."""
    output_dir = tmp_path / "plot_outputs"
    output_dir.mkdir()
    return output_dir
