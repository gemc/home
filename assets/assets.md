# Generating offscreen images or VTK

Use `scripts/generate_example_assets.py` to regenerate all assets in one step:

```shell
# from the repository root — requires ~/venv/pygemc/bin/python
~/venv/pygemc/bin/python scripts/generate_example_assets.py             # all examples
~/venv/pygemc/bin/python scripts/generate_example_assets.py --vtk       # VTK only
~/venv/pygemc/bin/python scripts/generate_example_assets.py --screenshots  # screenshots only
~/venv/pygemc/bin/python scripts/generate_example_assets.py b1 cherenkov   # selected examples
```

The script reads `source_dir`, `source_support`, `gemc_args`, `vtz_zoom`, `pyvista-fast`, `snevents`,
and `skip_asset_generation` from `_data/examples.yml` automatically.
The gemc binary is at `/opt/projects/gemc/src/build/bin/gemc` (no module load needed at runtime).

Examples normally come from `/opt/projects/gemc/src/examples/<category>/<example>`. Entries with
`source_dir` can point elsewhere, such as `../clas12-systems/geometry_src/dc`. Use `source_support` for sibling
files or directories that the copied working tree needs at generation time.
Use `gemc_args` for extra GEMC command-line arguments, such as a plugin path.

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

When an example sets `pyvista-fast: true` the script appends `--pyvista-fast`, forcing the fast rendering path
that is well suited to large systems such as `ec`; `pyvista-fast: false` appends `--no-pyvista-fast` instead.

Set `skip_asset_generation: true` for examples that should be kept in the examples directory but
excluded from screenshot, VTK, and plot regeneration.

### Per-example reference

| Example | category | script | vtksz stem |
|---------|----------|--------|------------|
| b1 | basic | b1.py | b1 |
| b2 | basic | b2.py | b2 |
| materials | basic | materials.py | material |
| scintillator_barrel | basic | scintillator_barrel.py | scintillator_barrel |
| simple_flux | basic | simple_flux.py | simple_flux |
| cherenkov | optical | cherenkov.py | cherenkov |
| dc | clas12 | dc.py | dc |
| ec | clas12 | ec.py | ec |

`source_dir`, `source_support`, `gemc_args`, `vtz_zoom`, `pyvista-fast`, `snevents`, and
`skip_asset_generation` live in `_data/examples.yml` - do not duplicate them here.


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

## Source-first rebuild plan

When rebuilding any GUI documentation SVG, do this from scratch from `../src/gemc` before editing pixels:

1. Read the applicable Qt source and headers in `../src/gemc`, not only the existing SVG. For each page, list
   the layout containers in order, then list every visible widget created in code.
2. Cross-check page order from `../src/gemc/gui/leftButtons.cc` and
   `../src/gemc/gui/rightContent.cc`. The left rail and active page must match that order.
3. Copy source SVG icon geometry inline from `../src/gemc/.../*.svg`. Keep documentation SVGs self-contained; do
   not reference files outside the published site.
4. Draw the schematic only after the widget inventory is complete. Preserve group-box order, labels, button
   text, spin boxes, combo boxes, sliders, color swatches, and tab names from source.
5. Rebuild annotations after the UI drawing is current. Annotation arrows should target live controls, not old
   coordinates inherited from previous diagrams.
6. Validate all GUI diagrams with `xmllint --noout assets/images/documentation/display_*.svg`, render changed
   files once with `rsvg-convert`, and run
   `/Users/ungaro/.rubies/ruby-3.4.1/bin/bundle exec jekyll build`.

**Key command:** when told **"annotate gui"** (or "reannotate gui"), re-read this section, inspect the
corresponding screenshot (if one is provided or already on disk), adjust element positions and annotation
coordinates in the relevant SVG, and rebuild all annotation entries from this spec. The SVGs are the
source of truth; `scripts/annotate_gui.py` is obsolete.

**Always derive UI structure from Qt source headers, not screenshots.** Key source files:
- Display View tab: `src/gemc/g4display/tabs/g4displayview.h` — `QSlider` (camera/light theta/phi),
  `QComboBox` (presets, projection, precision, culling, background), `QCheckBox` (slice On/Flip),
  `QRadioButton` (Intersection/Union), `GQTToggleButtonWidget` (4 SVG toggle buttons)
- Display Utilities tab: `src/gemc/g4display/tabs/g4displayutilities.h` — scene decoration checkboxes,
  scale/frame fields, color swatches, and 2D/3D scene text annotation controls
- Volumes tree: `src/gemc/gtree/gtree.h` and `src/gemc/gtree/right_widget.cc` — `QTreeWidget`
  (visibility checkbox, color button, name), four `GQTButtonsWidget` style buttons
  (wireframe/surface/cloud/centre-twinkle), `QSlider` opacity, full selected-volume labels, read-only
  parameters text area, `Inspect <leaf>`, and `Draw Logical Overlaps <leaf>`
- Setup tree: `src/gemc/dbselect/dbselectView.h` — `QStandardItemModel` (exp/system, volumes,
  variation, run cols), `ComboDelegate` for the run dropdown, green/red status icon
- G4 Commands: `src/gemc/g4dialog/tabs/gcommands.h` — `QLineEdit` search, `QTreeView` commands,
  `QTextEdit` help, `QListWidget` history, `QLineEdit` command entry
- Generator: `src/gemc/pmaker/pmakerView.cc` and `src/gemc/pmaker/pmakerTab.cc` — `QTabWidget` with one
  particle tab per `Gparticle`, final `+` add tab, Particle/Momentum/Angles/Vertex group boxes, and two
  `AngleCoverageWidget` instances: one for theta and `dtheta`, one for phi and `dphi`

**Icon sources (embed inline as `<g>` elements — do NOT use `<image>` or external refs):**
- Left-panel page buttons (90×90): `src/gui/images/buttons/display_1.svg`, `setup_1.svg`, `tree_1.svg`,
  `dialog_1.svg`, `generator_1.svg`
  - Embed with `transform="translate(11,Y) scale(1.875)"` — scales 48×48 icon to fill the 90×90 button
  - Active button: `style="color:white"` on the `<g>` (icons use `currentColor` throughout)
  - Inactive button: `style="color:var(--muted)"` on the `<g>`
  - Current page order from `src/gemc/gui/leftButtons.cc`: Display, Setup, Volumes, G4Dialog, Generator
- Volumes style buttons (48×48): `src/gemc/gtree/images/wireframe_1.svg`, `surface_1.svg`,
  `cloud_1.svg`, `centre_1.svg`
  - Embed with `transform="translate(x,y)"` (scale 1:1) — icon is already 48×48
  - Active button: `style="color:white"`, button rect `fill="var(--active)"`
  - Inactive button: `style="color:var(--muted)"`, button rect `class="style-btn"`
- Display View toggle buttons: `src/gemc/g4display/images/hidden_lines.svg`, `anti_aliasing.svg`,
  `auxiliary_edges.svg`, `field_lines.svg`
  - Copy the source SVG contents directly into inline `<g>` elements; do not redraw them by hand
  - Keep the documentation SVG self-contained rather than linking to `../src`, which is not published with the
    site
  - Use monochrome `currentColor` artwork on small Qt-style buttons, matching the left page-button treatment

**SVG style conventions (match `gemcArchitecture.svg`):**
- Font: Avenir / "Segoe UI" / Arial
- CSS variables: `--ink`, `--muted`, `--section`, `--border`, `--active`, `--panel`, etc. with
  `@media (prefers-color-scheme: dark)` block
- Annotation boxes: `.ann-box` (white fill, blue stroke `#1a50c0`), `.ann-text` bold 11.5 px
- Annotation arrows: `.ann-line` stroke `#c8200e`, `marker-end: url(#arr)`, arrowhead `<marker id="arr">`
- Toggle buttons: coral red `#e05a52`
- Active page button / tab: `#007aff`

## display_gui.svg — Display page (viewBox 0 0 980 800)

| Label                    | Target                                                                 |
|--------------------------|------------------------------------------------------------------------|
| SVG rendering toggles    | center of the 4 SVG toggle buttons — label bc above, arrow down        |
| Slide to orbit camera    | camera θ slider thumb and Read View button                             |
| Projection and precision | TWO arrows: one → Projection dropdown, one → Sides per circle dropdown |
| Reposition light source  | light θ slider thumb — label inside light box near bottom, arrow up    |
| Cut planes position      | X input field — label right of On/Flip row, horizontal arrow left      |
| CUT Switch               | Y-row "On" toggle (second On) — label right, arrow left                |
| Cloud and explode        | cloud-points spinbox and explode slider/dropdown in Scene Properties   |

## display_utilities.svg — Display Utilities tab (viewBox 0 0 980 720)

| Label             | Target                    | Placement                         |
|-------------------|---------------------------|-----------------------------------|
| Utilities tab     | Utilities tab header      | top right, arrow to active tab    |
| Scene decorations | Apply Decorations button  | label below group, arrow right    |
| Add annotation text | Scene Text text field    | label below group, diagonal arrow |

## display_setup.svg — Setup page (viewBox 0 0 980 640)

Table columns (x dividers at 310, 394, 534, 720); column centers: volumes=352, variation=464, run=627.
Data rows end at y=286; annotations live in the empty striped-row space below.
Arrows are vertical at their column x, staggered in y so labels never overlap.

Annotations:
- `# matching volumes`: target the volumes column header; place tc x=352 y=406, arrow up to y=154.
- `Select variation`: target the variation column header; place tc x=464 y=462, arrow up to y=154.
- `Select run number`: target the run column header; place tc x=627 y=518, arrow up to y=154.
- `Check to include in sim.`: target the simple_flux row toggle; place label right of the data at x=728,
  with a horizontal arrow left to x=188.
- `Click to reload geometry`: target the Reload button; place label ending at x=868, with a short arrow right
  to Reload at x=908.

## display_volumes.svg — Volumes page (viewBox 0 0 980 600)

b2 geometry shown; chamber_0 selected. Tree columns: Visibility / Color / Name (x≈136–656). Right
properties panel x=668–956.
Right panel controls follow `right_widget.cc`: the top row is four 48×48 schematic style buttons representing
the 96×96 Qt buttons (wireframe, surface, cloud, centre/twinkle), followed by opacity, labels, parameter text
area, position, rotation, mother, description, `Inspect chamber_0`, and `Draw Logical Overlaps chamber_0`.

Annotations:
- `Check to show / hide`: target the tracker visibility checkbox; place ann-box tc x=148 y=392, arrow up
  from y=390 to y=238.
- `Click to change color`: target the target color swatch; place ann-box tc x=215 y=442, diagonal arrow to
  (193,216).
- `Volumes in system tree`: target the Name column header; place ann-box bc x=420 y=98, arrow down from
  y=118 to y=128.
- `Selected volume info`: target the properties panel title; place ann-box bc x=800 y=98, arrow down from
  y=118 to y=162.
- `Set transparency (0-1)`: target the opacity slider; place ann-box bc x=800 y=386, horizontal arrow from
  (712,374) to (726,374).
- `Style buttons`: target the representation button row, including the fourth centre/twinkle button.
- `Inspect / overlaps`: target the two full-width action buttons at the bottom of the right panel.

## display_g4dialog.svg — G4Dialog page (viewBox 0 0 980 720)

Layout: search strip y=50–82; command tree (x=112–542) and help panel (x=542–972) y=82–540; history
y=540–636; command entry y=636–720.

Annotations:
- `Commands filtered by search`: target `w_search`; place ann-box tc x=411 y=8, arrow down from y=30 to y=53.
- `Click a command to select`: target the `/run/beamOn` selected row; place ann-box tc x=215 y=456, arrow up
  from y=456 to y=232.
- `Parameters and help appear here`: target `w_help`; place ann-box tc x=663 y=456, arrow up from y=456 to
  y=227.
- `History of executed commands`: target the history section header; place ann-box tc x=657 y=600, arrow up
  from y=600 to y=556.
- `Enter any Geant4 command`: target `w_command`; place ann-box tc x=217 y=600, arrow down from y=622 to
  y=641.

## display_generator.svg — Generator page (viewBox 0 0 980 720)

The Generator page comes from `src/gemc/pmaker/pmakerView.cc` and `src/gemc/pmaker/pmakerTab.cc`. It is a
`QTabWidget` with one tab per `Gparticle`, a final `+` tab that adds a default particle, and close buttons on
particle tabs. Each particle tab contains a scroll area with group boxes for Particle, Momentum, Angles, and
Vertex.

The Angles group has two stacked rows separated by a horizontal line:

- theta row: `thetaSpin`, `thetaSlider`, `dthetaSpin`, `dthetaSlider`, `thetaModelCombo`, and one
  `AngleCoverageWidget`
- phi row: `phiSpin`, `phiSlider`, `dphiSpin`, `dphiSlider`, and a second `AngleCoverageWidget`

Each coverage widget is a 90×90 circle with a gray sector for `center +/- delta` and a red center-angle line.
Do not draw only one angular coverage widget.

| Label                     | Target                            | Placement                          |
|---------------------------|-----------------------------------|------------------------------------|
| One tab per particle      | active particle tab               | top center, arrow down to tab      |
| Add particle              | `+` tab                           | upper right, arrow left to `+` tab |
| Particle and multiplicity | Particle group controls           | right of group, arrow left         |
| Momentum spread           | momentum delta field              | right of group, arrow left         |
| Angular coverage          | theta/phi coverage preview circle | below/right of Angles, arrow up    |
| Vertex model              | vertex model dropdown             | below/right of Vertex, arrow up    |
