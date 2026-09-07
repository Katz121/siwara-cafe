"""Canonical validation entry point for the current design."""
from pathlib import Path
import runpy

if __name__ == '__main__':
    runpy.run_path(str(Path(__file__).with_name('validate_redesign.py')), run_name='__main__')
