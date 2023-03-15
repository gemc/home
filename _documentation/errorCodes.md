---
layout: default
title: Exit Codes
description: gemc exit codes with one string description
order: 10
---

 <ul>
	{% for ecode in site.data.gemcEC %}
	<li> {{ ecode.name}}: {{ ecode.code }}</li>
	{% endfor %}
</ul>

