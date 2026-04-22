
> **NOTE**
>
> The `gparticle` option allows to control the Geant4 particle gun. 
> For the complete list of parameter that can be passed to it: 
> 
> `gemc help gparticle`. 
>
> Some of them:
> - name: Particle name (mandatory),  for example "proton".
> - multiplicity: How many copies of this particle will be generated in each event. 
> - p: Particle momentum. 
> - delta_p: Particle momentum range, centered on p.. Default value: 0
> - theta: Particle polar angle. 
> - delta_theta: Particle polar angle range, centered on theta. . Default value: 0
> - phi: Particle azimuthal angle. . Default value: 0
>
>
> For example, to define a particle gun with 5 identical electrons along z and 1 proton at theta=30,phi=90 degrees, use
> 
>   - Command line:
>     
>           -gparticle="[{name: e-, p: 5000, multiplicity: 5}, {name: proton, p: 2000, theta: 30, phi: 90}]"
> 
>   -  Yaml:
>   
>           particle:
>            - name: e-
>              p: 5000
>              multiplicity: 5
>            - name: proton
>              p: 2000
>              theta: 30
>              phi: 90
{: .doc-important }


