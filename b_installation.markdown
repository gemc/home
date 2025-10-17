---
layout: default
title: Installation
permalink: /installation/

development_tag: dev3
development_release_date: <small><time>released nightly</time></small>
latest_tag: 1.0
latest_release_date: <small><time>Not Yet Released</time></small>
repo_link: https://github.com/gemc/src/releases/tag
release_notes: https://github.com/gemc/src/releases
path_prefix: /path/to/gemc
docker_local_mount: ~/mywork
docker_remote_mount: /mywork
---

{% include mynotes.html %}


### License

See the [license conditions](/home/license/).

<br/>

### Release Notes


- [`development`]({{ page.release_notes }}/tag/{{ page.development_tag }}) - {{ page.development_release_date }}{: .meta }
- [`{{ page.latest_tag }}`]({{ page.release_notes }}/tag/{{ page.latest_tag }}) - {{ page.latest_release_date }}{: .meta }
- [`All Releases`]({{ page.release_notes }})

<br/>

> [!NOTE] 
> Use the most recent GEMC release to ensure you are taking  advantage of
> latest bug fixes and the new features. This also helps the developers to provide the best support.

<br/><br/>


## Table of Contents
 
- [Build and Install GEMC from source code](#build-and-install-gemc-from-source)
- [Run GEMC in a Docker Container](#run-gemc-in-a-docker-container)



<br/><br/>

{% include docs/installation/build.md %}

<br/><br/>


{% include docs/installation/docker.md %}

<br/><br/><br/><br/><br/>

# Appendix
<hr/>
<br/>

{% include docs/installation/pre-requisites.md %}


<br/>
<br/>
<br/>


