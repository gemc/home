<blockquote class="doc-important" markdown="1">
**phys_list**

The physics list can be selected using the option
```
gemc -phys_list <value>
```
where `<value>` can be a combination of the Geant4 physics constructors separated by the `+` sign. For example
```
gemc -phys_list="FTFP_BERT + G4NeutronCrossSectionXS"
```
To see a list of the available Geant4 constructors:
```
gemc -showPhysics
```
</blockquote>