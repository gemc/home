---
layout: default
title: Quickstart
permalink: /documentation/quickstart/
---


<br/>


# Quickstart

1. Using the python API, create a simple geometry consisting of a target and a `flux` detector. 
2. Shoot protons at the target and count how many tracks cross the detector.

<br/>


## Create a system

We could write a simple python script from scratch to define the geometry and materials, 
but the GEMC api comes with template creators that facilitate this considerably.
Let's use it to make a **system**, named _counter_. <br/>

In a directory of your choice, the following command 
will make a subdir called `counter` containing template scripts for geometry and materials:

```shell 
system_template.py -s counter
```

You should see the following output:


```text
 Writing files for experiment >examples<, system template >counter< using variations >['default']<:

  - counter.py
  - geometry.py
  - materials.py
  - README.md

  - Variations defined in counter.py:
    * default
```

The files are already configured to create the geometry with a target and a `flux` detector. 
By default, a `yaml` card is provided to shoot protons at the target.

Use `-h` to see other options for `system_template.py`.

<br/>

## Build the geometry

Inside the `counter` directory, run `counter.py` to create the geometry and materials databases:

```shell
./counter.py
```

You should see the following output:

```text

  ❖ Database file gemc.db does not exist
  ❖ Created new SQLite database: gemc.db

  ❖  GConfiguration for experiment <examples>,  system <counter> : 
	▪︎ Factory: sqlite         
	▪︎ SQLite File: gemc.db
	▪︎ (Variation, Run): (default, 1)
	▪︎ Number of volumes: 2
	▪︎ Number of materials: 2

```

By default, the `sqlite` factory is used, so an sqlite file `gemc.db` is been created containing 
the geometry and materials. 

The geometry is created for the defaults run number `1` and variation `default`. 
Use `-h` to see other options.

<br/>

## Run gemc

Use the `counter.yaml` steering card and run `GEMC` in interactive mode using `-gui`:

```shell
gemc counter.yaml -gui
```

You will see the gemc GUI window. Click the Run button (top left) to start the simulation. 
You should see 100 particles being generated and crossing the flux box, producing red hits.

{% include figure.html
   src="assets/images/documentation/quickstart_flux.png"
   alt="The quickstart example"
   caption="A proton beam impinging on an epoxy target. The flux box collects hits from the tracks crossing it."
%}

Use GEMC without the `-gui` option to run it in batch mode.

<br/>

## Output 

The yaml file specify the `ascii` format and an output file name `counter`.
After running gemc you will see files with the `_t<T>` string appended to them, where `T` is 
the thread used for those events. 

The `ascii` files contain both `true information` and `digitized` hits from the tracks. 
For example:



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

Change the format to `root` in the yaml card to use `ROOT` output instead.

<br/>
<br/>

# More Details

Let's dig in some of the code for more insight.

<br/>

## The main script: `counter.py`


The relevant lines in `counter.py` are:

```python
cfg = autogeometry('examples', 'counter')

define_materials(cfg)
build_counter(cfg)
```

The first one declare the `counter` system inside the `examples` experiment. 

The second and third lines call methods defined in 
`materials.py` and `geometry.py` to create the materials and geometry. Let's take a look at them.

<br/>

## Defining the geometry: `geometry.py`

The `build_counter` function creates the geometry by calling these `build_flux_box` and `build_target` functions:

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

Notice how the `flux` digitization is assigned to the flux box and how the utilities `make_box` and `make_tube` are 
used to create the shapes. 

The materials associated with the flux_box and the target have custom names: they are defined in `materials.py`.

Notice the absence of `G4VSolid`, `G4LogicalVolume`, `G4PVPlacement`, `G4Material`, etc definitions: 
GEMC handles the building of those objects based on the database entries filled with the functions above. 


<br/>


## Define the materials: `materials.py`

The `define_material` method creates the `epoxy` and `carbonFiber` materials used by the geometry:

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
<br/>


> [!NOTE]
> The code created by  `system_template.py` could have easily be 
> contained in `counter.py`. Here we are showing how geometry and materials
> can be organized in separate files and methods.

<br/>

## The steering card: `counter.yaml`

In GEMC, the simulation parameters can be passed through a steering card and/or command line options.
In both cases `YAML` is used. For this example:


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

Notice how the Geant4 world volume `root` is defined dynamically in the steering card. 
It could also be defined in the geometry scripts.


<br/><br/>

