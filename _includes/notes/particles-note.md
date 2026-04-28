<blockquote class="doc-important" markdown="1">
**gparticle**

The `gparticle` option allows to control the Geant4 particle gun. 
For the complete list of parameter that can be passed to it: `gemc help gparticle`. 

Some of them: 
- `name`: Particle name (mandatory),  for example "proton".
- `multiplicity`: How many copies of this particle will be generated in each event. 
  notice that the copies are not identical if some additional parameters are specified, 
  for example delta_p, delta_theta. 
- `p`: Particle momentum. 
- `delta_p`: Particle momentum range, centered on p.
- `theta`: Particle polar angle. 
- `delta_theta`: Particle polar angle range, centered on theta. D
- `phi`: Particle azimuthal angle. 

For example, to define a particle gun with one electron along z plus 1 proton at theta=30,phi=90 degrees, use

- Command line:
     
      -garticle="[{name: e-, p: 5000}, {name: proton, p: 2000, theta: 30, phi: 90}]"
 
- Yaml:
	   
       particle:
        - name: e-
          p: 5000
          multiplicity: 5
	    - name: proton
		  p: 2000
		  theta: 30
		  phi: 90

</blockquote>

