"""Run all Module 1 checks; PostgreSQL tests announce a skip without an explicit DSN."""
import sys
import unittest
from pathlib import Path

root=Path(__file__).resolve().parent
sys.path.insert(0,str(root))
folders=sorted(path for path in root.iterdir() if path.is_dir() and path.name[:2].isdigit())
for folder in folders: sys.path.insert(0,str(folder))
suite=unittest.TestSuite()
for folder in folders: suite.addTests(unittest.TestLoader().discover(str(folder),pattern='test_*.py',top_level_dir=str(folder)))
result=unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
