# Generating offscreen images or VTK

Use `scripts/generate_example_assets.py` to regenerate all assets in one step:

```shell
# from the repository root — requires ~/venv/pygemc/bin/python
~/venv/pygemc/bin/python scripts/generate_example_assets.py             # all examples
~/venv/pygemc/bin/python scripts/generate_example_assets.py --vtk       # VTK only
~/venv/pygemc/bin/python scripts/generate_example_assets.py --screenshots  # screenshots only
~/venv/pygemc/bin/python scripts/generate_example_assets.py b1 cherenkov   # selected examples
```

The script reads `vtz_zoom` and `snevents` from `_data/examples.yml` automatically.
The gemc binary is at `/opt/projects/gemc/src/build/bin/gemc` (no module load needed at runtime).

The sections below document the manual steps the script automates.

## GEMC Screenshots

Each example produces one screenshot: `gemc_view.png`, showing events running through the geometry.
The driver is TOOLSSG_OFFSCREEN; run from the example directory. The driver writes `gemc_run_0.png`.

**gemc_view.png** — use `snevents` from `_data/examples.yml` (default `-n=1` if absent):

```shell
cd /opt/projects/gemc/src/examples/<category>/<example>
/opt/projects/gemc/src/build/bin/gemc <example>.yaml \
  -g4view="[{driver: TOOLSSG_OFFSCREEN, segsPerCircle: 200}]" \
  -n=<snevents>
cp gemc_run_0.png /opt/projects/gemc/home/assets/images/examples/<example>/gemc_view.png
```

## VTK

VTK files use the `~/venv/pygemc` environment and the standalone pygemc source.
Run from the example directory. Use `vtz_zoom` from `_data/examples.yml` as `-pvz`.

```shell
cd /opt/projects/gemc/src/examples/<category>/<example>
PYTHONPATH=/opt/projects/gemc/pygemc/src \
  MPLCONFIGDIR=/private/tmp/matplotlib-cache \
  ~/venv/pygemc/bin/python <example>.py \
  -pvvtk /opt/projects/gemc/home/assets/images/examples/<example>/<vtksz_stem> \
  -pvz <vtz_zoom>
```

The `-pvvtk` path has no extension; pygemc appends `.vtksz` automatically.
The vtksz stem matches the basename in the `vtksz:` field in `_data/examples.yml`.

### Per-example reference

| Example | category | script | vtksz stem |
|---------|----------|--------|------------|
| b1 | basic | b1.py | b1 |
| b2 | basic | b2.py | b2 |
| materials | basic | materials.py | material |
| scintillator_barrel | basic | scintillator_barrel.py | scintillator_barrel |
| simple_flux | basic | simple_flux.py | simple_flux |
| cherenkov | optical | cherenkov.py | cherenkov |

`vtz_zoom` and `snevents` live in `_data/examples.yml` — do not duplicate them here.


# Generate pyvista solids

Use scripts/generate_solid_vtksz.py 


# Qt GUI SVG icon system

SVG icons for toggle buttons (`g4display/images/*.svg`) use a single file for both checked and unchecked states.
The background placeholder `fill="#aaddff"` and foreground `currentColor` are replaced at render time in
`GQTToggleButtonWidget::refresh_svg_icons()`:

- **Unchecked**: background → `"none"`, foreground → `palette(WindowText)`
- **Checked**: background → `palette(Highlight).name()`, foreground → `palette(HighlightedText)`

`refresh_svg_icons()` is called on construction, on every `toggled` signal, and on palette/style changes
(`changeEvent`). This keeps icons in sync with the system theme without per-state SVG files.

SVG frame convention (48×48 viewBox): `<rect x="6" y="6" width="36" height="36" rx="3" fill="#aaddff"
stroke="currentColor" stroke-width="1"/>`. Drawing occupies `y=12–22`; two label lines at `y=31`/`y=38`,
`font-size="7.5"`, `font-family="Arial"`, `font-weight="500"`, `text-anchor="middle"`, `fill="currentColor"`.

**Two-level QRC registration**: SVGs must appear in both the module-level `qtresources.qrc` (for tests/examples)
and the root `qtresources.qrc` (for the main binary), using identical `alias` paths.

**Button sizing**: `GQTToggleButtonWidget` and `GQTButtonsWidget` currently use 120×120 px buttons. CSS is
minimal — `border: none; background-color: transparent; padding: 0; margin: 0;` — so the SVG itself carries
all visual state.




# GUI diagrams (SVG from scratch)

GUI pages are documented as hand-drawn SVGs in `assets/images/documentation/display_*.svg`.
Each SVG contains the full schematic of the Qt UI plus annotation labels and arrows — no PNG embedding.

**Key command:** when told **"annotate gui"** (or "reannotate gui"), re-read this section, inspect the
corresponding screenshot (if one is provided or already on disk), adjust element positions and annotation
coordinates in the relevant SVG, and rebuild all annotation entries from this spec. The SVGs are the
source of truth; `scripts/annotate_gui.py` is obsolete.

**Always derive UI structure from Qt source headers, not screenshots.** Key source files:
- Display View tab: `src/g4display/tabs/g4displayview.h` — `QSlider` (camera/light θ/φ), `QComboBox` (presets, projection, precision, culling, background), `QCheckBox` (slice On/Flip), `QRadioButton` (Intersection/Union), `GQTToggleButtonWidget` (6 toggle buttons)
- Volumes tree: `src/gtree/gtree.h` — `QTreeWidget` (3 cols: visibility checkbox, color button, name), right panel: `GQTButtonsWidget` (wireframe/solid/cloud), `QSlider` opacity, labels (type, daughters, name, material, mass, volume, density)
- Setup tree: `src/dbselect/dbselectView.h` — `QStandardItemModel` (exp/system, volumes, variation, run cols), `ComboDelegate` for variation/run dropdowns, green/red status icon
- G4 Commands: `src/g4dialog/tabs/gcommands.h` — `QLineEdit` search, `QTreeView` commands, `QTextEdit` help, `QListWidget` history, `QLineEdit` command entry

**Icon sources (embed inline as `<g>` elements — do NOT use `<image>` or external refs):**
- Left-panel page buttons (90×90): `src/gui/images/buttons/display_1.svg`, `dialog_1.svg`, `setup_1.svg`, `tree_1.svg`
  - Embed with `transform="translate(11,Y) scale(1.875)"` — scales 48×48 icon to fill the 90×90 button
  - Active button: `style="color:white"` on the `<g>` (icons use `currentColor` throughout)
  - Inactive button: `style="color:var(--muted)"` on the `<g>`
- Volumes style buttons (48×48): `src/gtree/images/wireframe_1.svg`, `surface_1.svg`, `cloud_1.svg`
  - Embed with `transform="translate(x,y)"` (scale 1:1) — icon is already 48×48
  - Active button: `style="color:white"`, button rect `fill="var(--active)"`
  - Inactive button: `style="color:var(--muted)"`, button rect `class="style-btn"`

**SVG style conventions (match `gemcArchitecture.svg`):**
- Font: Avenir / "Segoe UI" / Arial
- CSS variables: `--ink`, `--muted`, `--section`, `--border`, `--active`, `--panel` etc. with `@media (prefers-color-scheme: dark)` block
- Annotation boxes: `.ann-box` (white fill, blue stroke `#1a50c0`), `.ann-text` bold 11.5 px
- Annotation arrows: `.ann-line` stroke `#c8200e`, `marker-end: url(#arr)`, arrowhead `<marker id="arr">`
- Toggle buttons: coral red `#e05a52`
- Active page button / tab: `#007aff`

## display_gui.svg — Display page (viewBox 0 0 980 800)

| Label                    | Target                                                                 |
|--------------------------|------------------------------------------------------------------------|
| Toggle rendering options | center of the 6 red toggle buttons — label bc above, arrow down        |
| Slide to orbit camera    | camera θ slider thumb — label inside camera box below header           |
| Projection and precision | TWO arrows: one → Projection dropdown, one → Sides per circle dropdown |
| Reposition light source  | light θ slider thumb — label inside light box near bottom, arrow up    |
| Cut planes position      | X input field — label right of On/Flip row, horizontal arrow left      |
| CUT Switch               | Y-row "On" toggle (second On) — label right, arrow left                |

## display_setup.svg — Setup page (viewBox 0 0 980 640)

Table columns (x dividers at 310, 394, 534, 720); column centers: volumes=352, variation=464, run=627.
Data rows end at y=286; annotations live in the empty striped-row space below.
Arrows are vertical at their column x, staggered in y so labels never overlap.

| Label                    | Target                    | Placement                                                    |
|--------------------------|---------------------------|--------------------------------------------------------------|
| # matching volumes       | volumes column header     | tc x=352 y=406, arrow up to y=154                            |
| Select variation         | variation column header   | tc x=464 y=462, arrow up to y=154                            |
| Select run number        | run column header         | tc x=627 y=518, arrow up to y=154                            |
| Check to include in sim. | toggle of simple_flux row | label right of data at x=728, horizontal arrow left to x=188 |
| Click to reload geometry | Reload button             | label ending at x=868, short arrow right to Reload at x=908  |

## display_volumes.svg — Volumes page (viewBox 0 0 980 560)

b2 geometry shown; chamber_0 selected. Tree columns: Visibility / Color / Name (x≈136–656). Right properties panel x=668–956.

| Label                  | Target                            | Placement                                                                 |
|------------------------|-----------------------------------|---------------------------------------------------------------------------|
| Check to show / hide   | tracker visibility checkbox       | ann-box tc x=148 y=392, arrow UP from y=390 to y=238 (tracker row)        |
| Click to change color  | target color swatch button        | ann-box tc x=215 y=442, diagonal arrow to (193,216) (target color button) |
| Volumes in system tree | Name column header                | ann-box bc x=420 y=98, arrow DOWN from y=118 to y=128                     |
| Selected volume info   | Properties panel title            | ann-box bc x=800 y=98, arrow DOWN from y=118 to y=162                     |
| Set transparency (0–1) | Opacity slider (right panel)      | ann-box bc x=800 y=370, horizontal arrow LEFT from (712,359) to (726,359) |

## display_g4dialog.svg — G4Dialog page (viewBox 0 0 980 720)

Layout: search strip y=50–82; command tree (x=112–542) + help panel (x=542–972) y=82–540; history y=540–636; command entry y=636–720.

| Label                           | Target                       | Placement                                                                |
|---------------------------------|------------------------------|--------------------------------------------------------------------------|
| Commands filtered by search     | search input (w_search)      | ann-box tc x=411 y=8, arrow DOWN from y=30 to y=53 (top of input)        |
| Click a command to select       | /run/beamOn selected row     | ann-box tc x=215 y=456, arrow UP from y=456 to y=232 (inside tree)       |
| Parameters and help appear here | right help panel (w_help)    | ann-box tc x=663 y=456, arrow UP from y=456 to y=227 (help content)      |
| History of executed commands    | history section header       | ann-box tc x=657 y=600 (right side), arrow UP from y=600 to y=556        |
| Enter any Geant4 command        | command entry field (w_command) | ann-box tc x=217 y=600 (left side), arrow DOWN from y=622 to y=641    |

