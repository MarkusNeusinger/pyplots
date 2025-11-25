"""
Smoke tests to verify basic functionality.
"""

import pytest


def test_imports():
    """Test that core packages can be imported."""
    import matplotlib
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np

    assert matplotlib is not None
    assert plt is not None
    assert pd is not None
    assert np is not None


def test_matplotlib_backend():
    """Test matplotlib can create figures without display."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 2, 3])
    plt.close(fig)


def test_sample_data_fixture(sample_data):
    """Test that sample_data fixture provides valid data."""
    assert len(sample_data) == 50
    assert 'x' in sample_data.columns
    assert 'y' in sample_data.columns
    assert 'category' in sample_data.columns
