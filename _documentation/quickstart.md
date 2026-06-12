---
layout: default
title: Quickstart
permalink: /documentation/quickstart/
---

# Quickstart

This quickstart walks through a minimal but complete GEMC simulation:

1. Generate a geometry system with a target and a %%flux%% detector using `gemc-system-template`.
2. Build the geometry database with Python.
3. Shoot protons at the target and count the tracks crossing the detector.

<br/>

## Create a system

Run `gemc-system-template` from a directory of your choice to create a `counter/` subdirectory
with ready-to-run geometry and materials scripts:

```shell
gemc-system-template -s counter
```

The command prints the list of generated files:

<pre>
Writing files for experiment &gt;examples&lt;, system template &gt;counter&lt; using variations &gt;['default']&lt;:

  - counter.py
  - geometry.py
  - materials.py
  - README.md

  - Variations defined in counter.py:
    * default
</pre>

The generated files define a geometry with a methane-gas target and a %%flux%% detector,
and include a YAML steering card that shoots protons at the target.

To see all available options:

```shell
gemc-system-template -h
```

<br/>

## Build the geometry

Go into the `counter` directory and run `counter.py` to write the geometry and materials to a SQLite database:

```shell
cd counter
./counter.py
```

The script creates `gemc.db` in the current directory and reports what it stored:

<pre>
  ❖ Database file gemc.db does not exist
  ❖ Created new SQLite database: gemc.db

  ❖  GConfiguration for experiment &lt;examples&gt;,  system &lt;counter&gt; :
	▪︎ Factory: sqlite         
	▪︎ SQLite File: gemc.db
	▪︎ (Variation, Run): (default, 1)
	▪︎ Number of volumes: 2
	▪︎ Number of materials: 2
</pre>

<br/>

> [!NOTE]
> Add `-pv` or `-pvb` to display the geometry interactively as it is built (requires PyVista).
> 
> Interactive view:

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}/assets/images/documentation/counter.vtksz"
  title="Interactive VTK.js view of the counter geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>


<br/>

## Run GEMC

Use the `counter.yaml` steering card to run the simulation. Add `-gui` for the interactive Geant4 viewer:

```shell
gemc counter.yaml -gui
```

Click **Run** in the Geant4 GUI to start the simulation. With `n: 100` events and a proton beam
aimed along the z-axis, all 100 tracks should cross the flux detector. Hits are highlighted in red.

{% include figure.html
src="assets/images/documentation/quickstart_flux.png"
alt="The quickstart example"
caption="A proton beam impinging on the target. The flux box collects hits from tracks crossing it."
%}

To run in batch mode:

```shell
gemc counter.yaml
```

<br/>

## Plot total energy deposited

Run 10,000 events to get good statistics:

```shell
gemc counter.yaml -n=10000
```

Plot the digitized %%totEdep%% variable: the total energy deposited in each %%flux%% hit.

```shell
gemc-analyzer counter_t0_digitized.csv totEdep --kind csv --bins 50
```

{% include figure.html
src="assets/images/documentation/quickstart_totEdep.png"
alt="Quickstart total energy deposited histogram"
caption="Total energy deposited in the flux detector for 10,000 generated protons."
%}

<br/>

## Output

The YAML steering card writes two output formats: %%csv%% and %%json%%. Output filenames include
%%_t<T>%%, where %%T%% is the thread number, for example %%counter_t0_digitized.csv%% and %%counter_t0.json%%.

The CSV format produces several files per thread:

- %%counter_t0_digitized.csv%% — digitized hit variables (one row per hit)
- %%counter_t0_true_info.csv%% — raw Geant4 true information (one row per step)
- %%counter_t0_generated.csv%% — all generated particles (one row per particle)
- %%counter_t0_generated_tracked.csv%% — all generated particles that are tracked in the simulation

An example of digitized row:

<div class="csv-preview-wrap" markdown="0">
  <table class="csv-preview">
    <thead>
      <tr>
        <th>evn</th>
        <th>timestamp</th>
        <th>thread_id</th>
        <th>detector</th>
        <th>hitn</th>
        <th>pid</th>
        <th>tid</th>
        <th>E</th>
        <th>time</th>
        <th>totEdep</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>0</td>
        <td>Wed 05.20.2026 06:59:52</td>
        <td>0</td>
        <td>flux</td>
        <td>0</td>
        <td>2212</td>
        <td>1</td>
        <td>1769.26</td>
        <td>0.58366</td>
        <td>0.000164249</td>
      </tr>
    </tbody>
  </table>
</div>

The JSON format keeps all hits for each event in a single file per thread (`counter_t0.json`):

```json
{
  "type": "event",
  "events": [
    {
      "event_number": 0,
      "header": {
        "timestamp": "Wed 05.20.2026 07:09:10",
        "thread_id": 0,
        "g4local_event": 0,
        "generated": {
          "generated": [
            {
              "name": "proton",
              "pid": 2212,
              "type": 1,
              "multiplicity": 1,
              "p": 1500,
              "theta": 0,
              "phi": 0,
              "vx": 0,
              "vy": 0,
              "vz": -50
            }
          ]
        },
        "detectors": {
          "flux": {
            "true_info": [ { "address": "box->2", "vars": { ... } } ],
            "digitized": []
          },
          "digitized_by_detector": {
            "flux": [
              {
                "address": "box->2",
                "vars": {
                  "hitn": 0, "pid": 2212, "tid": 1,
                  "E": 1769.26, "time": 0.58366, "totEdep": 0.000164249
                }
              }
            ]
          }
        }
      }
    }
  ]
}
```

{% include notes/output-note.md %}

<br/>

# More details

The following sections explain the main files in more detail.

<br/>

## The main script: `counter.py`

`counter.py` declares the system and delegates geometry and material construction to two helper modules:

```python
cfg = autogeometry('examples', 'counter')

define_materials(cfg)
build_counter(cfg)
```

`autogeometry` declares the %%counter%% system inside the %%examples%% experiment and returns the
configuration parameters passed to the builders.

<br/>

## Defining the geometry: `geometry.py`

`build_counter` creates two volumes: a cylindrical methane-gas target and a rectangular %%flux%% detector:

```python
def build_flux_box(configuration):
    gvolume = GVolume('flux_box')
    gvolume.description = 'air flux box'
    gvolume.make_box(40.0, 40.0, 2.0)
    gvolume.set_position(0, 0, 100)
    gvolume.material    = 'G4_AIR'
    gvolume.color       = '3399FF'
    gvolume.style       = 1
    gvolume.digitization = 'flux'
    gvolume.set_identifier('box', 2)
    gvolume.publish(configuration)

def build_target(configuration):
    gvolume = GVolume('target')
    gvolume.description = 'methane gas target'
    gvolume.make_tube(0, 20, 40, 0, 360)
    gvolume.material    = 'methaneGas'
    gvolume.publish(configuration)
```

`make_box` and `make_tube` are helper methods that set the solid type and parameters in one call.
The %%flux_box%% volume is assigned the %%flux%% digitization, which records a hit for every track that crosses it.

No Geant4 C++ objects (`G4VSolid`, `G4LogicalVolume`, `G4PVPlacement`, etc.) appear in the script.
GEMC constructs them internally from the database entries written by `publish`.

<br/>

## Defining the material: `materials.py`

The target uses a custom %%methaneGas%% material defined by atom count:

```python
gmaterial = GMaterial("methaneGas")
gmaterial.description = "methane gas CH4 0.000667 g/cm3"
gmaterial.density = 0.000667
gmaterial.addNAtoms("C", 1)
gmaterial.addNAtoms("H", 4)
gmaterial.publish(configuration)
```

<br/>

> [!NOTE]
> The code generated by `gemc-system-template` could all live in `counter.py`. Splitting into
> `geometry.py` and `materials.py` is a convention that keeps larger projects readable.

<br/>

## The steering card: `counter.yaml`

```yaml
runno: 1
n: 100               # number of events

nthreads: 1          # single thread → one output file per format

gparticle:
  - name: proton
    p: 1500*MeV      # momentum
    vz: -5*cm        # vertex z, just before the target

verbosity:
  - gsystem: 1

gsystem:
  - name: counter
    factory: sqlite  # read geometry from gemc.db

gstreamer:
  - filename: counter
    format: csv
  - filename: counter
    format: json

root: G4Box, 15*cm, 15*cm, 15*cm, G4_AIR   # world volume
```

Remove `nthreads: 1` to use all available cores; each thread writes its own output file. Add a
%%gstreamer%% entry with %%format: root%% for ROOT output.

The %%root%% entry defines the Geant4 world volume inline in the steering card.
%%root%% could also be defined in the geometry scripts.
