---
layout: default
title: Quickstart
permalink: /documentation/quickstart/
---

# Quickstart

This quickstart walks through a minimal GEMC simulation:

1. Use the Python API to create a simple geometry with a target and a `flux` detector.
2. Shoot protons at the target.
3. Count how many tracks cross the detector.

<br/>

## Create a system

You could write a Python script from scratch to define the geometry and materials, 
but in this example we will create a **system** named `counter` using 
the GEMC API template creators.

From a directory of your choice, run this command to create a subdirectory 
named `counter` containing template scripts for geometry and materials:

```shell
system_template.py -s counter
```

You should see this log:

<pre>

Writing files for experiment &gt;examples&lt;, system template &gt;counter&lt; using variations &gt;['default']&lt;:

  - counter.py
  - geometry.py
  - materials.py
  - README.md

  - Variations defined in counter.py:
    * default
</pre>

The generated files are already configured to build a geometry with a target and a `flux` detector. 
By default, the template also provides a YAML steering card that shoots protons at the target.

To see additional options for `system_template.py`, run:

```shell
system_template.py -h
```

<br/>


## Build the geometry

Go into the `counter` directory and run `counter.py` to create the geometry and materials databases:

```shell
./counter.py
```

You should see output similar to this:

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

By default, GEMC uses the `sqlite` factory, so this command creates a SQLite database named `gemc.db`. 
The database contains the geometry and materials for run number `1` and variation `default`.

<br/>

> [!NOTE]
> If you have `pyvista` installed, you can add the `-pv` or `-pvb` options to display the
> geometry as it is being generated. 

<br/>

To see other available options, run:

```shell
./counter.py -h
```

<br/>

## Run GEMC

Use the `counter.yaml` steering card to run GEMC, add `-gui` for interactive mode:

```shell
gemc counter.yaml -gui
```

The GEMC GUI window will open. Click the **Run** button in the top-left corner to start the simulation.

You should see 100 generated particles crossing the flux box. The hits are shown in red.

{% include figure.html
src="assets/images/documentation/quickstart_flux.png"
alt="The quickstart example"
caption="A proton beam impinging on the target. The flux box collects hits from the tracks crossing it."
%}

To run GEMC in batch mode instead, omit the `-gui` option:

```shell
gemc counter.yaml
```

<br/>

## Plot total energy deposited

The generated `counter.yaml` steering card writes CSV and JSON output. For better plotting
statistics, run 10,000 events:

```shell
gemc counter.yaml -n=10000
```

Plot the digitized `totEdep` variable, the total energy deposited in each flux hit:

```shell
python3 -m analyzer counter_t0_digitized.csv totEdep --kind csv --bins 50
```

{% include figure.html
src="assets/images/documentation/quickstart_totEdep.png"
alt="Quickstart total energy deposited histogram"
caption="Total energy deposited in the flux detector for 10,000 generated protons."
%}

<br/>

## Output

The YAML file specifies the `csv` and `json` output formats and uses `counter` as the output filename prefix.

After running GEMC, you should see output files whose names include `_t<T>`, where `T` is the thread 
number that processed those events.

The CSV output contains both **true information** and **digitized hits** from the tracks. For example,
the digitized hit file starts with:

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

The JSON output keeps the event structure in a single file per thread. For example,
`counter_t0.json` starts with:

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
          ],
          "generated_tracked": [
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
            "true_info": [
              {
                "address": "box->2",
                "vars": {
                  "avgTime": 0.58366,
                  "avglx": -0.00410225,
                  "avgly": -0.00258459,
                  "avglz": -1.6544,
                  "avgx": -0.00410225,
                  "avgy": -0.00258459,
                  "avgz": 98.3456,
                  "hitn": 0,
                  "mtid": 0,
                  "mvx": -123456,
                  "mvy": -123456,
                  "mvz": -123456,
                  "pid": 2212,
                  "tid": 1,
                  "totalEDeposited": 0.000164249,
                  "vx": 0,
                  "vy": 0,
                  "vz": -50,
                  "processName": "NULL"
                }
              }
            ],
            "digitized": []
          },
          "digitized_by_detector": {
            "flux": [
              {
                "address": "box->2",
                "vars": {
                  "hitn": 0,
                  "pid": 2212,
                  "tid": 1,
                  "E": 1769.26,
                  "time": 0.58366,
                  "totEdep": 0.000164249
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


<br/>

# More Details

The previous sections showed how to create, build, run, and inspect the quickstart example. 
This section explains the main files in more detail.

<br/>

## The main script: `counter.py`

The relevant lines in `counter.py` are:

```python
cfg = autogeometry('examples', 'counter')

define_materials(cfg)
build_counter(cfg)
```

The first line declares the `counter` system inside the `examples` experiment.

The next two lines call functions defined in `materials.py` and `geometry.py`. 
These functions create the materials and geometry used by the simulation.

<br/>

## Defining the geometry: `geometry.py`

The `build_counter` function creates the geometry by calling the `build_flux_box` and `build_target` functions:

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
	gvolume.set_identifier('box', 2)  # identifier for this box
	gvolume.publish(configuration)

def build_target(configuration):
	gvolume = GVolume('target')
	gvolume.description = 'methane gas target'
	gvolume.make_tube(0, 20, 40, 0, 360)
	gvolume.material    = 'methaneGas'
	gvolume.publish(configuration)
```

The flux box is assigned the `flux` digitization. The geometry uses the helper 
methods `make_box` and `make_tube` to define the shapes.

The flux box uses the built-in Geant4 material `G4_AIR`. The target uses the custom
`methaneGas` material defined in `materials.py`.

Notice that the script does not define `G4VSolid`, `G4LogicalVolume`, `G4PVPlacement`, `G4Material`, 
or related Geant4 objects directly. GEMC builds those Geant4 objects from the 
database entries created by the Python API.

<br/>

## Defining the material: `materials.py`

The `define_materials` function creates the custom `methaneGas` material used by the target:

```python
# example of material: methane gas, defined with number of atoms
gmaterial = GMaterial("methaneGas")
gmaterial.description = "methane gas CH4 0.000667 g/cm3"
gmaterial.density = 0.000667
gmaterial.addNAtoms("C", 1)
gmaterial.addNAtoms("H", 4)
gmaterial.publish(configuration)
```

The `methaneGas` material is defined by specifying the number of atoms for each element.

> [!NOTE]
> The code generated by `system_template.py` could be contained entirely in `counter.py`. 
> In this example, geometry and materials are organized in separate files to show a cleaner project structure.

<br/>

## The steering card: `counter.yaml`

In GEMC, simulation parameters can be passed through a steering card, command-line options, or both. 
In either case, the parameters use YAML syntax.

For this example, `counter.yaml` contains:

```yaml
runno: 1
n: 100

nthreads: 1

gparticle:
  - name: proton
    p: 1500
    vz: -5.0

verbosity:
  - gsystem: 1

gsystem:
  - name: counter
    factory: sqlite

gstreamer:
  - filename: counter
    format: csv
  - filename: counter
    format: json

root: G4Box, 15*cm, 15*cm, 15*cm, G4_AIR
```

The `nthreads` entry keeps the quickstart output in a single `counter_t0_digitized.csv`
file and a single `counter_t0.json` file. Remove it to use all threads.
To use ROOT output, add another `gstreamer` entry with `format: root`.

The `root` entry dynamically defines the Geant4 world volume in the steering card. 
The world volume could also be defined in the geometry scripts.
