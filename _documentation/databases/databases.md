---
layout: default
title: Databases
order: 2
description: Databases in GEMC
---

# GEMC Databases

The detectors parameters are stored in databases. This includes:

- Native Geant4 volumes
- Cad imports definitions
- Materials, including optical properties
- Optical surfaces
- Sensitivity parameters

The supported databases are:

 <ul>
	{% for db in site.data.supported_db %}
	<li> <b>{{ db.name}}</b>: 
 		<ul>
			<li> {{ db.description }}</li>
			<li> {{ db.detail }}</li>
			<li> Created by default: {{ db.default }}<br/><br/></li>
 		</ul>
	</li>
	{% endfor %}
</ul>


