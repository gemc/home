---
layout: default
title: Sensitive Scintillator Array
directory: $SCIG/examples/scintillator_array
---

The setup is an array of scintillator bars in a cylindrical configuration.
The bars are trapezoids to maximize the surface area.

The geometry is constructed using the python script:

	./scintillator_array.py

<br/>

The output is defined by the entry `+goutput` in the jcard 'scintillator_array.jcard'.
Two format are written out: 'text' and 'root'.

Sets the desired number of cores, number of events, and verbosity in the jcard 'scintillator_array.jcard'. To run gemc:

	gemc scintillator_array.jcard 

Use the `-gui` option to run interactively:

	gemc simple_flux.jcard -gui

The geometry looks like this:

![scint_array]{:width="70%"}

<br/>

Another picture with 1000 events leaving hit in the sensitive bars:

![scint_hits]{:width="70%"}


After running, the produced root file can be inspected:

	root
	TFile f("events.root")
	f.ls()

This will show the following branches in the output file:
	
- header:	GEMC Root Event Header
- trueInfo_flux: True Info Data Root Tree
- digitized_flux: Digitized Data Root Tree
  
The variables' names in each branch can be listed and plotted. For example:

	digitized_flux->Print()
    digitized_flux->Draw("eTot:bar_id>>(37, 0, 38, 100, 20.0, 20.6)", "eTot>20", "colz")
    trueInfo_flux->Draw("avgy:avgx>>(400, -400, 400, 400, -400, 400)", "", "colz")

will show the energy deposited in the bars versus bar id and the hit positions in the x-y plane:

[![eTot_vs_bar_id]{:width="70%"}]

[![avgy_vs_avgx]{:width="70%"}]


The code that produce the geometry:

<script src="https://gist.github.com/maureeungaro/2a3f64a684f2d9d1891b4bf5a0edcc60.js"></script>

[scint_array]: /home/assets/images/examples/scintillator_array/geometry.png
[scint_hits]: /home/assets/images/examples/scintillator_array/geometry_and_hits.png
[eTot_vs_bar_id]: /home/assets/images/examples/scintillator_array/eTot_vs_bar_id.png
[avgy_vs_avgx]: /home/assets/images/examples/scintillator_array/avgy_vs_avgx.png
