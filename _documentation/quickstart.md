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

## Output

The YAML file specifies the `ascii` output format and uses `counter` as the output filename prefix.

After running GEMC, you should see output files whose names include `_t<T>`, where `T` is the thread 
number that processed those events.

The `ascii` output contains both **true information** and **digitized hits** from the tracks. For example:

```text
   Detector <flux> True Info Bank {
      Hit address: box->2 {
         avgTime: 0.589659
         avglx: -0.531997
         avgly: -0.428564
         avglz: -0.562993
         avgx: -0.531997
         avgy: -0.428564
         avgz: 99.437
         hitn: 0
         pid: 2212
         tid: 1
         totalEDeposited: 1.31941
         processName: NULL
      }
   }
   Detector <flux> Digitized Bank {
      Hit address: box->2 {
         hitn: 0
         pid: 2212
         tid: 1
         E: 1747.43
         time: 0.589659
         totEdep: 1.31941
      }
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
	gvolume.description = 'carbon fiber box'
	gvolume.make_box(40.0, 40.0, 2.0)
	gvolume.set_position(0, 0, 100)
	gvolume.material    = 'carbonFiber'
	gvolume.color       = '3399FF'
	gvolume.style       = 1
	gvolume.digitization = 'flux'
	gvolume.set_identifier('box', 2)  # identifier for this box
	gvolume.publish(configuration)

def build_target(configuration):
	gvolume = GVolume('target')
	gvolume.description = 'epoxy target'
	gvolume.make_tube(0, 20, 40, 0, 360)
	gvolume.material    = 'epoxy'
	gvolume.publish(configuration)
```

The flux box is assigned the `flux` digitization. The geometry uses the helper 
methods `make_box` and `make_tube` to define the shapes.

The materials used by the flux box and target, `carbonFiber` and `epoxy`, are custom 
materials defined in `materials.py`.

Notice that the script does not define `G4VSolid`, `G4LogicalVolume`, `G4PVPlacement`, `G4Material`, 
or related Geant4 objects directly. GEMC builds those Geant4 objects from the 
database entries created by the Python API.

<br/>

## Defining the materials: `materials.py`

The `define_materials` function creates the `epoxy` and `carbonFiber` materials used by the geometry:

```python
# example of material: epoxy glue, defined with number of atoms
gmaterial = GMaterial("epoxy")
gmaterial.description = "epoxy glue 1.16 g/cm3"
gmaterial.density = 1.16
gmaterial.addNAtoms("H",  32)
gmaterial.addNAtoms("N",   2)
gmaterial.addNAtoms("O",   4)
gmaterial.addNAtoms("C",  15)
gmaterial.publish(configuration)

# example of material: carbon fiber, defined using the fractional mass
gmaterial = GMaterial("carbonFiber")
gmaterial.description = "carbon fiber - 1.75g/cm3"
gmaterial.density = 1.75
gmaterial.addMaterialWithFractionalMass("G4_C",  0.745)
gmaterial.addMaterialWithFractionalMass("epoxy", 0.255)
gmaterial.publish(configuration)
```

The `epoxy` material is defined by specifying the number of atoms for each element. 
The `carbonFiber` material is defined using fractional masses.

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

nthreads: 4

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
    format: ascii

root: G4Box, 15*cm, 15*cm, 15*cm, G4_AIR
```

The `nthreads` entry limits the threads used to 4. Remove it to use all threads. 
To use ROOT output, change the output format in `counter.yaml` from `ascii` to `root`.

The `root` entry dynamically defines the Geant4 world volume in the steering card. 
The world volume could also be defined in the geometry scripts.
