"""Assemble the current working edition from manifest-listed lesson sources."""

import json
import os
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "System_Design_Fullstack_Masterclass.md"


def slug(title):
    return re.sub(r"[^\w -]", "", title.lower()).replace(" ", "-")


def render(source, anchor, depth, documents):
    def link(match):
        target = urlsplit(match[2])
        if target.scheme or target.netloc:
            return match[0]
        path = (source.parent / unquote(target.path)).resolve() if target.path else source
        if path in documents:
            destination = "#" + documents[path]
            if target.fragment:
                destination += "--" + target.fragment
        else:
            destination = Path(os.path.relpath(path, ROOT)).as_posix()
            if target.fragment:
                destination += "#" + target.fragment
        return f"[{match[1]}]({destination})"

    def heading(match):
        identifier = anchor if len(match[1]) == 1 else anchor + "--" + slug(match[2])
        return f'<a id="{identifier}"></a>\n\n' + "#" * (len(match[1]) + depth) + " " + match[2]

    parts = re.split(r"(^```[^\n]*\n.*?^```[^\n]*$)", source.read_text(), flags=re.M | re.S)
    for index in range(0, len(parts), 2):
        parts[index] = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, parts[index])
        parts[index] = re.sub(r"^(#{1,3}) (.+)$", heading, parts[index], flags=re.M)
    return "".join(parts).strip()


def build():
    manifest = json.loads((ROOT / "course-manifest.json").read_text())
    modules = sorted(manifest["modules"], key=lambda module: module["order"])
    ready = [lesson for lesson in manifest["lessons"]
             if lesson["status"] in {"written_pending_curriculum_mapping", "complete"}]
    if not ready:
        raise ValueError("No written lessons are available to assemble")
    documents = {}
    for lesson in ready:
        documents[(ROOT / lesson["path"]).resolve()] = lesson["id"]
        documents[(ROOT / lesson["exercise_solution_path"]).resolve()] = lesson["id"] + "--exercise-solution"

    parts = ["# Senior Full-Stack System Design Masterclass",
             f"Working edition · {len(ready)} written lesson(s) · Target: {manifest['expected_lesson_count']} lessons",
             "This partial edition contains the complete currently written lesson content and worked exercise solutions. "
             "The original curriculum has not yet been verified; lesson placement remains provisional. "
             "It is not the completed 98-lesson textbook.",
             "## Contents"]
    for module in modules:
        lessons = sorted((item for item in ready if item["module_id"] == module["id"]), key=lambda item: item["order"])
        if not lessons:
            continue
        parts.append(f"- [{module['title']}](#{module['id']})\n" + "\n".join(
            f"  - [{lesson['title']}](#{lesson['id']})" for lesson in lessons))
    for module in modules:
        lessons = sorted((item for item in ready if item["module_id"] == module["id"]), key=lambda item: item["order"])
        if not lessons:
            continue
        parts.append(f'<a id="{module["id"]}"></a>\n\n## {module["title"]}')
        for lesson in lessons:
            parts.append(render(ROOT / lesson["path"], lesson["id"], 2, documents))
            parts.append(render(ROOT / lesson["exercise_solution_path"], lesson["id"] + "--exercise-solution", 3, documents))
    return "\n\n".join(parts) + "\n"


if __name__ == "__main__":
    OUTPUT.write_text(build())
    print(f"Built {OUTPUT.name}")
