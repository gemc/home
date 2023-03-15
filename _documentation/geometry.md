---
layout: default
title: Geometry
order: 1
description: Build detectors, assign sensitivity.
---

A detector in gemc is composed by one or more *sytems*, each a hierarchical collection of volumes. 
In the example below, a forward and a central detector are defined, each composed by a set of volumes.

<ul style='list-style-type: "⦿ ";'>
	 <ul style='list-style-type: "❖ "'>
		<li>Forward detector
	 <ul style='list-style-type:square'>
			<li>calorimeter
			<ul style='list-style-type: "‣ ︎"'>
				<li>paddle 1
				</li>
				<li>paddle 2
				</li>
				<li>...
				</li>
			</ul>
			</li>
		</ul>
		</li>
		<li>Central Detector
	 <ul style='list-style-type:square'>
			<li>Time Of Flight
			<ul style='list-style-type: "‣ ︎"'>
				<li>scintillator 1
				</li>
				<li>...
				</li>
			</ul>
			</li>
			<li>Cerenkov
			<ul style='list-style-type: "‣ ︎"'>
				<li>mirror 1
				</li>
				<li>...
				</li>
			</ul>
			</li>
		</ul>
		</li>
	</ul>
</ul>

The volumes can be geant4 objects built using the [sci-g python api](https://github.com/gemc/sci-g) or imported from CAD / GDML.

<br/>

<h4> How to create a system and add volumes to it</h4>

<br/>


[//]: # ({% assign pages_list = site.documentation | where_exp: "item" , "item.path contains 'geometryDocs'" | sort: 'order' %})

[//]: # ({% for post in pages_list %})

[//]: # (<li><a style="font-size:16px;" href="/home/{{ post.url }}">{{ post.title }}</a>: {{post.description}}</li>)

[//]: # ({% endfor %})
