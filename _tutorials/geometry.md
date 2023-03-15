---
layout: documentation
title: Geometry
order: 1
description: Tutorial on building detectors
---


{% assign pages_list = site.tutorials | where_exp: "item" , "item.path contains 'geometryTuts'" %}
{% for post in pages_list %}
<h5><a href="/home/{{ post.url }}">{{ post.title }}</a></h5> {{post.description}}
{% endfor %}
