---
layout: default
title: Installation
permalink: /installation/

development_tag: dev
latest_tag: 0.2
latest_pytag: v0.2.0
dev_tag: dev
development_release_date: <small><time> → released nightly, shows commits</time></small>
latest_release_date: <small><time>→ released on 05/21/2026</time></small>
latest_prelease_date: <small><time>→ released on 05/28/2026</time></small>
repo_link: https://github.com/gemc/src
prepo_link: https://github.com/gemc/src
release_notes: https://github.com/gemc/src/releases
prelease_notes: https://github.com/gemc/pygemc/releases
binary_tag: dev
binary_geant4_tag: 11.4.1
path_prefix: /path/to/gemc
docker_local_mount: ~/mywork
docker_remote_mount: /mywork
---

### License

See the [license conditions](/home/license/).

<br/>

### Release Notes

- `gemc` [`{{ page.latest_tag }}`]({{ page.release_notes }}/tag/{{ page.latest_tag }}) {{ page.latest_release_date }}{: .meta }
- `pygemc` [`{{ page.latest_pytag }}`]({{ page.prelease_notes }}/tag/{{ page.latest_pytag }}) {{ page.latest_prelease_date }}{: .meta }
- [`dev`]({{ page.release_notes }}/tag/{{ page.development_tag }}) {{ page.development_release_date }}{: .meta }

<br/>

## Table of Contents

- [Install the Python API](#install-the-python-api)
- [Download a precompiled binary distribution](#download-a-precompiled-binary-distribution)
- [Build from source](#build-from-source)
- [Run in a Docker container](#run-in-a-docker-container)
- [Run using Apptainer](#run-using-apptainer)

- *Appendix*:
  - [Software Prerequisites for binary installation](#software-prerequisites-for-binary-installation)
  - [Software Prerequisites and Geant4 Installation for the GEMC build](#software-prerequisites-and-geant4-installation-for-gemc-build)
  - [Supported and tested platforms](#supported-and-tested-platforms)

<br/><br/>

## Install the Python API

<br/>

`pygemc` is available from [PyPI](https://pypi.org/project/pygemc/).
Use a virtual environment for direct `pip` installs:

```shell
python3 -m venv ~/venv/pygemc
source ~/venv/pygemc/bin/activate
python -m pip install pygemc
```

The optional Jupyter modules used by PyVista VTK export can be installed with:

```shell
python -m pip install "pygemc[jupyter]"
```

The optional ROOT-file analysis dependencies can be installed with:

```shell
python -m pip install "pygemc[root]"
```

[PyPI](https://pypi.org/project/pygemc/) does not install the `gemc` executable but can be used to 
create and visualize geometry or analyze results. 

<br/>

## Download a precompiled binary distribution

Binary tarballs contain the `gemc` executable and the examples (but not `pygemc`). Linux builds are available
for `amd64` and `arm64`; the macOS build is native to Apple Silicon (`arm64`).

Make sure to check the [Software Prerequisites for binary installation](#software-prerequisites-for-binary-installation)
before unpacking the tarball.

Choose an installation directory first:

```shell
gemc_home=/path/to/gemc
mkdir -p "$gemc_home"
cd "$gemc_home"
```

Then, use the commands from the tab that matches your Linux distribution and CPU architecture. 
This will install GEMC and the Geant4 data files.

{% capture tab1 %}

```shell
archive=gemc-dev-geant4-{{ page.binary_geant4_tag }}-fedora-44-amd64.tar.gz
curl -L -o "$archive" "{{ page.release_notes }}/download/{{ page.binary_tag }}/$archive"
tar -xzf "$archive" -C "$gemc_home" --strip-components=1
./install_geant4_data.sh
```

{% endcapture %}

{% capture tab2 %}

```shell
archive=gemc-dev-geant4-{{ page.binary_geant4_tag }}-fedora-44-arm64.tar.gz
curl -L -o "$archive" "{{ page.release_notes }}/download/{{ page.binary_tag }}/$archive"
tar -xzf "$archive" -C "$gemc_home" --strip-components=1
./install_geant4_data.sh
```

{% endcapture %}

{% capture tab3 %}

```shell
archive=gemc-dev-geant4-{{ page.binary_geant4_tag }}-almalinux-10-amd64.tar.gz
curl -L -o "$archive" "{{ page.release_notes }}/download/{{ page.binary_tag }}/$archive"
tar -xzf "$archive" -C "$gemc_home" --strip-components=1
./install_geant4_data.sh
```

{% endcapture %}

{% capture tab4 %}

```shell
archive=gemc-dev-geant4-{{ page.binary_geant4_tag }}-almalinux-10-arm64.tar.gz
curl -L -o "$archive" "{{ page.release_notes }}/download/{{ page.binary_tag }}/$archive"
tar -xzf "$archive" -C "$gemc_home" --strip-components=1
./install_geant4_data.sh
```

{% endcapture %}

{% capture tab5 %}

```shell
archive=gemc-dev-geant4-{{ page.binary_geant4_tag }}-ubuntu-24.04-amd64.tar.gz
curl -L -o "$archive" "{{ page.release_notes }}/download/{{ page.binary_tag }}/$archive"
tar -xzf "$archive" -C "$gemc_home" --strip-components=1
./install_geant4_data.sh
```

{% endcapture %}

{% capture tab6 %}

```shell
archive=gemc-dev-geant4-{{ page.binary_geant4_tag }}-ubuntu-24.04-arm64.tar.gz
curl -L -o "$archive" "{{ page.release_notes }}/download/{{ page.binary_tag }}/$archive"
tar -xzf "$archive" -C "$gemc_home" --strip-components=1
./install_geant4_data.sh
```

{% endcapture %}

{% capture tab7 %}

```shell
archive=gemc-dev-geant4-{{ page.binary_geant4_tag }}-ubuntu-26.04-amd64.tar.gz
curl -L -o "$archive" "{{ page.release_notes }}/download/{{ page.binary_tag }}/$archive"
tar -xzf "$archive" -C "$gemc_home" --strip-components=1
./install_geant4_data.sh
```

{% endcapture %}

{% capture tab8 %}

```shell
archive=gemc-dev-geant4-{{ page.binary_geant4_tag }}-ubuntu-26.04-arm64.tar.gz
curl -L -o "$archive" "{{ page.release_notes }}/download/{{ page.binary_tag }}/$archive"
tar -xzf "$archive" -C "$gemc_home" --strip-components=1
./install_geant4_data.sh
```

{% endcapture %}

{% capture tab9 %}

```shell
archive=gemc-dev-geant4-{{ page.binary_geant4_tag }}-debian-13-amd64.tar.gz
curl -L -o "$archive" "{{ page.release_notes }}/download/{{ page.binary_tag }}/$archive"
tar -xzf "$archive" -C "$gemc_home" --strip-components=1
./install_geant4_data.sh
```

{% endcapture %}

{% capture tab10 %}

```shell
archive=gemc-dev-geant4-{{ page.binary_geant4_tag }}-debian-13-arm64.tar.gz
curl -L -o "$archive" "{{ page.release_notes }}/download/{{ page.binary_tag }}/$archive"
tar -xzf "$archive" -C "$gemc_home" --strip-components=1
./install_geant4_data.sh
```

{% endcapture %}

{% capture tab11 %}

```shell
archive=gemc-dev-geant4-{{ page.binary_geant4_tag }}-archlinux-latest-amd64.tar.gz
curl -L -o "$archive" "{{ page.release_notes }}/download/{{ page.binary_tag }}/$archive"
tar -xzf "$archive" -C "$gemc_home" --strip-components=1
./install_geant4_data.sh
```

{% endcapture %}

{% capture tab12 %}

The macOS asset is tagged with the build host's macOS and Clang versions, so its exact name floats over time.
Resolve it from the `{{ page.binary_tag }}` release, then download and unpack:

```shell
archive=$(curl -sL https://api.github.com/repos/gemc/src/releases/tags/{{ page.binary_tag }} \
  | grep -oE 'gemc-{{ page.binary_tag }}-geant4-{{ page.binary_geant4_tag }}-macosx[0-9]+-clang[0-9]+-arm64\.tar\.gz' \
  | head -1)
curl -L -o "$archive" "{{ page.release_notes }}/download/{{ page.binary_tag }}/$archive"
tar -xzf "$archive" -C "$gemc_home" --strip-components=1
xattr -dr com.apple.quarantine "$gemc_home"   # clear Gatekeeper quarantine on the downloaded binaries
./install_geant4_data.sh
```

{% endcapture %}

{% include tabs.html
id="install_binary_tarball"
count=12
tab1_title="Fedora 44 amd64"
tab1_content=tab1

tab2_title="Fedora 44 arm64"
tab2_content=tab2

tab3_title="AlmaLinux 10 amd64"
tab3_content=tab3

tab4_title="AlmaLinux 10 arm64"
tab4_content=tab4

tab5_title="Ubuntu 24.04 amd64"
tab5_content=tab5

tab6_title="Ubuntu 24.04 arm64"
tab6_content=tab6

tab7_title="Ubuntu 26.04 amd64"
tab7_content=tab7

tab8_title="Ubuntu 26.04 arm64"
tab8_content=tab8

tab9_title="Debian 13 amd64"
tab9_content=tab9

tab10_title="Debian 13 arm64"
tab10_content=tab10

tab11_title="Arch Linux amd64"
tab11_content=tab11

tab12_title="macOS arm64 (Apple Silicon)"
tab12_content=tab12
%}

<br/>
After installation, source the GEMC environment file. Add this line to `.bashrc` or `.zshrc` if you
want it available in every shell:

```shell
source /path/to/gemc/gemc.env
```

Run a few checks to verify the installation:

```shell
gemc -v
test_gdynamic_plugin_load
test_gdata_event_verbose
```


<br/>

## Build from source

You will need Geant4 to build GEMC.  Check the 
[Software Prerequisites and Geant4 Installation for the GEMC build](#software-prerequisites-and-geant4-installation-for-gemc-build)
in the appendix for the complete list of requirements. 

<br/>

### 1. Obtain the source

Set the versioned installation prefix once, so you can copy and paste the commands below. Change `gprefix`
to the GEMC version and location you want to install.

```shell
gprefix={{ page.path_prefix }}/{{ page.latest_tag }}
```

The source code will be cloned into `$gprefix/source`, and GEMC will be installed into `$gprefix`.
For the development release, set `gprefix={{ page.path_prefix }}/{{ page.dev_tag }}` and use the development tab.


Download the code:

{% capture tab1 %}
Download the latest release:

```shell
mkdir -p "$gprefix"
cd "$gprefix"
git clone -c advice.detachedHead=false --branch {{ page.latest_tag }} {{ page.repo_link }} source
```

{% endcapture %}

{% capture tab2 %}
Clone the repository to build the nightly development version:

```shell
mkdir -p "$gprefix"
cd "$gprefix"
git clone --depth=1 {{ page.repo_link }} source
```

{% endcapture %}

{% include tabs.html
id="clone-gemc-commands"

count=2
tab1_title="Release"
tab1_content=tab1
tab2_title="GitHub Repository" 
tab2_content=tab2

%}






<br/>

### 2. Compile and install GEMC

The [Meson](https://mesonbuild.com) build system is used to compile and install GEMC.

The **setup** phase will check for the required dependencies and fetch external libraries.
Here we use a `build` directory inside `source`:

```shell
cd "$gprefix/source"
meson setup build --native-file=core.ini --prefix="$gprefix"
```

The **compile** phase will build the code and external libraries. The **install** phase will
copy the binaries, libraries, and python modules to the installation directory.

```shell
meson compile -C build
meson install -C build
```

Optionally, after installation, run `meson test -C build -v` to test the configured GEMC build.

<br/>

### Build Options

- The setup option `-Droot=enabled` will add ROOT support (needs ROOT installed on your system).
- The setup option `-Di_test=true` will enable the GUI interfaces in the tests.
- Use `-v` at build time for verbose output.
- To wipe out the build directory and start over, use `rm -rf build` and then re-run setup.
- Use `-jN` to set the number of threads during compilation.

<br/>

### Post installation

Add these lines to your shell configuration file (e.g. `~/.bashrc` or `~/.zshrc`):

```shell
export gprefix={{ page.path_prefix }}/{{ page.latest_tag }}
export PATH=$gprefix/bin:$gprefix/python_env/bin:$PATH
```

The second PATH entry adds the bundled Python
virtual environment so that `python3` resolves to the venv interpreter — making `import pygemc`
available in your scripts without any activation step or separate `pip install`. It also exposes the
`gemc-analyzer` and `gemc-system-template` command-line tools.

Check the installed simulator and Python tools with:

```shell
gemc -v
gemc-system-template --help
gemc-analyzer --help
```


<br/><br/>

## Run in a Docker container

You can use Docker to run GEMC. The available images are listed below.
Both `arm64` and `amd64` are supported (except on Arch Linux images which are `amd64` only [^1]).

{:.zebra}

| OS | GEMC Version | Registry address | arm64 | amd64 |
|----|--------------|------------------|-------|-------|
{% for img in site.data.docker.images -%}
| {{ img.id }} {{ img.osversion }} | {{ img.gemcv }} | ```{{ img.tag }}``` | {{ img.arm64 }} | {{ img.amd64 }} |
{% endfor %}

The addresses above are the [Docker Hub](https://hub.docker.com/r/gemc/gemc) images, published under the
[Docker-Sponsored Open Source](https://www.docker.com/community/open-source/application/) program, which allows
unlimited anonymous pulls. They are mirrored from the canonical
[GitHub Container Registry](https://github.com/gemc/src/pkgs/container/src) build: the two registries carry
identical content and tags. To pull from GHCR instead, replace the `docker.io/gemc/gemc:` prefix with
`ghcr.io/gemc/src:` and keep the same tag, for example `ghcr.io/gemc/src:dev-ubuntu-24.04`.

It is recommended to bind a local directory to save and store your work.
For illustration, the commands below bind the container path `{{ page.docker_remote_mount }}` to
`{{ page.docker_local_mount }}` and use the image `{{ site.data.docker.images[0].tag }}`.

[^1]: For Apple Silicon Mac add the option `--platform linux/amd64` to the `docker run` command if you want to use the
`archlinux amd64` images.

<br/>

### Batch mode

```
docker run -it --rm -v {{ page.docker_local_mount }}:{{ page.docker_remote_mount}} {{ site.data.docker.images[0].tag }} bash
```

<br/>

### Browser graphical interface

Set these convenience variables for the interactive session. Choose your own password:

```shell
VPORTS=(-p 6080:6080 -p 5900:5900)
VNC_PASS=(-e X11VNC_PASSWORD=change-me)
VNC_BIND=(-e VNC_BIND=0.0.0.0)
GEO_FLAGS=(-e GEOMETRY=1920x1200)
```

```shell
docker run -it --rm -v {{ page.docker_local_mount }}:{{ page.docker_remote_mount}} $VPORTS $VNC_BIND $VNC_PASS $GEO_FLAGS {{ site.data.docker.images[0].tag }}
```

Then point your browser to [`http://localhost:6080/vnc.html`](http://localhost:6080/vnc.html) to access the
graphical interface.

<br/>



## Run using Apptainer

Linux hosts can use `apptainer` (formerly `singularity`) to run Docker containers.
You can use it with the Docker images above. It runs similarly to Docker, but the entrypoint needs to be
sourced explicitly.

```
apptainer exec --cleanenv --bind {{ page.docker_local_mount }}:{{ page.docker_remote_mount}} docker://{{ site.data.docker.images[0].tag }} bash
```

Then:

```
source /usr/local/bin/docker-entrypoint.sh
gemc -v
```

<br/>

> [!WARNING]
> The graphical interface, especially OpenGL windows, may not work properly in Apptainer when you
> connect through a remote host.


<br/>

<blockquote class="doc-important" markdown="1">
**Note**

Apptainer uses a default cache directory to store images. If it becomes full, set the cache and
temporary directories to a location with enough disk space.
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

## Software Prerequisites for binary installation

<br/>

Binary tarball installations need only the runtime packages required by the `gemc` executable and the tools used
to download and unpack the archive. ROOT is intentionally not included in this list.

<br/>

{% capture btab1 %}

```shell
dnf install -y --allowerasing ca-certificates curl gzip tar expat sqlite-libs zlib \
libX11 libXext libXmu libXt mesa-libEGL mesa-libGL qt6-qtbase qt6-qtsvg tbb
```

{% endcapture %}

{% capture btab2 %}

```shell
dnf install -y --allowerasing ca-certificates curl gzip tar expat sqlite-libs zlib \
libX11 libXext libXmu libXt mesa-libEGL mesa-libGL qt6-qtbase qt6-qtsvg tbb
```

{% endcapture %}

{% capture btab3 %}

```shell
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata \
ca-certificates curl gzip tar libexpat1 libsqlite3-0 zlib1g \
libegl1 libgl1 libx11-6 libxext6 libxmu6 libxt6 \
libqt6core6t64 libqt6gui6 libqt6widgets6 libqt6opengl6 libqt6openglwidgets6 libqt6svg6 libtbb12
```

{% endcapture %}

{% capture btab4 %}

```shell
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata \
ca-certificates curl gzip tar libexpat1 libsqlite3-0 zlib1g \
libegl1 libgl1 libx11-6 libxext6 libxmu6 libxt6 \
libqt6core6t64 libqt6gui6 libqt6widgets6 libqt6opengl6 libqt6openglwidgets6 libqt6svg6 libtbb12
```

{% endcapture %}

{% capture btab5 %}

```shell
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata \
ca-certificates curl gzip tar libexpat1 libsqlite3-0 zlib1g \
libegl1 libgl1 libx11-6 libxext6 libxmu6 libxt6 \
libqt6core6t64 libqt6gui6 libqt6widgets6 libqt6opengl6 libqt6openglwidgets6 libqt6svg6 libtbb12
```

{% endcapture %}

{% capture btab6 %}

```shell
pacman-key --init && pacman-key --populate
pacman -Sy --noconfirm archlinux-keyring
pacman -Syu --noconfirm --needed ca-certificates curl gzip tar expat sqlite zlib \
libx11 libxext libxmu libxt mesa qt6-base qt6-svg tbb
```

{% endcapture %}

{% capture btab7 %}

The binary links against Homebrew Qt, SQLite, expat, zlib, and TBB; XQuartz supplies the X11/OpenGL runtime
used by the visualization.

```shell
brew install qt sqlite expat zlib tbb
brew install --cask xquartz
```

{% endcapture %}

{% include tabs.html
id="binary_install_requirements"
count=7
tab1_title="Fedora 44"
tab1_content=btab1

tab2_title="AlmaLinux 10"
tab2_content=btab2

tab3_title="Ubuntu 24.04"
tab3_content=btab3

tab4_title="Ubuntu 26.04"
tab4_content=btab4

tab5_title="Debian 13"
tab5_content=btab5

tab6_title="Arch Linux"
tab6_content=btab6

tab7_title="macOS"
tab7_content=btab7
%}

<br/>

## Software Prerequisites and Geant4 Installation for the GEMC build

<br/>

- Builders and compilers:

    - C++ Compiler and Standard Library supporting the C++17 Standard
    - [CMake](https://cmake.org) 3.16 or later
    - [Meson](https://mesonbuild.com) 1.10.1 or later

<br/>

- System Packages (typically installed with your system package manager):

    - expat: 2.0.1 or higher
    - zlib: 1.2.3 or higher
    - [Qt6](https://www.qt.io): 6.5 or higher (required for GUI)
    - [ROOT](https://root.cern): 6.36.04 or higher (optional, required for ROOT output)

<br/>

One-line installation commands for basic packages and dependencies on MacOS and some popular Linux distributions:

<br/>

{% capture tab1 %}

```shell
dnf install -y --allowerasing git make cmake gcc-c++ gdb valgrind libxcrypt-devel \
expat-devel zlib zlib-devel mariadb-devel sqlite-devel python3-devel ninja-build \
mesa-libGL-devel mesa-libGLU-devel libX11-devel libXpm-devel libXft-devel \
libXt-devel libXmu-devel libXrender-devel xorg-x11-server-Xvfb xrandr \
bzip2 wget curl nano bash zsh hostname gedit environment-modules pv which \
psmisc procps mailcap net-tools rsync patch bash-completion python3-numpy \
xterm x11vnc openbox lxqt-panel dejavu-sans-mono-fonts \
qt6-qtbase-devel qt6-qtsvg qt6-qtsvg-devel root liblsan libasan libubsan libtsan tbb
```

{% endcapture %}

{% capture tab2 %}

```shell
dnf install -y --allowerasing git make cmake gcc-c++ gdb valgrind libxcrypt-devel \
expat-devel zlib zlib-devel mariadb-devel sqlite-devel python3-devel ninja-build \
mesa-libGL-devel mesa-libGLU-devel libX11-devel libXpm-devel libXft-devel \
libXt-devel libXmu-devel libXrender-devel \
bzip2 wget curl nano bash zsh hostname gedit environment-modules pv which \
psmisc procps mailcap net-tools rsync patch bash-completion python3-numpy \
xterm dejavu-sans-mono-fonts \
qt6-qtbase-devel qt6-qtsvg qt6-qtsvg-devel root liblsan libasan libubsan libtsan tbb
```

{% endcapture %}

{% capture tab3 %}

```shell
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata \
git make cmake g++ gdb valgrind libcrypt-dev libexpat1-dev zlib1g zlib1g-dev \
libmysqlclient-dev libsqlite3-dev python3-dev python3-venv ninja-build \
libgl1-mesa-dev libglu1-mesa-dev libx11-dev libxpm-dev libxft-dev \
libxt-dev libxmu-dev libxrender-dev xvfb x11-xserver-utils \
bzip2 wget curl nano bash zsh hostname gedit environment-modules pv which \
ca-certificates psmisc procps mailcap net-tools rsync patch bash-completion python3-numpy \
xterm x11vnc openbox tint2 dbus-x11 fonts-dejavu-core \
qt6-base-dev libqt6opengl6 libqt6openglwidgets6 qt6-base-dev-tools libqt6svg6 qt6-svg-dev \
liblz4-dev liblzma-dev libzstd-dev \
liblsan0 libasan8 libubsan1 libtsan2 libtbb12
```

{% endcapture %}

{% capture tab4 %}

```shell
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata \
git make cmake g++ gdb valgrind libcrypt-dev libexpat1-dev zlib1g zlib1g-dev \
libmysqlclient-dev libsqlite3-dev python3-dev python3-venv ninja-build \
libgl1-mesa-dev libglu1-mesa-dev libx11-dev libxpm-dev libxft-dev \
libxt-dev libxmu-dev libxrender-dev xvfb x11-xserver-utils \
bzip2 wget curl nano bash zsh hostname gedit environment-modules pv which \
ca-certificates psmisc procps mailcap net-tools rsync patch bash-completion python3-numpy \
xterm x11vnc openbox tint2 dbus-x11 fonts-dejavu-core \
qt6-base-dev libqt6opengl6 libqt6openglwidgets6 qt6-base-dev-tools libqt6svg6 qt6-svg-dev \
liblz4-dev liblzma-dev libzstd-dev \
liblsan0 libasan8 libubsan1 libtsan2 libtbb12
```

{% endcapture %}

{% capture tab5 %}

```shell
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata \
git make cmake g++ gdb valgrind libcrypt-dev libexpat1-dev zlib1g zlib1g-dev \
libmariadb-dev libsqlite3-dev python3-dev python3-venv ninja-build \
libgl1-mesa-dev libglu1-mesa-dev libx11-dev libxpm-dev libxft-dev \
libxt-dev libxmu-dev libxrender-dev xvfb x11-xserver-utils \
bzip2 wget curl nano bash zsh hostname gedit environment-modules pv which \
ca-certificates psmisc procps mailcap net-tools rsync patch bash-completion python3-numpy \
xterm x11vnc openbox tint2 dbus-x11 fonts-dejavu-core \
qt6-base-dev libqt6opengl6-dev libqt6openglwidgets6 qt6-base-dev-tools libqt6svg6 qt6-svg-dev \
liblz4-dev liblzma-dev libzstd-dev \
liblsan0 libasan8 libubsan1 libtsan2 libtbb12
```

{% endcapture %}

{% capture tab6 %}

```shell
pacman-key --init && pacman-key --populate
pacman -Sy --noconfirm archlinux-keyring
pacman -Syu --noconfirm --needed git make cmake gcc gdb valgrind expat zlib \
mariadb mariadb-libs sqlite python python-pip ninja mesa glu \
libx11 libxpm libxft libxt libxmu libxrender xorg-server-xvfb xorg-xrandr \
bzip2 wget curl nano bash zsh inetutils gedit pv which fakeroot \
psmisc procps mailcap net-tools rsync patch bash-completion ncurses python-numpy \
xterm tigervnc openbox ttf-dejavu qt6-base qt6-svg root gcc-libs tbb
```

{% endcapture %}

{% capture tab7 %}

```shell
brew install gnu-tar cmake mysql qt freeglut modules sqlite meson
```

{% endcapture %}

{% include tabs.html
id="install_requirements"
count=7
tab1_title="Fedora 44"
tab1_content=tab1

tab2_title="AlmaLinux 10"
tab2_content=tab2

tab3_title="Ubuntu 24.04"
tab3_content=tab3

tab4_title="Ubuntu 26.04"
tab4_content=tab4

tab5_title="Debian 13"
tab5_content=tab5

tab6_title="Arch Linux"
tab6_content=tab6

tab7_title="MacOS"
tab7_content=tab7
%}

<br/>

- External libraries, compiled from source against the same C++ Standard as GEMC (C++17 by default):

    - [CLHEP](https://proj-clhep.web.cern.ch/proj-clhep/): 2.4.6.0 or higher
    - [Xerces-C](https://xerces.apache.org/xerces-c/): 3.2 or higher
    - [Geant4](https://geant4.web.cern.ch): 11.3.2 or higher

<br/>

> [!IMPORTANT]
> GEMC can use any custom installation of `CLHEP`/`Xerces-C`/`Geant4`, however
> **we recommend using the [g4install](https://github.com/gemc/g4install) repository to install Geant4**,
> as it provides coexistence of multiple Geant4 versions and installation scripts.

<br/>

## Supported and tested platforms

- macOS: 26 (Apple Silicon, `arm64`)
  {% for img in site.data.docker.images -%}
  {% if img.gemcv == "dev" %}
- {{ img.id }}: {{ img.osversion }}
  {% endif %}>
  {% endfor %}

<br/>
<br/>
<br/>
