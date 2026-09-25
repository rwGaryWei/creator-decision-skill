import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('installer', ROOT/'scripts/install.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallTests(unittest.TestCase):
    def test_install_and_run_offline_helper(self):
        with tempfile.TemporaryDirectory() as folder:
            target = installer.install(folder)
            self.assertTrue((target/'SKILL.md').is_file())
            result = subprocess.run([sys.executable, str(target/'scripts/decision.py'), 'validate',
                                     str(ROOT/'examples/game/prototype.json')], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotIn('__pycache__', [p.name for p in target.iterdir()])

    def test_existing_install_preserved(self):
        with tempfile.TemporaryDirectory() as folder:
            target = installer.install(folder)
            (target/'SKILL.md').write_text('User customization', encoding='utf-8')
            with self.assertRaises(ValueError): installer.install(folder)
            self.assertEqual((target/'SKILL.md').read_text(encoding='utf-8'), 'User customization')

    def test_missing_project_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(FileNotFoundError): installer.install(Path(folder)/'missing')
