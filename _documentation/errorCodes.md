---
layout: default
title: Exit Codes
order: 10
description: Exit codes for gemc3
---

 <ul>
	{% for ecode in site.data.gemcEC %}
	<li> {{ ecode.name}}: {{ ecode.code }}</li>
	{% endfor %}
</ul>

