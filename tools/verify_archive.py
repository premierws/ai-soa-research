"""Verify the research archive without changing source projects."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "metadata/archive_manifest.json").read_text())
    errors: list[str] = []
    for item in manifest["files"]:
        path = root / item["path"]
        if not path.is_file():
            errors.append(f"missing file: {item['path']}")
            continue
        data = path.read_bytes()
        if len(data) != item["bytes"]:
            errors.append(f"size mismatch: {item['path']}")
        if hashlib.sha256(data).hexdigest() != item["sha256"]:
            errors.append(f"hash mismatch: {item['path']}")
    sources = json.loads((root / "metadata/source_manifest.json").read_text())
    for item in sources["files"]:
        if hashlib.sha256((root / item["path"]).read_bytes()).hexdigest() != item["sha256"]:
            errors.append(f"source snapshot mismatch: {item['path']}")
    report = (root / "docs/research_report_2026-11-12.md").read_text()
    if len(re.findall(r"^## ", report, re.MULTILINE)) != 20:
        errors.append("report section count mismatch")
    for marker in ("开放受约束的目标组合能力", "goal-thermal", "SubmitMission(MissionRequest)", "附录 B"):
        if marker not in report:
            errors.append(f"report marker missing: {marker}")
    examples = [json.loads(text) for text in re.findall(r"```json\n(.*?)\n```", report, re.DOTALL)]
    for name, expected in zip(("mission_request.json", "mission_receipt.json"), examples, strict=True):
        if json.loads((root / "examples" / name).read_text()) != expected:
            errors.append(f"JSON example mismatch: {name}")
    proto = re.search(r"```protobuf\n(.*?)\n```", report, re.DOTALL)
    if proto is None or (root / "examples/mission_contract.example.proto").read_text().strip() != proto[1].strip():
        errors.append("Proto example mismatch")
    # Check links in archive-authored entry points; source snapshots retain original links.
    docs = [root / "README.md", root / "examples/README.md"]
    docs += [root / "docs" / name for name in ("key_conclusions.md", "research_notes.md", "open_questions.md")]
    docs += [root / "references/source_catalog.md", root / "evidence/evidence_matrix.md", root / "evidence/source_excerpts.md"]
    link_count = 0
    for doc in docs:
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", doc.read_text()):
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
                continue
            relative = target.split("#", 1)[0]
            if not (doc.parent / relative).exists():
                errors.append(f"broken link in {doc.relative_to(root)}: {target}")
            link_count += 1
    result = {
        "status": "passed" if not errors else "failed",
        "manifest_files_checked": len(manifest["files"]),
        "source_snapshots_checked": len(sources["files"]),
        "local_links_checked": link_count,
        "report_sections": 20,
        "examples_compared_to_report": 3,
        "scope": "归档完整性检查，不是软件功能或实车验证",
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    (root / "metadata/verification_result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
