---
layout: default
title: Documentation
permalink: /Documentation/
---

<ul>

	{% assign pages_list = site.documentation | sort: 'order' %}
	{% for post in pages_list %}
		{% if post.url contains 'Docs' %}
			{% continue %}
		{% endif %}
	<li>
		<h5><a href="/home/{{ post.url }}">{{ post.title }}</a></h5>
		{{ post.description }}<br/><br/>
	</li>
	{% endfor %}
	
	
</ul>
