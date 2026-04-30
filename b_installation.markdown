---
layout: default
title: Installation
permalink: /installation/

development_tag: dev
latest_tag: 0.1
dev_tag: dev
development_release_date: <small><time>released nightly</time></small>
latest_release_date: <small><time>04/29/2026</time></small>
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
- [`{{ page.latest_tag }}`]({{ page.release_notes }}/tag/{{ page.latest_tag }}) - <small><time>Released on</time></small> {{ page.latest_release_date }}{: .meta }
- [`All Releases`]({{ page.release_notes }})

<br/>

> [!NOTE] 
> Use the most recent GEMC release to ensure you are taking  advantage of
> latest bug fixes and the new features. This also helps the developers to provide the best support.

<br/><br/>


## Table of Contents
 
- [Build and Install GEMC from source code](#build-and-install-gemc-from-source)
- [[Optional] Install Pyvista](#optional-install-pyvista)
- [GEMC using Docker](#gemc-using-docker)
- [GEMC using Apptainer](#gemc-using-apptainer)



<br/><br/>


## Build and Install GEMC from Source

Please see the [Software Prerequisites and Geant4 Installation](#software-prerequisites-and-geant4-installation) 
in the appendix for the requirements.

<br/>

### 1. Obtain the source 

For illustration, we will use  `{{ page.path_prefix }}` as the installation location, `{{ page.latest_tag }}` 
as the version to be installed, `source` as where to place the source code. 
Replace `{{ page.latest_tag }}` with `{{ page.dev_tag }}` if you want to instal the development release.  

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


The **setup** phase will check for the required dependencies and fetch external libraries.
Here we use a `build` directory inside `ssource`:


```shell
cd {{ page.path_prefix }}/{{ page.latest_tag }}/source
meson setup build --native-file=core.ini --prefix={{ page.path_prefix }}/{{ page.latest_tag }}
```

The **compile** phase will build the code and external libraries. The **install** phase will 
copy the binaries, libraries, and python modules to the installation directory.

```shell
meson compile -C build
meson install -C build
```

Optionally, after installation, `meson test -v` will run several tests of various components of GEMC. 

<br/>

### Build Options

- The setup option `-Droot=enabled` will add ROOT support (needs ROOT installed on your system).
- The setup option `-Di_test=true` will enable the GUI interfaces in the tests.
- Use `-v` at build time for verbose output.
- To wipe out the build directory and start over, use `rm -rf build` and then re-run setup.
- Use `-jN` to set the number of threads during compilation


<br/>



### Post Installation 

You can add the lines below to your shell configuration file (e.g. `~/.bashrc` or `~/.zshrc`). 

```shell
export GEMC_VERSION={{ page.latest_tag }}
export PATH={{ page.path_prefix }}/$GEMC_VERSION/bin:$PATH
export PYTHONPATH={{ page.path_prefix }}/$GEMC_VERSION/api:$PYTHONPATH
```

Here with `GEMC_VERSION` we control the version of GEMC to use. 


<br/>


## [Optional] Install Pyvista


While pyvista is not necessary to build the detectors, it provides  a nice visual feedback
without the need to run GEMC to visualize the geometry.

To install pyvista, including the qt modules, use a python environment:

```shell
python3 -m venv ~/venv/pyvista/
source ~/venv/pyvista/bin/activate
pip install pyvista vtk 
pip install pyqt6 pyvistaqt
```

To use it with the Python API, remember to activate the environment first: 

```shell
source ~/venv/pyvista/bin/activate
```

Then pass either `-pv` (native pyvista) or `-pvb` (for a qt GUI) to the python scripts that build 
the databases. 



<br/><br/>

## GEMC using Docker

You can use docker to run GEMC. The available images are listed below. 
Both `arm64` and `amd64` are supported (except on Arch Linux images which are `amd64` only [^1]).


{:.zebra}

| OS   | Registry address | arm64 | amd64                         |
|-----|-------------------------|-------------------------------------|
{% for img in site.data.docker.images -%}
| {{ img.id }} {{ img.osversion }}  | ```{{ img.tag }}``` | {{ img.arm64 }} | {{ img.amd64 }} |
{% endfor %}


It is recommended to bind a local directory to save and store your work.
For illustration purposes, below we will bind the image path `{{ page.docker_remote_mount }}`
to the local dir `{{ page.docker_local_mount }}` and we will use the image `{{ site.data.docker.images[0].tag }}`.

[^1]: For Apple Silicon Mac add the option `--platform linux/amd64` to the `docker run` command if you want to use the `archlinux amd64` images.

<br/>

### Batch mode

```
docker run -it --rm -v {{ page.docker_local_mount }}:{{ page.docker_remote_mount}} {{ site.data.docker.images[0].tag }} bash
```

<br/>

### Use a browser for the graphical interface:

Set these convenience variables for the interactive (choose your own password):

```shell
VPORTS=(-p 6080:6080 -p 5900:5900)
VNC_PASS=(-e X11VNC_PASSWORD=change-me)
VNC_BIND=(-e VNC_BIND=0.0.0.0)
GEO_FLAGS=(-e GEOMETRY=1920x1200)
```

```shell
docker run -it --rm -v {{ page.docker_local_mount }}:{{ page.docker_remote_mount}} $VPORTS $VNC_BIND $VNC_PASS $GEO_FLAGS {{ site.data.docker.images[0].tag }}
```

Then point your browser to [` http://localhost:6080/vnc.html`](  http://localhost:6080/vnc.html ) to access the graphical interface.

<br/>




<br/><br/>

## GEMC using Apptainer


Linux hosts can use `apptainer` (formally `singularity`) to run docker containers. 
You can use it with the docker images above.  It runs similarly to docker:


```
apptainer exec --cleanenv --bind {{ page.docker_local_mount }}:{{ page.docker_remote_mount}} docker://{{ site.data.docker.images[0].tag }} bash
```

<br/>

<blockquote class="doc-important" markdown="1">
**Note**

Apptainer uses a default cache directory to store the images. If that becomes full, one can use
environment variables to point to a location with enough disk space.
For example, set `sim_cache` to somewhere with enough space:

```shell
	export sif_cache=/path/to/$USER/cache
```

then set these variables:

```shell
	export APPTAINER_CACHEDIR=$sif_cache/apptainer-cache
	export APPTAINER_TMPDIR=$sif_cache/apptainer-tmp
	export TMPDIR=$sif_cache/apptainer-tmp
```

and run apptainer again.
</blockquote>


<br/><br/><br/>

# Appendix
<br/>

## Software Prerequisites and Geant4 Installation

<br/>

- Builders and compilers:

  - C++ Compiler and Standard Library supporting the C++17 Standard
  - [CMake](https://cmake.org) 3.16 or later
  - [Meson](https://mesonbuild.com) 1.10.1 or later

- Packages installed with your system package manager:

  - expat: 2.0.1 or higher
  - zlib: 1.2.3 or higher
  - [Qt6](https://www.qt.io): 6.5 or higher (required for GUI
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

- Packages, compiled from source against the same C++ Standard as GEMC (C++17 by default):

  - [Geant4](https://geant4.web.cern.ch): 11.3.2 or higher
  - [CLHEP](https://proj-clhep.web.cern.ch/proj-clhep/): 2.4.6.0 or higher 
  - [Xerces-C](https://xerces.apache.org/xerces-c/): 3.2  or higher

<br/>

> [!IMPORTANT]
> GEMC can use any custom installation of Geant4, however 
> **we recommend using the [g4install](https://github.com/gemc/g4install) repository to install Geant4**, 
> as it provides seamless coexistence of multiple Geant4 versions.

<br/>

## Supported and tested platforms
<br/>

- macOS: 26
{% for img in site.data.docker.images -%}
- {{ img.id }}: {{ img.osversion }} 
{% endfor %}	


<br/>
<br/>
<br/>


