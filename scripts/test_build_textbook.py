import json
import re
import tempfile
import unittest
from pathlib import Path

from build_textbook import ROOT, build, render


class TextbookTests(unittest.TestCase):
    def test_full_lesson_and_solution_are_preserved(self):
        lessons = [item for item in json.loads((ROOT / "course-manifest.json").read_text())["lessons"] if item['status'] == 'complete']
        book = build()

        def normalize(text):
            text = re.sub(r'^<a id="[^"]+"></a>\n\n', '', text, flags=re.M)
            text = re.sub(r'^#{1,6} ', '', text, flags=re.M)
            return re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text).strip()

        blocks = lambda text: re.findall(r'^```[^\n]*\n.*?^```[^\n]*$', text, flags=re.M | re.S)
        for index, lesson in enumerate(lessons):
            with self.subTest(lesson=lesson['id']):
                expected = "\n\n".join((ROOT / lesson[key]).read_text().strip() for key in ("path", "exercise_solution_path"))
                actual = book.split(f'<a id="{lesson["id"]}"></a>', 1)[1]
                if index + 1 < len(lessons):
                    actual = actual.split(f'<a id="{lessons[index + 1]["id"]}"></a>', 1)[0]
                actual = re.split(r'<a id="module-\d+"></a>', actual, maxsplit=1)[0]
                self.assertEqual(normalize(actual), normalize(expected))
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
