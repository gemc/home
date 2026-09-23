"""Render the generator example's ganalysis layouts from fresh, verified true-information CSV data."""

import importlib.util
import subprocess
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml
from pygemc.analyzer import plot_variable, plot_y_vs_x


class CaseDumper(yaml.SafeDumper):
    """Keep the generated particle snippets readable in the website data file."""


def represent_text(dumper, value):
    return dumper.represent_scalar("tag:yaml.org,2002:str", value, style="|" if "\n" in value else None)


CaseDumper.add_representer(str, represent_text)


def case_title(name):
    return name.replace("_xy", "_X_and_Y").replace("_", " ").capitalize().replace("x and y", "X and Y")


def render_card(config, hits, output):
    """Use the variables, bins, titles, and fixed limits from the actual steering card."""
    positions = dict(zip(("top_left", "top_right", "bottom_left", "bottom_right"), range(4)))
    if config.get("ganalysis_plots", 1) == 1:
        fig, ax = plt.subplots(figsize=(8, 6), dpi=150)
        axes = [ax]
    else:
        fig, grid = plt.subplots(2, 2, figsize=(12, 8), dpi=150)
        axes = list(grid.flat)
    for plot in config["ganalysis"]:
        ax = axes[positions[plot["position"]]]
        x = plot["x"]
        unit = "mm" if x.startswith("v") else "MeV/c"
        limits = None
        if plot.get("x_min_auto") is False and plot.get("x_max_auto") is False:
            limits = (plot["x_min"], plot["x_max"])
        if plot.get("dimension") == "2d":
            y = plot["y"]
            y_limits = None
            if plot.get("y_min_auto") is False and plot.get("y_max_auto") is False:
                y_limits = (plot["y_min"], plot["y_max"])
            plot_y_vs_x(hits, x=x, y=y, bins=plot["bins"], position_unit="mm", ax=ax,
                        xlim=limits, ylim=y_limits)
            ax.set_ylabel(f"{y} ({unit})")
            if x.startswith("v") and y.startswith("v"):
                ax.set_aspect("equal", adjustable="box")
        else:
            plot_variable(hits, x, bins=plot["bins"], xlim=limits, group_by=None,
                          logy=False, ax=ax, color="#2878a5")
            ax.set_ylabel("Throws / bin")
            ax.grid(axis="y", alpha=0.18)
        ax.set_xlabel(f"{x} ({unit})")
        ax.set_title(textwrap.fill(plot["title"], 48), fontsize=10, pad=10)
        ax.ticklabel_format(axis="x", style="plain", useOffset=False)
    title = case_title(output.stem.removeprefix("analyzer_"))
    fig.suptitle(f"{title}  |  {len(hits):,} verified throws", fontsize=16, y=0.99)
    fig.tight_layout(rect=(0, 0, 1, 0.95), h_pad=2, w_pad=2)
    fig.savefig(output, facecolor="white")
    plt.close(fig)


def run_steering_plots(ex, work_dir, asset_dir, gemc, env, data_path):
    # Load the source example's checks instead of maintaining a second distribution implementation.
    spec = importlib.util.spec_from_file_location("generator_checks", work_dir / "check_generator.py")
    checks = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checks)
    asset_dir.mkdir(parents=True, exist_ok=True)
    cases = []
    for card_name in ex["steering_cards"]:
        card = work_dir / card_name
        config = yaml.safe_load(card.read_text())
        events = int(ex.get("pevents", config["n"]))
        print(f"  {card.name}: generating and checking {events:,} throws", flush=True)
        result = subprocess.run([str(gemc), card.name, f"-n={events}", *ex.get("plot_gemc_args", [])],
                                cwd=work_dir, env=env, capture_output=True, text=True, timeout=60)
        if result.returncode:
            raise RuntimeError(f"{card.name} failed: {result.stdout[-2000:]} {result.stderr[-2000:]}")
        base = next(item["filename"] for item in config["gstreamer"] if item["format"] == "csv")
        generated = checks.read_rows(next(work_dir.glob(base + "*_generated.csv")))
        hits_path = next(work_dir.glob(base + "*_true_info.csv"))
        hits = checks.read_rows(hits_path)
        assert len(generated) == len(hits) == events
        by_event = {row["evn"]: row for row in generated}
        assert len(by_event) == events and {row["evn"] for row in hits} == set(by_event)
        for hit in hits:
            assert hit["detector"] == "flux" and float(hit["tid"]) == 1 and float(hit["mtid"]) == 0
            thrown = by_event[hit["evn"]]
            assert np.allclose([float(hit["v" + axis]) for axis in "xyz"],
                               [float(thrown["v" + axis]) for axis in "xyz"], rtol=0, atol=0.001)
            checks.check_momentum(hit, thrown)
        particle = config["gparticle"][0]
        checks.check_vertices(generated, particle)
        checks.check_angles(generated, particle)
        image_name = f"analyzer_{card.stem}.png"
        render_card(config, pd.read_csv(hits_path, skipinitialspace=True), asset_dir / image_name)
        cases.append({
            "name": card.stem,
            "title": case_title(card.stem),
            "group": "Angles" if "delta_theta" in particle else "Vertices",
            "expected": card.read_text().splitlines()[0].removeprefix("# "),
            "events": events,
            "view_events": ex.get("snevents", 1),
            "event_image": f"assets/images/examples/{asset_dir.name}/gemc_{card.stem}.png",
            "particle": yaml.safe_dump({"gparticle": [particle]}, sort_keys=False, width=100),
            "image": f"assets/images/examples/{asset_dir.name}/{image_name}",
        })
        print(f"  → {asset_dir / image_name}", flush=True)
    data_path.write_text(yaml.dump(cases, Dumper=CaseDumper, sort_keys=False, width=100))
