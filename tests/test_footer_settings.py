"""Tests for footer effect handling in settings updates."""

import ast
from pathlib import Path
import unittest


class TestFooterSettings(unittest.TestCase):
    """Settings changes should not leave dangling footer effects."""

    def test_apply_settings_stops_animation_before_replacing_footer_style(self):
        source = Path("bongo_cat/ui/main_window.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        apply_settings = next(
            node for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef) and node.name == "apply_settings"
        )

        call_lines = {}
        for node in ast.walk(apply_settings):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            if isinstance(func, ast.Attribute):
                if func.attr == "setup_footer_style":
                    call_lines["style"] = node.lineno
                elif func.attr == "stop" and isinstance(func.value, ast.Attribute):
                    if func.value.attr == "footer_animation":
                        call_lines["stop"] = node.lineno

        self.assertLess(call_lines["stop"], call_lines["style"])


if __name__ == "__main__":
    unittest.main()
