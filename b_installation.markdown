---
layout: default
title: Installation
permalink: /installation/

development_tag: dev
latest_tag: 1.0
dev_tag: dev
development_release_date: <small><time>released nightly</time></small>
latest_release_date: <small><time>Not Yet Released</time></small>
repo_link: https://github.com/gemc/src
release_notes: https://github.com/gemc/src/releases
path_prefix: /path/to/gemc
docker_local_mount: ~/mywork
docker_remote_mount: /mywork
---



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
- [Run GEMC using Apptainer](#run-gemc-using-apptainer)



<br/><br/>


## Build and Install GEMC from Source

Please see the [GEMC/Geant4 Software Prerequisites](#gemc-and-geant4-software-prerequisites) in the appendix for the requirements.

<br/>

### 1. Obtain the source 

For illustration only, we will use  `{{ page.path_prefix }}` as the installation location, `{{ page.latest_tag }}` as the version to be installed,
`source` as the location of the code. Replace `{{ page.latest_tag }}` with `{{ page.dev_tag }}` for the development release.  

Create the paths and cd to the version directory:

```shell
mkdir -p {{ page.path_prefix }}/{{ page.latest_tag }}/source
cd {{ page.path_prefix }}/{{ page.latest_tag }}
```

Download the code:

{% capture tab1 %}
Download the latest release:
```shell
cd {{ page.path_prefix }}/{{ page.latest_tag }}
git clone -c advice.detachedHead=false --recurse-submodules --branch {{ page.latest_tag }} {{ page.repo_link }} source
```
{% endcapture %}

{% capture tab2 %}
At your own risk, clone the repository to get the development version:
```shell
cd {{ page.path_prefix }}/{{ page.dev_tag }}
git clone --depth=1 {{ page.repo_link }} source
```
{% endcapture %}

{% include tabs.html 
   tab1_title="Release" tab1_content=tab1
   tab2_title="GitHub Repository" tab2_content=tab2
%}






<br/>

### 2. Compile and install GEMC

The [meson](https://mesonbuild.com) build system is used to compile and install GEMC. 
A `setup` phase will check for the required dependencies and fetch external libraries.
Here we use a `build` directory inside `source`:


```shell
cd {{ page.path_prefix }}/{{ page.latest_tag }}/source
meson setup build --native-file=core.ini --prefix={{ page.path_prefix }}/{{ page.latest_tag }}
```

The compile phase will build the code and external librarie: 

```shell
meson compile -C build
```

The install phase will copy the binaries, libraries, and python modules to the installation directory:

```shell
meson install -C build
```

Optionally, after installation, `meson test -v` will run several tests of various components of GEMC. 

<br/>

### Build Options

- The setup option `-Droot=enabled` will add ROOT support (needs ROOT installed on your system).
- The setup option `-Di_test=true` will enable the GUI interfaces in the tests.
- Use `-v` at build time for verbose output.
- To wipe out the build directory and start over, use `rm -rf build` and then re-run setup.
- Use `-jN` to limit the number of threads to `N` during compilation


<br/>



### Post Installation 

You can add the lines below to your shell configuration file (e.g. `~/.bashrc` or `~/.zshrc`). 
Here we use `$GEMC_VERSION` to control the version of GEMC you want to use.

```shell
export GEMC_VERSION={{ page.latest_tag }}
export PATH={{ page.path_prefix }}/$GEMC_VERSION/bin:$PATH
export PYTHONPATH={{ page.path_prefix }}/$GEMC_VERSION/api:$PYTHONPATH
```






<br/><br/>

## Run GEMC in a Docker Container

You can use docker to run GEMC. The available images are listed below. 
Both `arm64` and `amd64` are supported (except on Arch Linux images which are `amd64` only [^1]).

<br/>

{:.zebra}

| OS   | Pull Command | arm64 | amd64                         |
|-----|-------------------------|-------------------------------------|
{% for img in site.data.docker.images -%}
| {{ img.id }} {{ img.osversion }}  | ```docker pull {{ img.tag }}``` | {{ img.arm64 }} | {{ img.amd64 }} |
{% endfor %}


It is recommended to bind a local directory to save and store your work.
For illustration purposes, below we will bind the image path `{{ page.docker_remote_mount }}`
to the local dir `{{ page.docker_local_mount }}` and we will use the image `{{ site.data.docker.images[0].tag }}`.

[^1]: For Apple Silicon Mac add the option `--platform linux/amd64` to the `docker run` command if you want to use the `archlinux amd64` images.

<br/>

### Run docker in batch mode

```

docker run -it --rm -v {{ page.docker_local_mount }}:{{ page.docker_remote_mount}} {{ site.data.docker.images[0].tag }} bash

```

<br/>

### Run docker and use a browser for the graphical interface:

```

docker run -it --rm  -v {{ page.docker_local_mount }}:{{ page.docker_remote_mount}}  -p 8080:8080 {{ site.data.docker.images[0].tag }}

```

Then point your browser to [`http://localhost:8080/vnc.html`]( http://localhost:8080/vnc.html ) to access the graphical interface.

<br/>




<br/><br/>

## Run GEMC using Apptainer


Linux hosts can use `apptainer` (formally `singularity`) to run docker containers. 
You can use it with the docker images above.  It runs similarly to docker:


```

apptainer exec --cleanenv --bind {{ page.docker_local_mount }}:{{ page.docker_remote_mount}} {{ site.data.docker.images[0].tag }} bash

```

<br/>

> Apptainer uses a default cache directory to store the images. If that becomes full, one can use
> environment variables to point to a location with enough disk space.
> For example, to point to `/path/to/$USER/cache`:

```shell
	export sif_cache=/path/to/$USER/cache
	export APPTAINER_CACHEDIR=$sif_cache/apptainer-cache
	export APPTAINER_TMPDIR=$sif_cache/apptainer-tmp
	export TMPDIR=$sif_cache/apptainer-tmp
```

> Then run apptainer again.





<br/><br/><br/>

# Appendix
<br/>

## GEMC and Geant4 Software Prerequisites

<br/>

- Builders and compilers:

  - C++ Compiler and Standard Library supporting the C++17 Standard
  - [CMake](https://cmake.org) 3.16 or later
  - [Meson](https://mesonbuild.com) 1.10.1 or later

<br/>

- Packages, compiled from source against the same C++ Standard as GEMC (C++17 by default):

  - [Geant4](https://geant4.web.cern.ch): 11.3.2 or higher
  - [CLHEP](https://proj-clhep.web.cern.ch/proj-clhep/): 2.4.6.0 or higher 
  - [Xerces-C](https://xerces.apache.org/xerces-c/): 3.2  or higher
  
<br/>

- Packages installed with your system package manager:

  - expat: 2.0.1 or higher
  - zlib: 1.2.3 or higher
  - [Qt6](https://www.qt.io): 6.5 or higher (optional, required for GUI
  - [ROOT](https://root.cern): 6.36.04 or higher (optional, required for ROOT output)

<br/>

One liners installation of basic packages and dependencies on some popular Linux distributions:

{% capture tab1a %}
```shell
dnf install -y --allowerasing git make cmake gcc-c++ gdb valgrind expat-devel mariadb-devel \
sqlite-devel python3-devel ninja-build mesa-libGLU-devel libX11-devel libXpm-devel libXft-devel \
libXt-devel libXmu-devel libXrender-devel xorg-x11-server-Xvfb xrandr bzip2 wget curl nano bash \
zsh hostname gedit environment-modules pv which psmisc procps mailcap net-tools rsync patch \
bash-completion xterm x11vnc openbox lxqt-panel dejavu-sans-mono-fonts qt6-qtbase-devel root liblsan \
libasan libubsan libtsan tbb 
```
{% endcapture %}

{% capture tab2a %}
```shell
dnf install -y --allowerasing git make cmake gcc-c++ gdb valgrind expat-devel mariadb-devel \
sqlite-devel python3-devel ninja-build mesa-libGLU-devel libX11-devel libXpm-devel libXft-devel \
libXt-devel libXmu-devel libXrender-devel xorg-x11-server-Xvfb xrandr bzip2 wget curl nano bash 
zsh hostname gedit environment-modules pv which psmisc procps mailcap net-tools rsync patch \
bash-completion xterm x11vnc openbox tint2 dejavu-sans-mono-fonts qt6-qtbase-devel root liblsan \
libasan libubsan libtsan tbb
```
{% endcapture %}

{% capture tab3a %}
```shell
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata git make cmake \
g++ gdb valgrind libexpat1-dev libmysqlclient-dev libsqlite3-dev python3-dev ninja-build \
libglu1-mesa-dev libx11-dev libxpm-dev libxft-dev libxt-dev libxmu-dev libxrender-dev \
xvfb x11-xserver-utils bzip2 wget curl nano bash zsh hostname gedit environment-modules pv \
which ca-certificates psmisc procps mailcap net-tools rsync patch bash-completion xterm \
x11vnc openbox tint2 dbus-x11 fonts-dejavu-core qt6-base-dev libqt6opengl6t64 \
libqt6openglwidgets6t64 qt6-base-dev-tools liblsan0 libasan8 libubsan1 libtsan2 libtbb12
```
{% endcapture %}

{% capture tab4a %}
```shell
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata git make cmake \
g++ gdb valgrind libexpat1-dev libmariadb-dev libsqlite3-dev python3-dev ninja-build \
libglu1-mesa-dev libx11-dev libxpm-dev libxft-dev libxt-dev libxmu-dev libxrender-dev \
xvfb x11-xserver-utils bzip2 wget curl nano bash zsh hostname gedit environment-modules pv \
which ca-certificates psmisc procps mailcap net-tools rsync patch bash-completion xterm \
x11vnc openbox tint2 dbus-x11 fonts-dejavu-core qt6-base-dev libqt6opengl6 libqt6openglwidgets6 \
qt6-base-dev-tools liblsan0 libasan8 libubsan1 libtsan2 libtbb12 
```
{% endcapture %}

{% capture tab5a %}
```shell
pacman-key --init && pacman-key --populate
pacman -Sy --noconfirm archlinux-keyring
pacman -Syu --noconfirm --needed git make cmake gcc gdb valgrind expat mariadb mariadb-libs \
sqlite python python-pip ninja mesa glu libx11 libxpm libxft libxt libxmu libxrender \
xorg-server-xvfb xorg-xrandr bzip2 wget curl nano bash zsh inetutils gedit pv which fakeroot \
psmisc procps mailcap net-tools rsync patch bash-completion ncurses xterm tigervnc openbox \
ttf-dejavu qt6-base root gcc-libs tbb 
```
{% endcapture %}

{% include tabs5.html 
   tab1_title="Fedora"     tab1_content=tab1a
   tab2_title="AlmaLinux"  tab2_content=tab2a
   tab3_title="Ubuntu"     tab3_content=tab3a
   tab4_title="Debian"     tab4_content=tab4a
   tab5_title="Arch Linux" tab5_content=tab5a
%}

<br/>

## Supported and tested platforms
<br/>

- macOS: 15 or later (Sequoia)
- Linux:

  - Fedora 40 or later
  - AlmaLinux 9 or later
  - Ubuntu 24.04 or later
  - Debian 12 or later
  - Arch Linux (rolling release)

	


<br/>
<br/>
<br/>


