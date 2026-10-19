#!/usr/bin/env python3
"""Validate a five-image App Store gallery manifest."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = ("slug", "feature", "title", "body", "src", "bg", "ink", "accent", "footer")
HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")


def load_images(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        images = data.get("images")
        if isinstance(images, list):
            return images
        for value in data.values():
            if isinstance(value, list) and value and all(isinstance(item, dict) for item in value):
                return value
    raise ValueError("Expected an array of images or an object containing an images array")


def validate(images: list[dict[str, Any]]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if len(images) != 5:
        errors.append(f"gallery must contain exactly 5 images, found {len(images)}")

    slugs: list[str] = []
    sources: list[str] = []

    for index, image in enumerate(images, start=1):
        label = f"image {index:02d}"
        if not isinstance(image, dict):
            errors.append(f"{label}: must be an object")
            continue

        missing = [field for field in REQUIRED_FIELDS if field not in image]
        if missing:
            errors.append(f"{label}: missing fields: {', '.join(missing)}")

        slug = str(image.get("slug", ""))
        if slug:
            slugs.append(slug)
            expected = f"{index:02d}-"
            if not slug.startswith(expected):
                warnings.append(f"{label}: slug should start with '{expected}'")

        title = image.get("title")
        if not isinstance(title, list) or len(title) != 2 or not all(str(line).strip() for line in title):
            errors.append(f"{label}: title must be exactly two non-empty lines")

        body = image.get("body")
        if not isinstance(body, list) or len(body) != 2 or not all(str(line).strip() for line in body):
            errors.append(f"{label}: body must be exactly two non-empty lines")

        src = str(image.get("src", "")).strip()
        if src:
            sources.append(src)

        for field in ("bg", "ink", "accent"):
            value = str(image.get(field, "")).strip()
            if not HEX_RE.match(value):
                errors.append(f"{label}: {field} must be a 6-digit hex color such as #F7F4ED")

        if not str(image.get("feature", "")).strip():
            errors.append(f"{label}: feature/eyebrow is empty")
        if not str(image.get("footer", "")).strip():
            errors.append(f"{label}: footer is empty")

    if len(slugs) != len(set(slugs)):
        errors.append("gallery contains duplicate slugs")
    if len(sources) != len(set(sources)):
        errors.append("gallery reuses the same screenshot source")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json_file", type=Path, help="Gallery JSON file, or - for stdin")
    parser.add_argument("--pretty", action="store_true", help="Print a human-readable summary")
    args = parser.parse_args()

    raw = sys.stdin.read() if str(args.json_file) == "-" else args.json_file.read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
        images = load_images(data)
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"Invalid gallery manifest: {exc}", file=sys.stderr)
        return 2

    errors, warnings = validate(images)
    result = {"ok": not errors, "count": len(images), "errors": errors, "warnings": warnings}

    if args.pretty:
        print(f"images: {len(images)}")
        for warning in warnings:
            print(f"WARN: {warning}")
        for error in errors:
            print(f"ERROR: {error}")
        if not errors:
            print("gallery is valid")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
