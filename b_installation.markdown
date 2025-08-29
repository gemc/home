---
layout: default
title: Installation
permalink: /installation/
gemc_latest_docker_tag_ubuntu: ghcr.io/gemc/gemc:latest-ubuntu24
gemc_latest_docker_tag_alma: ghcr.io/gemc/gemc:latest-almalinux94
gemc_latest_docker_tag_fedora: ghcr.io/gemc/gemc:latest-fedora40
development_tag: dev3
development_release_date: <small><time>released nightly</time></small>
latest_tag: 1.0
latest_release_date: <small><time>Not Yet Released</time></small>
repo_link: https://github.com/gemc/src/releases/tag
release_notes: https://github.com/gemc/src/releases
---

{% include mynotes.html %}

<br/>

## License

See the [license conditions](/home/license/).

<br/>

## Release Notes


- [`development`]({{ page.release_notes }}/tag/{{ page.development_tag }}) - {{ page.development_release_date }}{: .meta }
- [`{{ page.latest_tag }}`]({{ page.release_notes }}/tag/{{ page.latest_tag }}) - {{ page.latest_release_date }}{: .meta }
- [`All Releases`]({{ page.release_notes }})


<br/>

---

<br/>

# Installation

> [!NOTE] 
> Always use the most recent GEMC release to ensure you are taking  advantage of
> latest bug fixes and the new features. This also helps the developer to provide the best support.

<br/>

GEMC can be installed by: 
 
- [Local compilation from source code](#build-and-install-gemc-from-source)
- [Using a docker container](#run-gemc-in-a-docker-container)


<br/>


<br/>


## Build and Install GEMC from Source

Set a `GEMC` environment variable that points to your desired installation location. Typically: `/opt/gemc` or `~/gemc`. 

We will install GEMC in it. 

```bash
  export GEMC=/opt/gemc
  mkdir -p $GEMC
```

Download the latest release source code anywhere on your system:

```bash
wget {{ page.repo_link }}/{{ page.latest_tag }}.tar.gz
```

Alternatively, clone the repository to get the latest development version:
```bash
git clone https://github.com/gemc/src
```





The [meson build system](https://mesonbuild.com) is used to compile and install GEMC.


<br/>

---

<br/>


## Run GEMC in a Docker container

Pull the latest image:
```docker pull {{ page.gemc_container_tag }}```

It is recommended to mount a working directory to save store your work.
For example `~/mywork`.

## Run docker in batch mode[^1]:

```
docker run -it --rm -v ~/mywork:/mywork {{ page.gemc_container_tag }} bash
```


## Run docker and use a browser for the graphical interface:

```
docker run -it --rm  -v ~/mywork:/mywork  -p 8080:8080  {{ page.gemc_container_tag }}
```

(*point your browser to http://localhost:8080/vnc.html*)


[//]: # (#### run docker and use vnc[^2] for the graphical interface:)

[//]: # (> docker run -it \-\-rm  -v ~/mywork:/jlab/work/mywork  -p 127.0.0.1:6080:6080  -p 5901:5901 {{ page.gemc_container_tag }})

<br/>

---

<br/>

# Local installation through compilation[^3]

<br/>

Download the common environment and installation repo 
[ceInstall](https://github.com/jeffersonlab/ceInstall) 
to an installation location (for example: `/opt/sim`)

```
  git clone https://github.com/jeffersonlab/ceInstall
  module use ceInstall/modules
  module load sim_system
```

```
install_gemc 3.0
```

This will install gemc and the  [sci-g](https://github.com/gemc/sci-g)  python api.

#### Put in your .bashrc/.zshrc/.tcshrc file to load the env at login:

```
  export SIM_HOME=/opt/sim
  source $SIM_HOME/ceInstall/setup.(c)sh
  module load gemc3/1.0
```


For more details and system requirements check the [Common Environment Install](https://github.com/JeffersonLab/ceInstall) repository.

<br/> <br/> <br/> <br/>

---

[^1]: on linux permissions problems for /var/run/docker.sock may be solved with  ```sudo chmod 666 /var/run/docker.sock```
[^2]: recommended: <a href='https://www.realvnc.com/en/connect/download/viewer/'>realvnc vnc viewer</a>
[^3]: tested on macOS Ventura, Linux Fedora 36
