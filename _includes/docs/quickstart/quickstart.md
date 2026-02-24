


## The main script

The relevant lines in `counter.py` are:

```python
def main():
	configuration = GConfiguration('examples', 'counter')

	define_materials(configuration)
	build_counter(configuration)
	configuration.printC()
```

The first one declare the `counter` system inside the `examples` experiment. See also [systems documentation](../../docs/systems/) for more details.

The second and third lines call functions defined in `materials.py` and `geometry.py` to create the materials and geometry. Let's take a look at them.


## geometry.py

The `build_counter` function creates the geometry by calling these `build_flux_box` and `build_target` functions:

```python
def build_flux_box(configuration):
	gvolume = GVolume('absorber')
	gvolume.description = 'carbon fiber box'
	gvolume.make_box(40.0, 40.0, 2.0)
	gvolume.material    = 'carbonFiber'
	gvolume.color       = '3399FF'
	gvolume.style       = 1
	gvolume.digitization = 'flux'
	gvolume.set_position(0, 0, 100)
	gvolume.set_identifier('box', 2)  # identifier for this box
	gvolume.publish(configuration)

def build_target(configuration):
	gvolume = GVolume('target')
	gvolume.description = 'epoxy target'
	gvolume.make_tube(0, 20, 40, 0, 360)
	gvolume.material    = 'epoxy'
	gvolume.publish(configuration)
```

Notice how the `flux` digitization is assigned to the flux box and how `make_box` and `make_tube` are used to create the shapes. 
See also [geometry documentation](../../docs/geometry/) for more details. The two materials have custom names: they are defined in `materials.py`.

Notice the absence of solid, logical, and physical volumes: GEMC handles all of that internally. 

<br/>


## materials.py


