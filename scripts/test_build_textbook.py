import json
import re
import tempfile
import unittest
from pathlib import Path

from build_textbook import ROOT, build, render


class TextbookTests(unittest.TestCase):
    def test_full_lesson_and_solution_are_preserved(self):
        lesson = json.loads((ROOT / "course-manifest.json").read_text())["lessons"][0]
        expected = "\n\n".join((ROOT / lesson[key]).read_text().strip()
                                 for key in ("path", "exercise_solution_path"))
        actual = build().split(f'<a id="{lesson["id"]}"></a>', 1)[1]

        def normalize(text):
            text = re.sub(r'^<a id="[^"]+"></a>\n\n', '', text, flags=re.M)
            text = re.sub(r'^#{1,6} ', '', text, flags=re.M)
            return re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text).strip()

        self.assertEqual(normalize(actual), normalize(expected))
        blocks = lambda text: re.findall(r'^```[^\n]*\n.*?^```[^\n]*$', text, flags=re.M | re.S)
        self.assertEqual(blocks(actual), blocks(expected))

    def test_rebases_navigation_without_rewriting_code(self):
        code = '```python\n# Keep heading\n[code](#unchanged)\n```'
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "example.md"
            source.write_text('# Example\n\n[Jump](#detail)\n\n## Detail\n\n'
                              '[Docs](https://example.com/a#b)\n\n' + code)
            result = render(source, "example", 2, {source: "example"})
        self.assertIn('[Jump](#example--detail)', result)
        self.assertIn('<a id="example--detail"></a>\n\n#### Detail', result)
        self.assertIn('[Docs](https://example.com/a#b)', result)
        self.assertIn(code, result)


if __name__ == "__main__":
    unittest.main()
