"""Smoke tests for report generator."""

from agents.report_generator import REPORTS_DIR


def test_reports_dir_path():
    assert str(REPORTS_DIR).endswith("reports")
