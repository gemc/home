#!/usr/bin/env python3
"""
Generate gemc_view.png, .vtksz, analyzer plots, and variation image tables for
every example in _data/examples.yml, and update the corresponding markdown sections.

Run from the repository root:

    ~/venv/pygemc/bin/python scripts/generate_example_assets.py             # all
    ~/venv/pygemc/bin/python scripts/generate_example_assets.py --vtk       # VTK only
    ~/venv/pygemc/bin/python scripts/generate_example_assets.py --screenshots  # screenshots only
    ~/venv/pygemc/bin/python scripts/generate_example_assets.py --plots     # analyzer plots + md update only
    ~/venv/pygemc/bin/python scripts/generate_example_assets.py b1 cherenkov   # selected examples

Values (vtz_zoom, snevents, pevents, to_plot, variation_plots) are read from _data/examples.yml.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT     = Path(__file__).resolve().parent.parent
EXAMPLES_YML  = REPO_ROOT / "_data" / "examples.yml"
SRC_EXAMPLES  = Path("/opt/projects/gemc/src/examples")
ASSETS_ROOT   = REPO_ROOT / "assets" / "images" / "examples"
GEMC          = Path("/opt/projects/gemc/src/build/bin/gemc")
PYGEMC_SRC    = Path("/opt/projects/gemc/pygemc/src")
PYGEMC_PYTHON = Path("~/venv/pygemc/bin/python").expanduser()
GEMC_ANALYZER = Path("~/venv/pygemc/bin/gemc-analyzer").expanduser()

G4VIEW = "[{driver: TOOLSSG_OFFSCREEN, segsPerCircle: 200}]"

# ---------------------------------------------------------------------------
# Analyzer variable config: var → (data_stream, column, extra_cli, img_stem, description)
# ---------------------------------------------------------------------------
PLOT_CONFIG = {
    "totEdep": ("digitized", "totEdep", [],
                "analyzer_totEdep",     "total energy deposited per hit"),
    "dose":    ("digitized", "dose",    [],
                "analyzer_dose",        "accumulated dose"),
    "etot":    ("digitized", "etot",    [],
                "analyzer_etot",        "deposited energy"),
    "E":       ("true_info", "E",       [],
                "analyzer_true_energy", "true particle track energy"),
    "yvsx":    ("true_info", None,
                ["--plot", "yvsx", "--xlim", "-20", "20", "--ylim", "-20", "20"],
                "analyzer_yvsx",        "y vs x hit positions"),
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_examples() -> list:
    with open(EXAMPLES_YML) as f:
        return yaml.safe_load(f) or []


def parse_vtksz_path(vtksz: str):
    """Return (asset_slug, vtksz_stem) from a Jekyll-relative vtksz path."""
    parts = vtksz.split("/")
    slug = parts[-2]
    stem = Path(parts[-1]).stem
    return slug, stem


def find_primary_yaml(src_dir: Path) -> Path:
    """Return the main simulation YAML, skipping saved_configuration and annotations."""
    candidates = [
        p for p in src_dir.glob("*.yaml")
        if "saved" not in p.name and p.stem != "annotations"
    ]
    if not candidates:
        raise FileNotFoundError(f"No primary YAML found in {src_dir}")
    if len(candidates) == 1:
        return candidates[0]
    for c in candidates:
        if c.stem in (src_dir.name, src_dir.name + "s"):
            return c
    return candidates[0]


def find_geometry_script(src_dir: Path) -> Path:
    """Return the geometry Python script (the one calling autogeometry)."""
    candidates = [p for p in src_dir.glob("*.py") if not p.name.startswith("_")]
    if not candidates:
        raise FileNotFoundError(f"No Python script found in {src_dir}")
    if len(candidates) == 1:
        return candidates[0]
    for c in candidates:
        if "autogeometry" in c.read_text(errors="ignore"):
            return c
    return candidates[0]


def ensure_db(src_dir: Path, py_script: Path) -> bool:
    """Run the geometry script without pyvista flags to create gemc.db if missing."""
    db = src_dir / "gemc.db"
    if db.exists():
        return True
    print(f"  Building gemc.db …", flush=True)
    result = subprocess.run(
        [str(PYGEMC_PYTHON), py_script.name],
        cwd=src_dir, env=_pygemc_env(), capture_output=True, text=True,
    )
    if not db.exists():
        print(f"  ERROR: gemc.db still missing after running {py_script.name}")
        print(result.stderr[-400:])
        return False
    return True


def _pygemc_env() -> dict:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PYGEMC_SRC)
    env["MPLCONFIGDIR"] = "/private/tmp/matplotlib-cache"
    return env


def extract_yaml_section(yaml_path: Path, key: str) -> str | None:
    """Return the raw indented block for a top-level key, preserving original formatting."""
    lines = yaml_path.read_text().splitlines()
    block: list[str] = []
    for line in lines:
        if block:
            if line and not line[0].isspace() and not line.startswith("#"):
                break
            block.append(line)
        elif line.startswith(f"{key}:"):
            block.append(line)
    if not block:
        return None
    while block and not block[-1].strip():
        block.pop()
    return "\n".join(block)


def get_csv_base(yaml_path: Path) -> str | None:
    """Return the CSV gstreamer filename from the example YAML, or None if absent."""
    with open(yaml_path) as f:
        cfg = yaml.safe_load(f) or {}
    for entry in cfg.get("gstreamer", []):
        if entry.get("format") == "csv":
            return entry.get("filename")
    return None


def get_system_name(yaml_path: Path) -> str | None:
    """Return the first gsystem name from the example YAML."""
    with open(yaml_path) as f:
        cfg = yaml.safe_load(f) or {}
    gsystem = cfg.get("gsystem", [])
    return gsystem[0].get("name") if gsystem else None


def link_to_md_path(link: str) -> Path:
    """Convert a Jekyll link like '/home/examples/basic/b1' to the .md source path."""
    parts = [p for p in link.split("/") if p and p != "home"]
    parts[0] = "_" + parts[0]
    parts[-1] = parts[-1] + ".md"
    return REPO_ROOT.joinpath(*parts)


# ---------------------------------------------------------------------------
# Screenshot
# ---------------------------------------------------------------------------

def _quote_cmd(cmd: list[str]) -> str:
    """Format a command list for display, quoting args that contain [ or spaces."""
    def _q(c: str) -> str:
        if "=" in c:
            k, v = c.split("=", 1)
            if "[" in v or " " in v:
                return f'{k}="{v}"'
        return c
    return " ".join(_q(c) for c in cmd)


def run_screenshot(src_dir: Path, yaml_file: Path, asset_dir: Path, n: int,
                   extra_args: list[str] | None = None) -> bool:
    """Run gemc with TOOLSSG_OFFSCREEN and save gemc_run_1.png as gemc_view.png."""
    cmd = [str(GEMC), yaml_file.name, f"-g4view={G4VIEW}", f"-n={n}"]
    if extra_args:
        cmd += extra_args
    print(f"  screenshot gemc_view.png  (n={n})", flush=True)
    print(f"  {_quote_cmd(cmd)}", flush=True)
    result = subprocess.run(cmd, cwd=src_dir, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR: gemc exited {result.returncode}")
        print(result.stderr[-400:])
        return False
    png = src_dir / "gemc_run_1.png"
    if not png.exists():
        print(f"  ERROR: gemc_run_1.png not produced")
        return False
    asset_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(png, asset_dir / "gemc_view.png")
    print(f"  → {asset_dir / 'gemc_view.png'}")
    return True


# ---------------------------------------------------------------------------
# VTK
# ---------------------------------------------------------------------------

def run_vtk(src_dir: Path, py_script: Path, yaml_file: Path,
            asset_dir: Path, stem: str, pvz: float) -> bool:
    """Run the pygemc script with -pvvtk and --read-yaml to export .vtksz."""
    out_base = asset_dir / stem
    cmd = [
        str(PYGEMC_PYTHON), py_script.name,
        "--read-yaml", yaml_file.name,
        "-pvvtk", str(out_base),
        "-pvz",   str(pvz),
    ]
    print(f"  VTK  {stem}.vtksz  (pvz={pvz})", flush=True)
    result = subprocess.run(cmd, cwd=src_dir, env=_pygemc_env(),
                            capture_output=True, text=True)
    vtksz = Path(str(out_base) + ".vtksz")
    if not vtksz.exists():
        print(f"  ERROR: {vtksz} not produced")
        print(result.stderr[-400:])
        return False
    print(f"  → {vtksz}")
    return True


# ---------------------------------------------------------------------------
# Analyzer plots
# ---------------------------------------------------------------------------

def run_gemc_for_plots(src_dir: Path, yaml_file: Path, n: int,
                       extra_args: list[str] | None = None) -> bool:
    """Run gemc in batch mode to produce CSV output for the analyzer."""
    cmd = [str(GEMC), yaml_file.name, f"-n={n}"]
    if extra_args:
        cmd += extra_args
    print(f"  gemc (analyzer events n={n}): {_quote_cmd(cmd)}", flush=True)
    result = subprocess.run(cmd, cwd=src_dir, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR: gemc exited {result.returncode}")
        print(result.stderr[-400:])
        return False
    return True


def run_single_plot(src_dir: Path, csv_base: str, var: str,
                    asset_dir: Path) -> bool:
    """Run gemc-analyzer for one variable and save the figure to asset_dir."""
    if var not in PLOT_CONFIG:
        print(f"  WARNING: unknown plot variable '{var}', skipping")
        return False
    data_stream, col, extra, img_stem, desc = PLOT_CONFIG[var]
    csv_file = f"{csv_base}_t0_{data_stream}.csv"
    save_path = asset_dir / f"{img_stem}.png"

    cmd = [str(GEMC_ANALYZER), csv_file, "--kind", "csv"]
    if col:
        cmd.insert(2, col)
    if data_stream == "true_info":
        cmd += ["--data", "true_info"]
    cmd += extra
    cmd += ["--save", str(save_path)]

    print(f"  plot {img_stem}.png  ({var})", flush=True)
    asset_dir.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(cmd, cwd=src_dir, env=_pygemc_env(),
                            capture_output=True, text=True)
    if not save_path.exists():
        print(f"  ERROR: {save_path.name} not produced")
        print(result.stderr[-400:])
        return False
    print(f"  → {save_path}")
    return True


def _fmt_n(n: int) -> str:
    return f"{n:,}"


def build_analyzer_section(slug: str, yaml_name: str, csv_base: str,
                            pevents: int, to_plot_list: list[str],
                            title: str) -> str:
    """Return the full '## Plotting with the GEMC Analyzer' markdown section."""
    lines = ["## Plotting with the GEMC Analyzer\n"]
    lines.append(f"\nRun GEMC with {_fmt_n(pevents)} events first. "
                 f"The default YAML file writes `{csv_base}_t0_digitized.csv`.\n")
    lines.append(f"\n```shell\ngemc {yaml_name} -n={pevents}\n```\n")

    for var in to_plot_list:
        if var not in PLOT_CONFIG:
            continue
        data_stream, col, extra, img_stem, desc = PLOT_CONFIG[var]
        csv_file = f"{csv_base}_t0_{data_stream}.csv"

        parts = ["gemc-analyzer", csv_file]
        if col:
            parts.append(col)
        parts += ["--kind", "csv"]
        if data_stream == "true_info":
            parts += ["--data", "true_info"]
        parts += extra

        img_path = f"/home/assets/images/examples/{slug}/{img_stem}.png"
        lines.append(f"\nPlot the {desc}:\n")
        lines.append(f"\n```shell\n{' '.join(parts)}\n```\n")
        lines.append(f"\n![{title} {desc}]({img_path})" + '{:width="70%"}\n')

    return "".join(lines)


def update_analyzer_section(md_path: Path, new_section: str) -> bool:
    """Replace '## Plotting with the GEMC Analyzer' to EOF with new_section."""
    if not md_path.exists():
        print(f"  WARNING: markdown not found: {md_path}")
        return False
    text = md_path.read_text()
    marker = "## Plotting with the GEMC Analyzer"
    idx = text.find(marker)
    if idx == -1:
        print(f"  WARNING: analyzer section not found in {md_path.name}")
        return False
    md_path.write_text(text[:idx] + new_section)
    print(f"  → updated analyzer section in {md_path.name}")
    return True


def run_plots(ex: dict, src_dir: Path, yaml_file: Path,
              asset_dir: Path, slug: str) -> None:
    """Run gemc + gemc-analyzer and update the markdown analyzer section."""
    pevents     = ex.get("pevents")
    to_plot_str = ex.get("to_plot", "")
    link        = ex.get("link", "")
    title       = ex.get("title", slug)

    if not pevents or not to_plot_str:
        return

    to_plot_list = [v.strip() for v in to_plot_str.split(",") if v.strip()]
    if not to_plot_list:
        return

    csv_base = get_csv_base(yaml_file)
    if not csv_base:
        print(f"  WARNING: no CSV gstreamer in {yaml_file.name}, skipping plots")
        return

    print(f"  plots  (n={pevents}, vars={to_plot_str})", flush=True)

    if not run_gemc_for_plots(src_dir, yaml_file, pevents):
        return

    for var in to_plot_list:
        run_single_plot(src_dir, csv_base, var, asset_dir)

    md_path = link_to_md_path(link)
    section = build_analyzer_section(slug, yaml_file.name, csv_base,
                                     pevents, to_plot_list, title)
    update_analyzer_section(md_path, section)


# ---------------------------------------------------------------------------
# Markdown snippet updaters (Generator + Output)
# ---------------------------------------------------------------------------

_GENERATOR_HEADING = "## Generator\n\n"
_GENERATOR_GENERIC = "The particle kinematics are defined in the YAML file:"


def update_generator_snippet(md_path: Path, yaml_file: Path) -> bool:
    """Replace the Generator section description + gparticle block with the YAML content."""
    gparticle = extract_yaml_section(yaml_file, "gparticle")
    if not gparticle:
        return False
    text = md_path.read_text()
    heading_start = text.find(_GENERATOR_HEADING)
    if heading_start == -1:
        return False
    content_start = heading_start + len(_GENERATOR_HEADING)
    block_open = "```yaml\ngparticle:"
    block_start = text.find(block_open, content_start)
    if block_start == -1:
        return False
    block_end = text.find("\n```", block_start) + len("\n```")
    new_text = (text[:heading_start]
                + _GENERATOR_HEADING
                + _GENERATOR_GENERIC + "\n\n"
                + "```yaml\n" + gparticle + "\n```"
                + text[block_end:])
    md_path.write_text(new_text)
    print(f"  → updated Generator snippet in {md_path.name}")
    return True


def update_output_snippet(md_path: Path, yaml_file: Path) -> bool:
    """Replace the gstreamer yaml block in the Output section with the YAML content."""
    gstreamer = extract_yaml_section(yaml_file, "gstreamer")
    if not gstreamer:
        return False
    text = md_path.read_text()
    out_start = text.find("## Output\n")
    if out_start == -1:
        return False
    block_open = "```yaml\ngstreamer:"
    block_start = text.find(block_open, out_start)
    if block_start == -1:
        return False
    block_end = text.find("\n```", block_start) + len("\n```")
    new_text = (text[:block_start]
                + "```yaml\n" + gstreamer + "\n```"
                + text[block_end:])
    md_path.write_text(new_text)
    print(f"  → updated Output snippet in {md_path.name}")
    return True


# ---------------------------------------------------------------------------
# Variation plots  (examples with multiple gsystem variations, e.g. cherenkov)
# ---------------------------------------------------------------------------

def _gsystem_arg(system_name: str, variation: str) -> str:
    return f"-gsystem=[{{name: {system_name}, variation: {variation}}}]"


def run_variation_screenshot(src_dir: Path, yaml_file: Path, asset_dir: Path,
                             system_name: str, variation: str,
                             label: str, n: int) -> bool:
    """Run gemc for one variation and save gemc_run_1.png as <label>.png."""
    gsys = _gsystem_arg(system_name, variation)
    cmd  = [str(GEMC), yaml_file.name, f"-g4view={G4VIEW}", f"-n={n}", gsys]
    print(f"  variation screenshot {label}.png  ({variation}, n={n})", flush=True)
    print(f"  {_quote_cmd(cmd)}", flush=True)
    result = subprocess.run(cmd, cwd=src_dir, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR: gemc exited {result.returncode}")
        print(result.stderr[-400:])
        return False
    png = src_dir / "gemc_run_1.png"
    if not png.exists():
        print(f"  ERROR: gemc_run_1.png not produced")
        return False
    asset_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(png, asset_dir / f"{label}.png")
    print(f"  → {asset_dir / f'{label}.png'}")
    return True


def run_variation_analyzer(src_dir: Path, yaml_file: Path, asset_dir: Path,
                           system_name: str, variation: str,
                           label: str, csv_base: str, n: int) -> bool:
    """Run gemc then gemc-analyzer (yvsx) for one variation → <label>_y_vs_x.png."""
    gsys = _gsystem_arg(system_name, variation)
    if not run_gemc_for_plots(src_dir, yaml_file, n, extra_args=[gsys]):
        return False

    _, _, extra, _, _ = PLOT_CONFIG["yvsx"]
    csv_file  = f"{csv_base}_t0_true_info.csv"
    save_path = asset_dir / f"{label}_y_vs_x.png"
    cmd = ([str(GEMC_ANALYZER), csv_file, "--kind", "csv", "--data", "true_info"]
           + extra + ["--save", str(save_path)])
    print(f"  variation plot {label}_y_vs_x.png", flush=True)
    asset_dir.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(cmd, cwd=src_dir, env=_pygemc_env(),
                            capture_output=True, text=True)
    if not save_path.exists():
        print(f"  ERROR: {save_path.name} not produced")
        print(result.stderr[-400:])
        return False
    print(f"  → {save_path}")
    return True


def build_variation_table(slug: str, variation_plots: list) -> str:
    """Return the markdown image table + caption block for the given variations."""
    img_base = f"/home/assets/images/examples/{slug}"
    n = len(variation_plots)
    sep  = "|" + "|".join([":---:"] * n) + "|"
    row1 = ("|"
            + "|".join(f" ![{v['label'].replace('_', ' ')}]({img_base}/{v['label']}.png) "
                       for v in variation_plots)
            + "|")
    row2 = ("|"
            + "|".join(f" ![{v['label'].replace('_', ' ')} y vs x]"
                       f"({img_base}/{v['label']}_y_vs_x.png) "
                       for v in variation_plots)
            + "|")
    positions = ["Left", "Center", "Right", "Right"][:n]
    caption_items = ", ".join(
        f"{pos}: <span class=\"gstring\">{v['name']}</span>"
        for pos, v in zip(positions, variation_plots)
    )
    caption = f'<p class="image-caption">\n  {caption_items}.\n</p>'
    return f"{sep}\n{row1}\n{row2}\n\n{caption}"


def update_variation_table(md_path: Path, new_table: str) -> bool:
    """Replace the variation image table + caption block in the markdown."""
    text = md_path.read_text()
    table_start = text.find("|:---")
    if table_start == -1:
        print(f"  WARNING: variation table not found in {md_path.name}")
        return False
    caption_tag = '<p class="image-caption">'
    cap_start   = text.find(caption_tag, table_start)
    if cap_start == -1:
        return False
    cap_end = text.find("</p>", cap_start) + len("</p>")
    md_path.write_text(text[:table_start] + new_table + text[cap_end:])
    print(f"  → updated variation table in {md_path.name}")
    return True


def run_variation_plots(ex: dict, src_dir: Path, yaml_file: Path,
                        asset_dir: Path, slug: str, md_path: Path | None,
                        do_screenshots: bool, do_plots: bool) -> None:
    """Process all variation_plots entries for an example."""
    variation_plots = ex.get("variation_plots", [])
    if not variation_plots:
        return

    snevents    = ex.get("snevents", 1)
    pevents     = ex.get("pevents")
    system_name = get_system_name(yaml_file) or slug
    csv_base    = get_csv_base(yaml_file)

    for vp in variation_plots:
        variation = vp.get("variation", "")
        label     = vp.get("label", "")
        if not variation or not label:
            continue
        if do_screenshots:
            run_variation_screenshot(src_dir, yaml_file, asset_dir,
                                     system_name, variation, label, snevents)
        if do_plots and pevents and csv_base:
            run_variation_analyzer(src_dir, yaml_file, asset_dir,
                                   system_name, variation, label, csv_base, pevents)

    if do_plots and md_path and md_path.exists():
        table = build_variation_table(slug, variation_plots)
        update_variation_table(md_path, table)


# ---------------------------------------------------------------------------
# Per-example processing
# ---------------------------------------------------------------------------

def process(ex: dict, do_screenshots: bool, do_vtk: bool, do_plots: bool):
    title    = ex.get("title", "")
    category = ex.get("category", "")
    vtksz    = ex.get("vtksz", "")
    pvz      = ex.get("vtz_zoom")
    snevents = ex.get("snevents", 1)

    if not vtksz:
        return

    slug, stem = parse_vtksz_path(vtksz)

    src_dir = SRC_EXAMPLES / category / stem
    if not src_dir.is_dir():
        src_dir = SRC_EXAMPLES / category / slug
    if not src_dir.is_dir():
        print(f"  WARNING: source dir not found for '{title}' – skipping")
        return

    asset_dir = ASSETS_ROOT / slug

    print(f"\n{'─'*60}")
    print(f"{title}  ({category}/{stem})", flush=True)

    with tempfile.TemporaryDirectory(prefix="gemc_assets_") as tmpdir:
        work_dir = Path(tmpdir) / stem
        shutil.copytree(src_dir, work_dir)
        print(f"  working copy: {work_dir}", flush=True)

        try:
            yaml_file = find_primary_yaml(work_dir)
            py_script = find_geometry_script(work_dir)
        except FileNotFoundError as e:
            print(f"  ERROR: {e}")
            return

        if do_screenshots:
            ensure_db(work_dir, py_script)
            run_screenshot(work_dir, yaml_file, asset_dir, snevents)

        if do_vtk and pvz is not None:
            run_vtk(work_dir, py_script, yaml_file, asset_dir, stem, pvz)

        if do_plots:
            ensure_db(work_dir, py_script)
            link    = ex.get("link", "")
            md_path = link_to_md_path(link) if link else None
            if md_path and md_path.exists():
                update_generator_snippet(md_path, yaml_file)
                update_output_snippet(md_path, yaml_file)
            run_plots(ex, work_dir, yaml_file, asset_dir, slug)

        if do_screenshots or do_plots:
            link    = ex.get("link", "")
            md_path = link_to_md_path(link) if link else None
            run_variation_plots(ex, work_dir, yaml_file, asset_dir, slug,
                                md_path if do_plots else None,
                                do_screenshots, do_plots)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--vtk",         action="store_true", help="VTK files only")
    parser.add_argument("--screenshots", action="store_true", help="Screenshots only")
    parser.add_argument("--plots",       action="store_true", help="Analyzer plots only")
    parser.add_argument("examples", nargs="*",
                        help="Titles to process (default: all; case-insensitive)")
    args = parser.parse_args()

    any_flag       = args.vtk or args.screenshots or args.plots
    do_vtk         = args.vtk         or not any_flag
    do_screenshots = args.screenshots or not any_flag
    do_plots       = args.plots       or not any_flag

    def normalise(s: str) -> str:
        return s.lower().replace(" ", "_").replace("-", "_")

    filter_set   = {normalise(t) for t in args.examples}
    all_examples = load_examples()
    targets = [
        ex for ex in all_examples
        if ex.get("vtksz")
        and (not filter_set or normalise(ex.get("title", "")) in filter_set)
    ]

    if not targets:
        print("No matching examples with a vtksz entry found.")
        sys.exit(1)

    for ex in targets:
        process(ex, do_screenshots, do_vtk, do_plots)

    print(f"\n{'─'*60}")
    print("Done.")


if __name__ == "__main__":
    main()
