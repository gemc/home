<blockquote class="doc-important" markdown="1">

**flux**

The `flux` digitization collects all `G4Steps` into hits by using the track id: all steps within a
sensitive element produced by the same track define a single hit. Different tracks' steps in the
same sensitive element are collected in separate hits. 
This digitization can be used to count and analyze the tracks passing through a volume.

{% include figure.html
src="assets/images/documentation/flux_hit_definition.png"
caption="Flux hit definition example: three tracks goes through two sensitive cells. <br/>

Track 1 creates two hits: < cell2, hit #1 > and < cell1, hit #1 >.<br/>

Track 2 creates two hits: < cell1, hit #2 > and < cell2, hit #2 >.<br/>

Track 3 creates one hit: < cell2, hit #3 >.<br/>

"
%}

The variables stored in the digitized output are:

- the sensitive element `identifier`, assigned by the user. For example
  - sector
  - layer
- `hitn`: hit number
- `pid`: particle id
- `tid`: track id
- `E`: track energy
- `time`: time of the hit
- `totEdep`: total energy deposited by the track




</blockquote>