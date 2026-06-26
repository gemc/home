---
layout: default
title: "Scintillator Barrel"
---
{% include directory.html data=site.data.examples columns=5 section_breaks=4 exclude_title="Quickstart" %}


# Scintillator Barrel
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

This example builds a cylindrical scintillator barrel detector made of 48 trapezoidal paddles
arranged in a complete ring. It demonstrates the `distribute_on_circle` API to replicate a
volume at equal angular intervals around a circle and shows how to size the paddles so that
adjacent faces are nearly contiguous.


{% assign example = site.data.examples | where: "title", "Scintillator Barrel" | first %}
You can run this example in your browser: [![{{ example.title }}]({{ example.badge }})]({{ example.binder }}){:target="_blank" rel="noopener noreferrer"} 

<br/>

## Quickstart

Copy the example to your current directory.
To create the geometry and run 3 events:

```shell
cp -r $GEMC_HOME/examples/basic/scintillator_barrel .
cd scintillator_barrel
./scintillator_barrel.py
gemc scintillator_barrel.yaml
```

<br/>

## Geometry

The geometry is defined in `scintillator_barrel.py`. The world (a box named %%root%%) contains
48 identical %%paddle%% volumes arranged in a ring:

- Each %%paddle%% is a `G4Trap` general trapezoid (%%G4_PLASTIC_SC_VINYLTOLUENE%%) with its
  wider face pointing radially outward and its narrower face toward the beam axis.
- The paddles are sized with the chord formula so that adjacent outer faces are contiguous:
  - outer half-width: `pX  = (radius + pY) × sin(π/n)`
  - inner half-width: `pLTX = (radius − pY) × sin(π/n)`
- `distribute_on_circle(n=48, radius=400 mm, align=True, axis='z')` places and rotates each
  copy around the z axis with equal 7.5° steps.

See the [Structure Helpers](/home/documentation/geometry/structure) documentation for the full
`distribute_on_circle` API reference and the sizing geometry.

Interactive viewer (full 48-paddle barrel):

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}/assets/images/examples/scintillator_barrel/scintillator_barrel.vtksz"
  title="Interactive VTK.js view of the scintillator_barrel geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## Physics List

`QBBC` is used by default, selected in the YAML file with `phys_list: QBBC`.

{% include notes/physics-list-note.md %}

<br/>

## Generator

The particle kinematics are defined in the YAML file:

```yaml
gparticle:
  - name: proton
    p: 500*MeV
    theta: 90*deg
    delta_phi: 360*deg
    multiplicity: 3
```

See also the [Internal Generator Documentation]( /home/documentation/generator/internal ) for more information.

<br/>

## Digitization

Each %%paddle%% is assigned the %%flux%% digitization with a unique paddle identifier:

```python
paddle.digitization = "flux"
# ...
v.set_identifier("paddle", i)
```

See the [Flux Documentation]( /home/documentation/sensitivity/flux ) for more information.

<br/>

## The `distribute_on_circle` API

The `distribute_on_circle` method on `GVolume` replicates the template volume `n` times
around a circle of the given `radius`. With `align=True`, each copy is additionally rotated
around the chosen axis by its angular position φᵢ, keeping each paddle's local frame aligned
radially:

```python
for i, v in enumerate(paddle.distribute_on_circle(n, radius, align=True, axis='z')):
    v.set_identifier("paddle", i)
    v.publish(cfg)
```

The method returns a list of independent `GVolume` copies, one per angular step, each named
`<name>_i` and positioned at `(radius·cos φᵢ, radius·sin φᵢ, 0)`.
Full API reference in the [Structure Helpers](/home/documentation/geometry/structure) documentation.

<br/>

## Usage

### Building the detector

Use the Python script `scintillator_barrel.py` to build the detector. By default, the setup
is stored in a SQLite file named `gemc.db`. Command-line options can define the database type,
variations, and run number.

See also the [Building Geometry]( /home/documentation/geometry/geometry_building ) for more information.

<br/>

### Running GEMC

The file `scintillator_barrel.yaml` runs the simulation. Add `-gui` to run interactively:

```shell
gemc scintillator_barrel.yaml -gui
```

Modify `scintillator_barrel.yaml` as needed, in particular to change the number of events,
add threads, or select output formats.

<br/>

## Running Events

The view below shows the barrel end-on after one event, with 3 protons fired radially
outward at θ = 90°. Each proton traverses one scintillator paddle.

{% include figure.html
src="assets/images/examples/scintillator_barrel/gemc_view.png"
caption="Scintillator barrel viewed end-on along the beam axis. Three protons at θ = 90°
travel radially outward, each depositing energy in one paddle."
%}

<br/>

## Output

The %%gstreamer%% option selects the output filenames and the format:

```yaml
gstreamer:
  - format: csv
    filename: barrel
```

See also the [Output Documentation]( /home/documentation/output ) for more information.

<br/>

## Plotting with the GEMC Analyzer

Run GEMC with 1,000 events first. The default YAML file writes the analyzer CSV streams.

```shell
gemc scintillator_barrel.yaml -n=1000
```

Plot the total energy deposited per hit:

```shell
gemc-analyzer barrel_t0_digitized.csv totEdep --kind csv
```

![Scintillator Barrel total energy deposited per hit](/home/assets/images/examples/scintillator_barrel/analyzer_totEdep.png){:width="70%"}

Plot the true particle track energy:

```shell
gemc-analyzer barrel_t0_true_info.csv E --kind csv --data true_info
```

![Scintillator Barrel true particle track energy](/home/assets/images/examples/scintillator_barrel/analyzer_true_energy.png){:width="70%"}
