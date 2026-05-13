#!/usr/bin/env python3

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


API_BASE = "https://api.github.com"


def github_get(url, token=None):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "gemc-jekyll-milestone-fetcher",
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(request) as response:
            body = response.read().decode("utf-8")
            data = json.loads(body)
            link = response.headers.get("Link")
            return data, link

    except urllib.error.HTTPError as error:
        message = error.read().decode("utf-8", errors="replace")
        print(f"GitHub API request failed: {url}", file=sys.stderr)
        print(f"HTTP {error.code}: {message}", file=sys.stderr)
        raise


def parse_next_link(link_header):
    if not link_header:
        return None

    parts = link_header.split(",")

    for part in parts:
        section = part.strip().split(";")
        if len(section) < 2:
            continue

        url_part = section[0].strip()
        rel_part = section[1].strip()

        if rel_part == 'rel="next"':
            return url_part.strip("<>")

    return None


def github_get_paginated(url, token=None):
    items = []
    next_url = url

    while next_url:
        data, link = github_get(next_url, token=token)

        if not isinstance(data, list):
            raise RuntimeError(f"Expected list response from {next_url}")

        items.extend(data)
        next_url = parse_next_link(link)

    return items


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as output:
        json.dump(data, output, indent=2, sort_keys=True)
        output.write("\n")

    print(f"Wrote {path}")


def main():
    parser = argparse.ArgumentParser(
        description="Fetch a GitHub milestone and its issues for Jekyll _data."
    )

    parser.add_argument("--owner", default="gemc")
    parser.add_argument("--repo", default="src")
    parser.add_argument("--milestone", type=int, default=1)
    parser.add_argument("--output-dir", default="_data/github")

    args = parser.parse_args()

    token = (
        os.environ.get("GITHUB_TOKEN")
        or os.environ.get("GH_TOKEN")
    )

    owner = urllib.parse.quote(args.owner)
    repo = urllib.parse.quote(args.repo)
    milestone = args.milestone

    output_dir = Path(args.output_dir)

    milestone_url = (
        f"{API_BASE}/repos/{owner}/{repo}/milestones/{milestone}"
    )

    issues_url = (
        f"{API_BASE}/repos/{owner}/{repo}/issues?"
        f"milestone={milestone}&state=all&per_page=100"
    )

    milestone_data, _ = github_get(milestone_url, token=token)
    issues_data = github_get_paginated(issues_url, token=token)

    write_json(output_dir / f"milestone_{milestone}.json", milestone_data)
    write_json(output_dir / f"milestone_{milestone}_issues.json", issues_data)


if __name__ == "__main__":
    main()