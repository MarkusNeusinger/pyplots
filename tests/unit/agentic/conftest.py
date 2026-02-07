"""Fixtures for agentic module tests."""

import os
import sys


# Add the modules directory to sys.path so tests can import agent, state, etc.
# This mirrors what the workflow scripts do at runtime.
MODULES_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "agentic", "workflows", "modules")
sys.path.insert(0, os.path.abspath(MODULES_DIR))
