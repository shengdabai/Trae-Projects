import contextlib
import importlib.util
import io
import os
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch, mock_open


class SecurityReportTests(unittest.TestCase):
    def setUp(self):
        path = Path(__file__).resolve().parents[1] / 'Claude Code/api配置/api_security_verification.py'
        spec = importlib.util.spec_from_file_location('verification', path)
        module = importlib.util.module_from_spec(spec)
        # No local credential files are loaded by this test.
        with patch.dict(sys.modules, {'dotenv': types.SimpleNamespace(load_dotenv=lambda *args: None)}):
            spec.loader.exec_module(module)
        self.module = module

    def test_report_never_prints_key_fragments(self):
        module = self.module
        key = 'synthetic-sensitive-value-1234567890'
        output = io.StringIO()
        with patch.dict(os.environ, {'KIMI_API_KEY': key}, clear=True), \
                patch.object(module.os.path, 'exists', return_value=True), \
                patch.object(module.subprocess, 'run', return_value=types.SimpleNamespace(returncode=0)), \
                contextlib.redirect_stdout(output):
            module.check_env_file_security()
        self.assertIn('KIMI_API_KEY', output.getvalue())
        self.assertNotIn(key[:10], output.getvalue())
        self.assertNotIn(key[-4:], output.getvalue())
        output = io.StringIO()
        with patch.object(module.os.path, 'exists', return_value=True), \
                patch('builtins.open', mock_open(read_data=f'api_key = "{key}"\n')), \
                contextlib.redirect_stdout(output):
            self.assertFalse(module.check_code_security())
        self.assertIn('test_openai.py:1:', output.getvalue())
        self.assertNotIn(key[:20], output.getvalue())

    def test_tracked_or_unignored_file_fails_without_loading_credentials(self):
        for exit_code in (1, 128):
            with self.subTest(exit_code=exit_code), \
                    patch.object(self.module.os.path, 'exists', return_value=True), \
                    patch.object(self.module.subprocess, 'run', return_value=types.SimpleNamespace(returncode=exit_code)), \
                    patch.object(self.module, 'load_dotenv') as load, \
                    contextlib.redirect_stdout(io.StringIO()):
                self.assertFalse(self.module.check_env_file_security())
                load.assert_not_called()

    def test_git_ignore_check_honors_negations_and_tracked_files(self):
        import subprocess
        import tempfile
        with tempfile.TemporaryDirectory(prefix='ignore-check-') as temp:
            subprocess.run(['git', 'init', '-q', temp], check=True)
            marker = Path(temp) / 'sample.txt'
            marker.write_text('non-sensitive test fixture')
            rules = Path(temp) / '.gitignore'
            for rule, expected in [('sample.txt\n', 0), ('sample.txt\n!sample.txt\n', 1)]:
                rules.write_text(rule)
                result = subprocess.run(['git', '-C', temp, 'check-ignore', '--quiet', '--', marker.name])
                self.assertEqual(result.returncode, expected)
            subprocess.run(['git', '-C', temp, 'add', 'sample.txt'], check=True)
            rules.write_text('sample.txt\n')
            result = subprocess.run(['git', '-C', temp, 'check-ignore', '--quiet', '--', marker.name])
            self.assertEqual(result.returncode, 1)


if __name__ == '__main__':
    unittest.main()
