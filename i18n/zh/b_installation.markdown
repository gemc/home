---
layout: default
title: "安装"
permalink: /installation/

development_tag: dev
latest_tag: 0.5
latest_pytag: v0.5.0
latest_ctag: 0.3
dev_tag: dev
development_release_date: <small><time> → released nightly, shows commits</time></small>
latest_release_date: <small><time>→ released on 10/08/2026</time></small>
latest_prelease_date: <small><time>→ released on 10/08/2026</time></small>
latest_crelease_date: <small><time>→ released on 10/08/2026</time></small>
repo_link: https://github.com/gemc/src
prepo_link: https://github.com/gemc/src
release_notes: https://github.com/gemc/src/releases
prelease_notes: https://github.com/gemc/pygemc/releases
crelease_notes: https://github.com/gemc/clas12-systems/releases
binary_tag: dev
binary_geant4_tag: 11.4.3
path_prefix: /path/to/gemc
docker_local_mount: ~/mywork
docker_remote_mount: /mywork
lang: zh
human_reviewed: false
---

### 许可证

参见[许可条款](/home/license/)。

<br/>

### 发布说明

- `gemc` [{{ page.latest_tag }}][gemc-release] {{ page.latest_release_date }}{: .meta }
- `pygemc` [{{ page.latest_pytag }}][pygemc-release] {{ page.latest_prelease_date }}{: .meta }
- `clas12-systems` [{{ page.latest_ctag }}][clas12-release] {{ page.latest_crelease_date }}{: .meta }
- [`dev`]({{ page.release_notes }}/tag/{{ page.development_tag }}) {{ page.development_release_date }}{: .meta }

[gemc-release]: {{ page.release_notes }}/tag/{{ page.latest_tag }}
[pygemc-release]: {{ page.prelease_notes }}/tag/{{ page.latest_pytag }}
[clas12-release]: {{ page.crelease_notes }}/tag/{{ page.latest_ctag }}

<br/>

[流式读出](/home/documentation/sro/plugins/)需要 GEMC 0.5 的 SRO 接口，以及针对同一 GEMC 安装重新构建的
实验插件。FT-Cal 的 JLAB 编码器
属于 `clas12-systems`；仅安装 `pygemc` 并不提供原生 SRO 实现。

[顶点与角度示例](/home/examples/basic/generator_manipulations)
包含 11 份控制卡和预先准备好的 Analyzer 图表。请使用 GEMC 0.5 或更高版本；GUI 图表需要
Qt Charts。其批处理仿真和 CSV 检查在没有 Qt Charts 的情况下也能运行。

将在下一版本中推出：Qt Linguist 工具会在构建期间编译 GUI 语言翻译文件；Qt
翻译数据用于本地化标准对话框。下面的软件包安装命令已包含这两项。Homebrew Qt 提供
这些工具和翻译文件。GUI 语言会自动检测，也可通过可选的 `-language=<code>` 参数指定。

## 目录

- [安装 Python API](#install-the-python-api)
- [下载预编译的二进制发行版](#download-a-precompiled-binary-distribution)
- [从源码构建](#build-from-source)
- [在 Docker 容器中运行](#run-in-a-docker-container)
- [使用 Apptainer 运行](#run-using-apptainer)

- *附录*：
  - [二进制安装的软件前置条件](#software-prerequisites-for-binary-installation)
  - [GEMC 构建的软件前置条件与 Geant4
    安装](#software-prerequisites-and-geant4-installation-for-the-gemc-build)
  - [受支持并经过测试的平台](#supported-and-tested-platforms)

<br/><br/>

## 安装 Python API

<br/>

`pygemc` 可从 [PyPI](https://pypi.org/project/pygemc/) 获取。
直接使用 `pip` 安装时，请使用虚拟环境：

```shell
python3 -m venv ~/venv/pygemc
source ~/venv/pygemc/bin/activate
python -m pip install pygemc
```

PyVista VTK 导出所用的可选 Jupyter 模块可通过以下命令安装：

```shell
python -m pip install "pygemc[jupyter]"
```

可选的 ROOT 文件分析依赖可通过以下命令安装：

```shell
python -m pip install "pygemc[root]"
```

从 [PyPI](https://pypi.org/project/pygemc/) 安装的软件不包含 `gemc` 可执行文件，但可用于
创建和可视化几何体或分析结果。

<br/>

## 下载预编译的二进制发行版

二进制压缩包包含 `gemc` 可执行文件和示例（但不包含 `pygemc`）。Linux 构建提供
`amd64` 和 `arm64` 版本；macOS 构建为 Apple Silicon（`arm64`）原生版本。

在解包压缩包之前，请务必查看[二进制安装的软件前置条件](#software-prerequisites-for-binary-installation)。

首先选择一个安装目录：

```shell
gemc_home=/path/to/gemc
mkdir -p "$gemc_home"
cd "$gemc_home"
```

然后，使用与你的 Linux 发行版和 CPU 架构相匹配的选项卡中的命令。
这会安装 GEMC 以及 Geant4 data 文件。

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

macOS 发布文件的名称中包含构建主机的 macOS 和 Clang 版本，因此其确切名称会随时间变化。
请先从 `{{ page.binary_tag }}` 发行版中解析出名称，然后下载并解包：

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
安装完成后，加载 GEMC 环境文件。如果你希望在每个 shell 中都可用，请将下面这行添加到
`.bashrc` 或 `.zshrc`：

```shell
source /path/to/gemc/gemc.env
```

运行几项检查以验证安装：

```shell
gemc -v
test_gdynamic_plugin_load
test_gdata_event_verbose
```


<br/>

## 从源码构建

构建 GEMC 需要 Geant4。请查看附录中的
[GEMC 构建的软件前置条件与 Geant4
安装](#software-prerequisites-and-geant4-installation-for-the-gemc-build)
以获取完整的要求清单。

<br/>

### 1. 获取源码

下载代码：

{% capture tab1 %}
下载最新发行版：

```shell
git clone -c advice.detachedHead=false --branch {{ page.latest_tag }} {{ page.repo_link }}
cd src
```

{% endcapture %}

{% capture tab2 %}
克隆仓库以构建每夜更新的开发版本：

```shell
git clone --depth=1 {{ page.repo_link }}
cd src
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

### 2. 配置构建并安装 GEMC

GEMC 使用 [Meson](https://mesonbuild.com) 构建系统进行编译和安装。

**setup** 阶段会检查所需的依赖项并获取外部库。
此处我们使用一个 `build` 目录。

```shell
meson setup build --prefix=/path/to/install/gemc
```

**install** 阶段会构建并安装 GEMC。此处我们使用 `-q` 进行静默构建。

```shell
meson install -C build -q
```

安装完成后，也可运行 `meson test -C build` 来测试已配置的 GEMC 构建。

<br/>

### 构建选项

- setup 选项 `-Droot=enabled` 会添加 ROOT 支持（需要系统上已安装 ROOT）。
- setup 选项 `-Di_test=true` 会在测试中启用 GUI 界面。
- 在构建/测试时使用 `-v` 可获得详细输出。
- 如需清除构建目录并重新开始，请使用 `rm -rf build`，然后重新运行 setup。
- 使用 `-jN` 设置编译期间的线程数。

<br/>

### 安装后设置

将下面这些行添加到你的 shell 配置文件（例如 `~/.bashrc` 或 `~/.zshrc`）：

```shell
export PATH=/path/to/install/gemc/bin:/path/to/install/gemc/python_env/bin:$PATH
```

第二个 PATH 条目添加了随附的 Python 虚拟环境，使 `python3`
指向该虚拟环境的解释器，从而让你的脚本中可以使用
`import pygemc`。

通过以下命令检查已安装的仿真器和 Python 工具：

```shell
gemc -v
gemc-system-template --help
gemc-analyzer --help
```


<br/>

### 从源码构建 CLAS12 探测器系统

CLAS12 探测器系统
（[`clas12-systems`](https://github.com/gemc/clas12-systems)）0.3 采用相同的 Meson 流程构建，并且不再
需要预先安装 GEMC。在仅配置了 Geant4 的环境中，例如
[`g4install`](https://github.com/gemc/g4install) Docker 镜像，构建过程会从
`gemc` 子项目自动编译 GEMC，并将其安装到同一安装前缀下，因此探测器几何体和插件可以
完全从零开始安装。只有 Geant4 必须预先安装（构建过程不会编译它）；查找 GEMC 时，依次优先采用
显式指定的 `-Duse-gemc-location=<dir>`、通过 `PATH`/pkg-config 找到的已安装 GEMC，最后才是
从源码构建的子项目。

```shell
git clone --depth=1 --branch {{ page.latest_ctag }} https://github.com/gemc/clas12-systems
cd clas12-systems
meson setup build --prefix="$PWD/install"   # builds GEMC too if none is installed
meson compile -C build
meson install -C build
```


<br/><br/>

## 在 Docker 容器中运行

你可以使用 Docker 来运行 GEMC。可用镜像列在下方。
`arm64` 和 `amd64` 均受支持（Arch Linux 镜像除外，它们仅支持 `amd64` [^1]）。

{:.zebra}

| 操作系统 | GEMC 版本 | 镜像仓库地址 | arm64 | amd64 |
|----|--------------|------------------|-------|-------|
{% for img in site.data.docker.images -%}
| {{ img.id }} {{ img.osversion }} | {{ img.gemcv }} | ```{{ img.tag }}``` | {{ img.arm64 }} | {{ img.amd64 }} |
{% endfor %}

上面的地址指向 [Docker Hub](https://hub.docker.com/r/gemc/gemc) 镜像，这些镜像通过
[Docker 开源赞助](https://www.docker.com/community/open-source/application/)计划发布，该计划允许
无限制的匿名拉取。这些镜像同步自主发布源
[GitHub Container Registry](https://github.com/gemc/src/pkgs/container/src) 的构建：两个镜像仓库的
内容和标签完全相同。若要改为从 GHCR 拉取，请将 `docker.io/gemc/gemc:` 前缀替换为
`ghcr.io/gemc/src:`，并保留相同的标签，例如 `ghcr.io/gemc/src:dev-ubuntu-24.04`。

建议绑定一个本地目录来保存和存储你的工作。
为便于说明，下面的命令将容器路径 `{{ page.docker_remote_mount }}` 绑定到
`{{ page.docker_local_mount }}`，并使用镜像 `{{ site.data.docker.images[0].tag }}`。

[^1]: 对于 Apple Silicon Mac，如果你想使用
`archlinux amd64` 镜像，请在 `docker run` 命令中添加选项 `--platform linux/amd64`。

<br/>

### 批处理模式

```
docker run -it --rm -v {{ page.docker_local_mount }}:{{ page.docker_remote_mount}} {{ site.data.docker.images[0].tag }} bash
```

<br/>

### 浏览器图形界面

为交互式会话设置这些便捷变量。请自行选择一个密码：

```shell
VPORTS=(-p 6080:6080 -p 5900:5900)
VNC_PASS=(-e X11VNC_PASSWORD=change-me)
VNC_BIND=(-e VNC_BIND=0.0.0.0)
GEO_FLAGS=(-e GEOMETRY=1920x1200)
```

```shell
docker run -it --rm -v {{ page.docker_local_mount }}:{{ page.docker_remote_mount}} $VPORTS $VNC_BIND $VNC_PASS $GEO_FLAGS {{ site.data.docker.images[0].tag }}
```

然后在浏览器中打开 [`http://localhost:6080/vnc.html`](http://localhost:6080/vnc.html)，以访问
图形界面。

<br/>



## 使用 Apptainer 运行

Linux 主机可以使用 `apptainer`（原名 `singularity`）来运行 Docker 容器。
它可以配合上面的 Docker 镜像使用。运行方式与 Docker 类似，但需要
显式加载入口点脚本。

```
apptainer exec --cleanenv --bind {{ page.docker_local_mount }}:{{ page.docker_remote_mount}} docker://{{ site.data.docker.images[0].tag }} bash
```

然后：

```
source /usr/local/bin/docker-entrypoint.sh
gemc -v
```

<br/>

> [!WARNING]
> 当你通过远程主机连接时，图形界面（尤其是 OpenGL 窗口）在 Apptainer 中
> 可能无法正常工作。


<br/>

<blockquote class="doc-important" markdown="1">
**注意**

Apptainer 使用默认缓存目录来存储镜像。如果该目录已满，请将缓存目录和
临时目录设置到有足够磁盘空间的位置。
例如，将 `sim_cache` 设置到有足够空间的位置：

```shell
	export sif_cache=/path/to/$USER/cache
```

然后设置这些变量：

```shell
	export APPTAINER_CACHEDIR=$sif_cache/apptainer-cache
	export APPTAINER_TMPDIR=$sif_cache/apptainer-tmp
	export TMPDIR=$sif_cache/apptainer-tmp
```

然后再次运行 apptainer。
</blockquote>


<br/><br/><br/>

# 附录

<br/>

## 二进制安装的软件前置条件

<br/>

二进制压缩包安装只需要 `gemc` 可执行文件所需的运行时软件包，以及用于
下载和解包压缩包的工具。此清单有意不包含 ROOT。

<br/>

{% capture btab1 %}

```shell
dnf install -y --allowerasing ca-certificates curl gzip tar expat sqlite-libs zlib \
libX11 libXext libXmu libXt mesa-libEGL mesa-libGL qt6-qtbase qt6-qtsvg qt6-qtcharts qt6-qttranslations tbb
```

{% endcapture %}

{% capture btab2 %}

```shell
dnf install -y --allowerasing ca-certificates curl gzip tar expat sqlite-libs zlib \
libX11 libXext libXmu libXt mesa-libEGL mesa-libGL qt6-qtbase qt6-qtsvg qt6-qtcharts qt6-qttranslations tbb
```

{% endcapture %}

{% capture btab3 %}

```shell
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata \
ca-certificates curl gzip tar libexpat1 libsqlite3-0 zlib1g \
libegl1 libgl1 libx11-6 libxext6 libxmu6 libxt6 \
libqt6core6t64 libqt6gui6 libqt6widgets6 libqt6opengl6 libqt6openglwidgets6 \
libqt6svg6 libqt6charts6 qt6-translations-l10n libtbb12
```

{% endcapture %}

{% capture btab4 %}

```shell
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata \
ca-certificates curl gzip tar libexpat1 libsqlite3-0 zlib1g \
libegl1 libgl1 libx11-6 libxext6 libxmu6 libxt6 \
libqt6core6t64 libqt6gui6 libqt6widgets6 libqt6opengl6 libqt6openglwidgets6 \
libqt6svg6 libqt6charts6 qt6-translations-l10n libtbb12
```

{% endcapture %}

{% capture btab5 %}

```shell
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata \
ca-certificates curl gzip tar libexpat1 libsqlite3-0 zlib1g \
libegl1 libgl1 libx11-6 libxext6 libxmu6 libxt6 \
libqt6core6t64 libqt6gui6 libqt6widgets6 libqt6opengl6 libqt6openglwidgets6 \
libqt6svg6 libqt6charts6 qt6-translations-l10n libtbb12
```

{% endcapture %}

{% capture btab6 %}

```shell
pacman-key --init && pacman-key --populate
pacman -Sy --noconfirm archlinux-keyring
pacman -Syu --noconfirm --needed ca-certificates curl gzip tar expat sqlite zlib \
libx11 libxext libxmu libxt mesa qt6-base qt6-svg qt6-charts qt6-translations tbb
```

{% endcapture %}

{% capture btab7 %}

该二进制文件链接到 Homebrew 的 Qt、SQLite、expat、zlib 和 TBB；XQuartz 提供可视化所使用的 X11/OpenGL
运行时。

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

## GEMC 构建的软件前置条件与 Geant4 安装

<br/>

- 构建工具与编译器：

    - 支持 C++20 的 C++ 编译器和标准库（用于 GEMC 0.5 或更高版本）：GCC 11+、Clang 13+ 或
      Apple Clang 14+；每个受支持的平台都已自带满足要求的编译器
    - [CMake](https://cmake.org) 3.16 或更高版本
    - [Meson](https://mesonbuild.com) 1.10.1 或更高版本

<br/>

- 系统软件包（通常通过你的系统包管理器安装）：

    - expat：2.0.1 或更高版本
    - zlib：1.2.3 或更高版本
    - [Qt6](https://www.qt.io)：6.4.2 或更高版本（GUI 所需）；SVG 提供工具栏图标，Charts
      启用 GUI Analyzer，但这两个模块都是可选的
    - [ROOT](https://root.cern)：6.36.04 或更高版本（可选，ROOT 输出所需）

<br/>

在 macOS 和一些常用 Linux 发行版上安装基础软件包和依赖项的单行命令：

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
qt6-qtbase-devel qt6-qtsvg qt6-qtsvg-devel qt6-qtcharts-devel \
qt6-qttools-devel qt6-qttranslations \
root liblsan libasan libubsan libtsan tbb
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
qt6-qtbase-devel qt6-qtsvg qt6-qtsvg-devel qt6-qtcharts-devel \
qt6-qttools-devel qt6-qttranslations \
root liblsan libasan libubsan libtsan tbb
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
qt6-charts-dev qt6-l10n-tools qt6-translations-l10n \
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
qt6-charts-dev qt6-l10n-tools qt6-translations-l10n \
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
qt6-charts-dev qt6-l10n-tools qt6-translations-l10n \
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
xterm tigervnc openbox ttf-dejavu qt6-base qt6-svg qt6-charts qt6-tools qt6-translations root gcc-libs tbb
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

- 外部库，须使用与 GEMC 相同的 C++ 标准（GEMC 0.5 或更高版本使用 C++20）从源码编译：

    - [CLHEP](https://proj-clhep.web.cern.ch/proj-clhep/)：2.4.6.0 或更高版本
    - [Xerces-C](https://xerces.apache.org/xerces-c/)：3.2 或更高版本
    - [Geant4](https://geant4.web.cern.ch)：11.3.2 或更高版本

<br/>

> [!IMPORTANT]
> GEMC 可以使用任何自定义安装的 `CLHEP`/`Xerces-C`/`Geant4`，不过
> **我们推荐使用 [g4install](https://github.com/gemc/g4install) 仓库来安装 Geant4**，
> 因为它支持多个 Geant4 版本共存，并提供安装脚本。

<br/>

## 受支持并经过测试的平台

- macOS：26（Apple Silicon，`arm64`）
  {% for img in site.data.docker.images -%}
  {% if img.gemcv == "dev" %}
- {{ img.id }}：{{ img.osversion }}
  {% endif %}>
  {% endfor %}

<br/>
<br/>
<br/>
