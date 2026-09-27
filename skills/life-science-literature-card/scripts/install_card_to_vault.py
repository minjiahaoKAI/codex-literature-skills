#!/usr/bin/env python3
"""Install a staged literature card and its assets into an Obsidian vault."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import struct
import uuid
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path, PurePosixPath


def relative_folder(value: str) -> Path:
    normalized = value.replace("\\", "/")
    parts = PurePosixPath(normalized).parts
    if not parts or any(part in {"", ".", ".."} for part in parts) or ":" in normalized:
        raise ValueError(f"Folder must be a safe vault-relative path: {value}")
    if normalized.startswith("/"):
        raise ValueError(f"Folder must be vault-relative: {value}")
    return Path(*parts)


def read_png_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        header = handle.read(24)
    if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError("Graphical abstract is not a valid PNG header")
    return struct.unpack(">II", header[16:24])


def require_file(path: Path, label: str) -> Path:
    if not path.is_file() or path.stat().st_size == 0:
        raise ValueError(f"{label} is missing or empty: {path}")
    return path.resolve()


def run(args: argparse.Namespace) -> dict[str, object]:
    vault = args.vault.resolve()
    if not vault.is_dir() or not (vault / ".obsidian").is_dir():
        raise ValueError(f"Not an opened Obsidian vault (missing .obsidian): {vault}")

    note = require_file(args.note, "Note")
    png = require_file(args.graphical_abstract, "Graphical abstract")
    svg = require_file(args.logic_map, "Logic map")
    mineru = args.mineru_directory.resolve()
    if not mineru.is_dir():
        raise ValueError(f"MinerU directory is missing: {mineru}")
    if note.suffix.lower() != ".md" or png.suffix.lower() != ".png" or svg.suffix.lower() != ".svg":
        raise ValueError("Expected .md note, .png graphical abstract, and .svg logic map")
    if not mineru.name or mineru.name in {".", ".."}:
        raise ValueError("MinerU directory must end in a Zotero key")

    notes_folder = relative_folder(args.notes_folder)
    assets_folder = relative_folder(args.assets_folder)
    sources_folder = relative_folder(args.sources_folder)
    note_text = note.read_text(encoding="utf-8")
    svg_text = svg.read_text(encoding="utf-8")
    if "\ufffd" in note_text or "\ufffd" in svg_text:
        raise ValueError("Note or SVG contains a Unicode replacement character")
    for field in (
        "note_type: literature-card", "card_cover:", "card_summary:",
        "card_logic_map:", "source_status:", "mineru_mode:",
        "zotero_key:", "pdf_key:", "cssclasses:",
    ):
        if field not in note_text:
            raise ValueError(f"Required note field is missing: {field}")
    asset_prefix = assets_folder.as_posix()
    for filename in (png.name, svg.name):
        if f"[[{asset_prefix}/{filename}" not in note_text:
            raise ValueError(f"Note does not link the staged asset: {asset_prefix}/{filename}")
    ET.fromstring(svg_text)
    width, height = read_png_dimensions(png)
    if width < 100 or height < 100:
        raise ValueError(f"PNG dimensions are implausibly small: {width}x{height}")

    mineru_files = [p for p in mineru.rglob("*") if p.is_file()]
    if not any(p.suffix.lower() == ".md" and p.stat().st_size for p in mineru_files):
        raise ValueError("MinerU directory contains no readable Markdown output")

    targets = [
        vault / notes_folder / note.name,
        vault / assets_folder / png.name,
        vault / assets_folder / svg.name,
        vault / sources_folder / mineru.name,
    ]
    if any(not target.resolve().is_relative_to(vault) for target in targets):
        raise ValueError("A target would leave the selected vault")
    if any(target.exists() for target in targets):
        raise FileExistsError("A final target already exists; use versioned names or review the existing card")
    if args.dry_run:
        return {"status": "ready", "targets": [str(p) for p in targets], "mineru_files": len(mineru_files)}

    temporary: list[Path] = []
    created: list[Path] = []
    try:
        for source, target in zip((note, png, svg, mineru), targets):
            target.parent.mkdir(parents=True, exist_ok=True)
            temp = target.with_name(target.name + ".codex-tmp-" + uuid.uuid4().hex)
            if not temp.resolve().is_relative_to(vault):
                raise ValueError("A temporary target would leave the selected vault")
            temporary.append(temp)
            if source.is_dir():
                shutil.copytree(source, temp)
                if len([p for p in temp.rglob("*") if p.is_file()]) != len(mineru_files):
                    raise RuntimeError("MinerU file count changed during copy")
            else:
                shutil.copy2(source, temp)
                if temp.stat().st_size != source.stat().st_size:
                    raise RuntimeError("Staged asset byte count changed during copy")
        for temp, target in zip(temporary, targets):
            temp.rename(target)
            created.append(target)
        timestamp = datetime.now().timestamp()
        for target in targets[:3]:
            os.utime(target, (timestamp, timestamp))
        return {
            "status": "filesystem_installed",
            "note": str(targets[0]),
            "graphical_abstract": str(targets[1]),
            "logic_map": str(targets[2]),
            "mineru_directory": str(targets[3]),
            "mineru_files": len(mineru_files),
            "visual_render_verification": "required_in_obsidian",
        }
    except Exception:
        for path in temporary + created:
            if not path.resolve().is_relative_to(vault):
                raise RuntimeError("Refusing cleanup outside the selected vault")
            if path.is_dir():
                shutil.rmtree(path)
            elif path.exists():
                path.unlink()
        raise


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault", required=True, type=Path)
    parser.add_argument("--note", required=True, type=Path)
    parser.add_argument("--graphical-abstract", required=True, type=Path)
    parser.add_argument("--logic-map", required=True, type=Path)
    parser.add_argument("--mineru-directory", required=True, type=Path)
    parser.add_argument("--notes-folder", default="���ױʼ�")
    parser.add_argument("--assets-folder", default="ͼƬ��Դ/literature_cards")
    parser.add_argument("--sources-folder", default="sources/mineru")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    print(json.dumps(run(args), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
