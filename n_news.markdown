---
layout: default
title: News
permalink: /news/
---

# News

{% for post in site.posts %}
## [{{ post.title }}]({{ post.url | relative_url }})

<small>{{ post.date | date: "%B %-d, %Y" }}</small>

{{ post.excerpt }}

[Read more]({{ post.url | relative_url }})

---
<br/>

{% endfor %}