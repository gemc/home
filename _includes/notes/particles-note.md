<blockquote class="doc-important" markdown="1">
**gparticle**

The `gparticle` option controls the Geant4 particle gun.
For the complete list of parameters: `gemc help gparticle`.

Common parameters:
- `name`: particle name (mandatory), e.g. `proton` or `e-`
- `multiplicity`: number of copies generated per event;
  copies are independently randomized when spread parameters such as `delta_p` or `delta_theta` are set
- `p`: particle momentum with unit, e.g. `4*GeV` or `4000*MeV`
- `delta_p`: momentum spread, centered on `p`
- `theta`: polar angle with unit, e.g. `23*deg` or `0.4*rad`
- `delta_theta`: polar-angle spread, centered on `theta`
- `phi`: azimuthal angle with unit, e.g. `90*deg`

Kinematic values accept an explicit Geant4 unit (`value*unit`). A plain number without
a unit falls back to MeV for momentum, deg for angles, and cm for vertex coordinates,
with a logged warning.

For example, to define a particle gun with one electron along z plus one proton at θ = 30° and φ = 90°:

- Command line:

      -gparticle="[{name: e-, p: 5*GeV}, {name: proton, p: 2000*MeV, theta: 30*deg, phi: 90*deg}]"

- YAML:

      gparticle:
        - name: e-
          p: 5*GeV
          multiplicity: 5
        - name: proton
          p: 2000*MeV
          theta: 30*deg
          phi: 90*deg

</blockquote>
