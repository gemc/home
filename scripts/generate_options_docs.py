#!/usr/bin/env python3

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path


ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
ENTRY_RE = re.compile(r"^\s*-(?P<name>[A-Za-z0-9_]+)(?:=(?P<shape><[^>]+>))?\s*\.{1,}\s*:\s*(?P<desc>.*)$")


def run_command(command):
    completed = subprocess.run(
        command,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    output = strip_ansi(completed.stdout)

    if completed.returncode != 0:
        print(f"Command failed: {' '.join(command)}", file=sys.stderr)
        print(output, file=sys.stderr)
        raise SystemExit(completed.returncode)

    return output


def strip_ansi(text):
    return ANSI_RE.sub("", text)


def slugify(name):
    slug = re.sub(r"[^A-Za-z0-9_-]+", "-", name).strip("-").lower()
    if not slug:
        raise ValueError(f"Cannot make slug from option name: {name!r}")
    return slug


def find_gemc(explicit_path):
    if explicit_path:
        gemc = Path(explicit_path)
        if gemc.exists():
            return gemc
        print(f"GEMC executable not found: {gemc}", file=sys.stderr)
        raise SystemExit(1)

    candidates = []
    path_gemc = shutil.which("gemc")
    if path_gemc:
        candidates.append(Path(path_gemc))

    candidates.extend(
        [
            Path("../src/build/gemc"),
            Path("build/gemc"),
        ]
    )

    for candidate in candidates:
        if candidate.exists():
            return candidate

    print("GEMC executable not found.", file=sys.stderr)
    print("Use --gemc /path/to/gemc, or build GEMC so ../src/build/gemc exists.", file=sys.stderr)
    raise SystemExit(1)


def parse_help_listing(help_text):
    entries = []
    section = None

    for line in help_text.splitlines():
        stripped = line.strip()

        if stripped == "Switches:":
            section = "switch"
            continue

        if stripped == "Options:":
            section = "option"
            continue

        if stripped == "Help / Search / Introspection:":
            section = None
            continue

        if section is None:
            continue

        match = ENTRY_RE.match(line)
        if not match:
            continue

        entries.append(
            {
                "kind": section,
                "name": match.group("name"),
                "shape": match.group("shape") or "",
                "description": match.group("desc").strip(),
            }
        )

    return entries


def markdown_escape_table_cell(text):
    return text.replace("|", "\\|").replace("\n", " ")


def page_front_matter(title):
    escaped_title = title.replace("'", "''")
    return f"---\nlayout: default\ntitle: '{escaped_title}'\n---\n\n"


def write_detail_page(path, entry, detail_text):
    title = f"GEMC option: {entry['name']}"
    command = f"gemc help {entry['name']}"

    body = [
        page_front_matter(title),
        f"# `{entry['name']}`\n\n",
        f"Type: `{entry['kind']}`\n\n",
        f"Description: {entry['description']}\n\n",
        f"Generated from:\n\n```sh\n{command}\n```\n\n",
        "```text\n",
        detail_text.strip(),
        "\n```\n",
    ]

    path.write_text("".join(body), encoding="utf-8")


def write_index(path, entries, detail_dir_name, base_link):
    lines = [
        page_front_matter("GEMC Options Reference"),
        "# GEMC Options Reference\n\n",
        "This page is generated from `gemc -h`. Click each item for help.<br/><br/>\n\n",
    ]

    for kind, heading in (("switch", "Switches"), ("option", "Options")):
        group = [entry for entry in entries if entry["kind"] == kind]
        if not group:
            continue

        lines.extend(
            [
                f"## {heading}\n\n",
            ]
        )
        if kind == "switch":
            lines.extend(
                [
                    "| Name | Description |\n",
                    "| --- | --- |\n",
                ]
            )
        else:
            lines.extend(
                [
                    "| Name | Shape | Description |\n",
                    "| --- | --- | --- |\n",
                ]
            )

        for entry in group:
            slug = slugify(entry["name"])
            link = f"{base_link}/{detail_dir_name}/{slug}"
            shape = entry["shape"] or ""
            name_link = f"[`{entry['name']}`]({link})"
            description = markdown_escape_table_cell(entry["description"])
            if kind == "switch":
                lines.append(f"| {name_link}<br/> | {description} |\n")
            else:
                lines.append(
                    "| "
                    f"{name_link}"
                    " | "
                    f"`{markdown_escape_table_cell(shape)}`"
                    " | "
                    f"{description}"
                    " |\n"
                )

        lines.append("\n")

    path.write_text("".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Generate GEMC option reference Markdown from gemc -h and gemc help <option>."
    )
    parser.add_argument("--gemc", help="Path to the gemc executable. Defaults to PATH, then ../src/build/gemc.")
    parser.add_argument(
        "--index",
        default="_documentation/api/options_reference.md",
        help="Markdown file to write for the generated index.",
    )
    parser.add_argument(
        "--details-dir",
        default="_documentation/api/options",
        help="Directory for one generated detail page per option.",
    )
    parser.add_argument(
        "--base-link",
        default="/home/documentation/api",
        help="Base URL used for links in the generated index.",
    )

    args = parser.parse_args()

    gemc = find_gemc(args.gemc)

    index_path = Path(args.index)
    details_dir = Path(args.details_dir)
    details_dir.mkdir(parents=True, exist_ok=True)
    index_path.parent.mkdir(parents=True, exist_ok=True)

    listing = run_command([str(gemc), "-h"])
    entries = parse_help_listing(listing)

    if not entries:
        print("No options found in gemc -h output.", file=sys.stderr)
        raise SystemExit(1)

    for entry in entries:
        detail_text = run_command([str(gemc), "help", entry["name"]])
        detail_path = details_dir / f"{slugify(entry['name'])}.md"
        write_detail_page(detail_path, entry, detail_text)
        print(f"Wrote {detail_path}")

    write_index(index_path, entries, details_dir.name, args.base_link)
    print(f"Wrote {index_path}")


if __name__ == "__main__":
    main()
