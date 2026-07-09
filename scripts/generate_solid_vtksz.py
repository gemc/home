#!/usr/bin/env python3
"""Generate per-solid .vtksz files for solidTypes.md documentation."""

import os, sys, asyncio, json, zipfile, io

# Use the updated pygemc (with G4Sphere + G4Polycone support) from the source tree
PYGEMC_SRC = "/opt/projects/gemc/pygemc/src"
if PYGEMC_SRC not in sys.path:
    sys.path.insert(0, PYGEMC_SRC)

PYENV_SP = "/opt/jlab_software/macosx26-clang21-arm64/gemc/dev/python_env/lib/python3.14/site-packages"
if PYENV_SP not in sys.path:
    sys.path.insert(0, PYENV_SP)

sys.argv = [sys.argv[0]]

import pyvista as pv
from pygemc.api.gconfiguration import GConfiguration
from pygemc.api.gvolume import GVolume

OUT_DIR = "/opt/projects/gemc/home/assets/images/documentation/solidTypes"
os.makedirs(OUT_DIR, exist_ok=True)


async def export_plotter_async(plotter, out_path: str, zoom: float = 0.35):
    from pyvista.trame.jupyter import launch_server
    from pyvista.trame import PyVistaLocalView
    from pyvista.trame.views import get_server

    server_name = pv.global_theme.trame.jupyter_server_name
    await launch_server(server_name).ready
    server = get_server(server_name)

    view = PyVistaLocalView(plotter, trame_server=server)
    content = view.export(format='zip')
    view.release_resources()
    try:
        plotter._on_render_callbacks.remove(view._plotter_render_callback)
    except ValueError:
        pass

    with open(out_path, 'wb') as f:
        f.write(content)
    print(f"  → {out_path}  ({len(content)} bytes)")


def make_cfg(tag):
    cfg = GConfiguration("solids", tag, enable_pyvista=True, use_background_plotter=False)
    cfg.args.pyvista = False
    cfg.args.pyvista_background = False
    cfg.args.pyvista_background_color = "0.97 0.97 1.0"
    cfg.args.pyvista_background_top = "none"
    return cfg


def publish(cfg, name, make_fn, color="4488cc", opacity=1.0):
    v = GVolume(name)
    make_fn(v)
    v.material = "G4_Al"
    v.color = color
    v.opacity = opacity
    v.style = 1
    v.publish(cfg)


SOLIDS = [
    ("G4Box",    "4488cc", 0.45,
     lambda cfg: publish(cfg, "box",    lambda v: v.make_box(30, 20, 10), color="4488cc")),
    ("G4Tubs",   "44aa66", 0.35,
     lambda cfg: publish(cfg, "tubs",   lambda v: v.make_tube(0, 20, 30, 0, 360), color="44aa66")),
    ("G4Cons",   "cc6644", 0.35,
     lambda cfg: publish(cfg, "cons",   lambda v: v.make_cons(0, 10, 0, 20, 30, 0, 270), color="cc6644")),
    ("G4Trd",    "886644", 0.45,
     lambda cfg: publish(cfg, "trd",    lambda v: v.make_trapezoid(20, 10, 15, 8, 25), color="886644")),
    ("G4Trap",   "aa44aa", 0.40,
     lambda cfg: publish(cfg, "trap",
                          lambda v: v.make_general_trapezoid(25, 5, 10, 12, 15, 10, 8, 10, 12, 8, 5),
                          color="aa44aa")),
    ("G4Sphere", "4466cc", 0.35,
     lambda cfg: publish(cfg, "sphere", lambda v: v.make_sphere(10, 20, 0, 270, 10, 120), color="4466cc")),
    ("G4Polycone", "cc8833", 0.30,
     lambda cfg: publish(cfg, "polycone",
                          lambda v: v.make_polycone(0, 270,
                                                    [-30, -10, 10, 30],
                                                    [0, 10, 10, 0],
                                                    [15, 20, 20, 15]),
                          color="cc8833")),
]


async def main():
    for tag, color, zoom, build_fn in SOLIDS:
        print(f"\n=== {tag} ===")
        try:
            cfg = make_cfg(tag)
            build_fn(cfg)
            plotter = cfg.plotter
            if plotter is None:
                print("  plotter is None — skipping")
                continue
            out = os.path.join(OUT_DIR, f"{tag}.vtksz")
            await export_plotter_async(plotter, out, zoom=zoom)
            cfg.close()
        except Exception as e:
            import traceback
            print(f"  ERROR: {e}")
            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
