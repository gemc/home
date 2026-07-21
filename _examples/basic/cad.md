---
layout: default
title: "CAD example"
---

# CAD Example
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

This example imports three STL organ meshes with the GEMC CAD factory and models a medical
brachytherapy treatment: an **Iridium-192** high-dose-rate (HDR) source is placed *inside the liver*
and emits photons isotropically. Each organ is a %%flux%% sensitive detector, so the deposited energy
is recorded per organ; `plot_dose.py` converts it to absorbed dose and to the equivalent Ir-192
irradiation time.

> **Upcoming in the next release.**

<br/>

## Quickstart

Copy the example to your current directory. To upload the CAD definitions, run 200 events producing
CSV output, and plot the dose in each organ:

```shell
cp -r $GEMC_HOME/examples/basic/cad .
cd cad
./cad.py
gemc cad.yaml -n=200
./plot_dose.py
```

<br/>

## Geometry

The geometry is defined declaratively in `stls/cad__default.yaml` and uploaded into `gemc.db` by
`cad.py`.

The CAD system named %%stls%% contains:

- %%heart_NIH3D%%, a blood-material heart mesh.
- %%respiratory_NIH3D%%, a translucent lung mesh made with %%G4_LUNG_ICRP%%.
- %%liver_NIH3D%%, a soft-tissue liver mesh.

Each entry in `stls/cad__default.yaml` sets the mesh file, material, color, scale, position, and
identifier. The %%system%% value must match both the `gsystem` name in `cad.yaml` and the directory
that contains the STL files. The three organs are centred on the y-axis (each centroid has
`x = z = 0`) and stacked along y, and the lung mesh — authored trachea-down — carries a 180° `rotation`
about z that turns it right-side up.

See also the [CAD Imports Documentation](/home/documentation/geometry/cad_imports) for more
information.

Interactive viewer:

<iframe
  src="/home/assets/vtkjs-viewer.html?fileURL=/home/assets/images/examples/cad/cad.vtksz"
  title="Interactive VTK.js view of the CAD organ geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## Physics List

`FTFP_BERT` is used by default, selected in the YAML file with `phys_list: FTFP_BERT`.

{% include notes/physics-list-note.md %}

<br/>

## Generator

The particle kinematics are defined in the YAML file:

```yaml
gparticle:
  - name: gamma
    p: 380*keV
    delta_p: 120*keV
    multiplicity: 300
    theta: 90*deg
    delta_theta: 90*deg
    randomThetaModel: cosine
    phi: 180*deg
    delta_phi: 180*deg
    vx: 0*mm
    vy: -140*mm
    vz: 0*mm
    delta_vx: 20*mm
    delta_vy: 20*mm
    delta_vz: 20*mm
    randomVertexModel: sphere
```

This models a clinical **Iridium-192 HDR brachytherapy source** loaded into the liver:

- **Energy** — Ir-192 emits a line spectrum (dominant lines 0.30–0.61 MeV). It is approximated here
  by photons at the ~0.38 MeV mean photon energy, smeared with `delta_p` to span the spectrum.
- **Position** — the vertex is the liver centroid in world coordinates, `(0, -140, 0) mm`, spread
  uniformly inside a ~35 mm sphere (`randomVertexModel: sphere` uses `|delta_v|` as the radius) to
  mimic the loaded dwell region. The organs are stacked along the y-axis (`x = z = 0`) with the heart
  at the origin, the liver just below it and the lungs above.
- **Direction** — isotropic 4π emission: `cosine` sampling of θ over 0–180° combined with a uniform
  φ over 0–360°.

See also the [Internal Generator Documentation](/home/documentation/generator/internal) for more
information.

<br/>

## Digitization

Each organ is configured as a %%flux%% sensitive detector in `stls/cad__default.yaml`:

```yaml
defaults:
  digitization: flux

volumes:
  - name: heart_NIH3D
    identifier: "organ: 1"
```

The %%flux%% digitization is an **event-mode** detector: it writes one output row per hit, each row
carrying the organ %%identifier%% and the deposited energy %%totEdep%%. This is what lets a single run
resolve the three organs separately.

> The built-in %%dosimeter%% digitization would also compute the dose, but it is a **run-mode**
> detector that accumulates every hit sharing its sensitive-detector name into a single summed
> record. Because all three organs share the one `dosimeter` name, they would collapse into one
> number. Using %%flux%% keeps the per-organ identity on every hit.

### Absorbed dose

`plot_dose.py` sums the deposited energy per organ and divides by the organ mass to obtain the
absorbed dose:

$$
D_{\text{organ}} = \frac{\sum_i \mathrm{totEdep}_i}{m_{\text{organ}}},
\qquad
m_{\text{organ}} = \rho \, V_{\text{mesh}}
$$

where the sum runs over the organ's hits, \\(\rho\\) is the assigned material density
(`gemc cad.yaml -printSystemsMaterials` reports 1.06, 1.04 and 1.03 g/cm³ for the blood, lung and
soft-tissue materials) and \\(V_{\text{mesh}}\\) is the CAD mesh volume (native signed volume × the
uniform `scale`³). One gray is one joule per kilogram, \\(1\,\mathrm{Gy} = 1\,\mathrm{J/kg}\\).

### Irradiation time

The simulation fires a fixed number of photons; the corresponding **real irradiation time** is the
time an Ir-192 source of activity \\(A\\) needs to emit that many photons. With a photon yield
\\(Y\\) (photons per decay) the source emits \\(R = A\,Y\\) photons per second, so for
\\(N_\gamma = N_{\text{events}} \times m\\) simulated photons (multiplicity \\(m\\)):

$$
R = A \, Y,
\qquad
t_{\text{rad}} = \frac{N_\gamma}{A \, Y}
$$

`plot_dose.py` defaults to a nominal HDR source, \\(A = 10\ \mathrm{Ci} = 3.7\times10^{11}\\) Bq, and
\\(Y = 2.3\\) photons per Ir-192 decay (the summed gamma-line intensity); both are adjustable with
`--activity` and `--yield`. Because the dose and \\(t_{\text{rad}}\\) both scale linearly with
\\(N_\gamma\\), the absorbed dose per unit treatment time (the dose rate) is
\\(D_{\text{organ}} / t_{\text{rad}}\\), and a full therapeutic dose is reached by scaling up the
photon count (equivalently, the dwell time).

See the [Dosimeter Documentation](/home/documentation/sensitivity/dosimeter) for more information.

<br/>

## Usage

### Building the detector

Use the Python script `cad.py` to upload the CAD definitions. The script reads
`stls/cad__default.yaml` and stores the setup in a SQLite file named `gemc.db`.

```shell
./cad.py
```

{% include notes/python-api-note.md %}

See also the [Building Geometry](/home/documentation/geometry/geometry_building) for more
information.

<br/>

### Running GEMC

The file `cad.yaml` can be used to run the setup. Add `-gui` to run interactively:

```shell
gemc cad.yaml -gui
```

Modify `cad.yaml` as needed, in particular to add particles, control the number of threads, or
change the output.

<br/>

## Running Events

{% include figure.html
src="assets/images/examples/cad/gemc_view.png"
caption="CAD simulation: an Iridium-192 brachytherapy source inside the liver emits photons
isotropically, depositing dose in the imported liver, heart, and lung meshes."
%}

<br/>

## Output

The %%gstreamer%% option selects the output filename and format:

```yaml
gstreamer:
  - format: csv
    filename: organs
```

{% include notes/output-note.md %}

See also the [Output Documentation](/home/documentation/output) for more information.

<br/>

## Plotting the dose in each organ

Run GEMC first so the flux CSV streams are written (more events give the organs-at-risk better
statistics):

```shell
gemc cad.yaml -n=200
```

Then plot the per-organ dose with `plot_dose.py`. It reads `organs_t0_digitized.csv`, prints the
deposited energy, mass and dose per organ, and draws the bar chart:

```shell
./plot_dose.py                       # nominal 10 Ci Ir-192 source
./plot_dose.py --activity 5          # a weaker 5 Ci source (rescales the irradiation time)
./plot_dose.py --save organs_dose.png
```

![cad dose per organ][cad-dose_per_organ]{:width="70%"}

The liver, which hosts the source, absorbs by far the largest dose; the heart just above it and the
lungs at the top of the stack receive a much smaller scattered dose — the localisation that makes
brachytherapy attractive. The title reports the Ir-192 irradiation time that the simulated photon
count represents (see [Irradiation time](#irradiation-time) above).

[cad-dose_per_organ]: /home/assets/images/examples/cad/dose_per_organ.png


## Plotting with the GEMC Analyzer

`plot_dose.py` above gives the per-organ dose. For a quick look at the raw flux output you can also
use the generic `gemc-analyzer`. Run GEMC first so the CSV streams are written:

```shell
gemc cad.yaml -n=200
```

Histogram the per-hit deposited energy %%totEdep%% (the flux stream records `totEdep`, not `dose`):

```shell
gemc-analyzer organs_t0_digitized.csv totEdep --kind csv
```

![cad total energy deposit][cad-analyzer_totEdep]{:width="70%"}

The analyzer colours the histogram by particle id: most of the energy is deposited by secondary
electrons (`pid 11`) set in motion by the Ir-192 photons (`pid 22`).

[cad-analyzer_totEdep]: /home/assets/images/examples/cad/analyzer_totEdep.png
