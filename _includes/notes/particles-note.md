<blockquote class="doc-important" markdown="1">
**gparticle**

The `gparticle` option controls the Geant4 particle gun.
For the complete list of parameters that can be passed to it: `gemc help gparticle`. 

Common parameters:
- `name`: particle name (mandatory), for example `proton`
- `multiplicity`: number of copies generated in each event.
  The copies are not identical if additional spread parameters are specified,
  for example `delta_p` or `delta_theta`.
- `p`: particle momentum
- `delta_p`: particle momentum range, centered on `p`
- `theta`: particle polar angle
- `delta_theta`: particle polar angle range, centered on `theta`
- `phi`: particle azimuthal angle

For example, to define a particle gun with one electron along z plus one proton at `theta=30` and `phi=90` degrees, use:

- Command line:
     
      -garticle="[{name: e-, p: 5000}, {name: proton, p: 2000, theta: 30, phi: 90}]"
 
- YAML:
	   
       particle:
        - name: e-
          p: 5000
          multiplicity: 5
	    - name: proton
		  p: 2000
		  theta: 30
		  phi: 90

</blockquote>
