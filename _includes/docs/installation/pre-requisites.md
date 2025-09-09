## GEMC and Geant4 Software Prerequisites

<br/>

- Builders and compilers:

  - C++ Compiler and Standard Library supporting the C++17 Standard
  - [CMake](https://cmake.org) 3.16 or later
  - [Meson](https://mesonbuild.com) 1.9.0 or later

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
```bash
dnf install -y --allowerasing git make cmake gcc-c++ gdb valgrind expat-devel mariadb-devel \
sqlite-devel python3-devel ninja-build mesa-libGLU-devel libX11-devel libXpm-devel libXft-devel \
libXt-devel libXmu-devel libXrender-devel xorg-x11-server-Xvfb xrandr bzip2 wget curl nano bash \
zsh hostname gedit environment-modules pv which psmisc procps mailcap net-tools rsync patch \
bash-completion xterm x11vnc openbox lxqt-panel dejavu-sans-mono-fonts qt6-qtbase-devel root liblsan \
libasan libubsan libtsan tbb 
```
{% endcapture %}

{% capture tab2a %}
```bash
dnf install -y --allowerasing git make cmake gcc-c++ gdb valgrind expat-devel mariadb-devel \
sqlite-devel python3-devel ninja-build mesa-libGLU-devel libX11-devel libXpm-devel libXft-devel \
libXt-devel libXmu-devel libXrender-devel xorg-x11-server-Xvfb xrandr bzip2 wget curl nano bash 
zsh hostname gedit environment-modules pv which psmisc procps mailcap net-tools rsync patch \
bash-completion xterm x11vnc openbox tint2 dejavu-sans-mono-fonts qt6-qtbase-devel root liblsan \
libasan libubsan libtsan tbb
```
{% endcapture %}

{% capture tab3a %}
```bash
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
```bash
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
```bash
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
<br/>

## Supported and tested platforms
<br/>

- Linux:

  - Fedora 40 or later
  - AlmaLinux 9 or later
  - Ubuntu 24.04 or later
  - Debian 12 or later
  - Arch Linux (rolling release)

<br/>

- macOS: 15 or later (Sequoia)


