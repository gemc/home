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
		<h4><a href="/home/{{ post.url }}">{{ post.title }}</a>: {{ post.description }}</h4>
	</li>
	{% endfor %}
		
</ul>
