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
    parser.add_argument(
        "--repo-milestone",
        action="append",
        default=[],
        metavar="REPO:MILESTONE",
        help=(
            "Additional repo and milestone to fetch. REPO may be a short repo name "
            "using --owner, or owner/repo. Can be repeated."
        ),
    )
    parser.add_argument("--output-dir", default="_data/github")

    args = parser.parse_args()

    token = (
        os.environ.get("GITHUB_TOKEN")
        or os.environ.get("GH_TOKEN")
    )

    output_dir = Path(args.output_dir)

    targets = [(args.owner, args.repo, args.milestone)]
    targets.extend(parse_repo_milestone(value, args.owner) for value in args.repo_milestone)

    for owner, repo, milestone in targets:
        fetch_and_write_milestone(owner, repo, milestone, output_dir, token)


def parse_repo_milestone(value, default_owner):
    if ":" not in value:
        raise SystemExit("--repo-milestone must use REPO:MILESTONE, for example pygemc:1")

    repo_part, milestone_part = value.rsplit(":", 1)
    if "/" in repo_part:
        owner, repo = repo_part.split("/", 1)
    else:
        owner, repo = default_owner, repo_part

    try:
        milestone = int(milestone_part)
    except ValueError as error:
        raise SystemExit(f"Invalid milestone number in --repo-milestone {value!r}") from error

    return owner, repo, milestone


def fetch_and_write_milestone(owner, repo, milestone, output_dir, token):
    api_owner = urllib.parse.quote(owner)
    api_repo = urllib.parse.quote(repo)

    milestone_url = (
        f"{API_BASE}/repos/{api_owner}/{api_repo}/milestones/{milestone}"
    )

    issues_url = (
        f"{API_BASE}/repos/{api_owner}/{api_repo}/issues?"
        f"milestone={milestone}&state=all&per_page=100"
    )

    print(f"Fetching {owner}/{repo} milestone {milestone}")

    milestone_data, _ = github_get(milestone_url, token=token)
    issues_data = github_get_paginated(issues_url, token=token)

    repo_key = repo.replace("-", "_")
    write_json(output_dir / f"{repo_key}_milestone_{milestone}.json", milestone_data)
    write_json(output_dir / f"{repo_key}_milestone_{milestone}_issues.json", issues_data)


if __name__ == "__main__":
    main()
