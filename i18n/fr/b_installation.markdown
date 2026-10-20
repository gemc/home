---
layout: default
title: "Installation"
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
lang: fr
human_reviewed: false
---

### Licence

Consultez les [conditions de licence](/home/license/).

<br/>

### Notes de version

- `gemc` [{{ page.latest_tag }}][gemc-release] {{ page.latest_release_date }}{: .meta }
- `pygemc` [{{ page.latest_pytag }}][pygemc-release] {{ page.latest_prelease_date }}{: .meta }
- `clas12-systems` [{{ page.latest_ctag }}][clas12-release] {{ page.latest_crelease_date }}{: .meta }
- [`dev`]({{ page.release_notes }}/tag/{{ page.development_tag }}) {{ page.development_release_date }}{: .meta }

[gemc-release]: {{ page.release_notes }}/tag/{{ page.latest_tag }}
[pygemc-release]: {{ page.prelease_notes }}/tag/{{ page.latest_pytag }}
[clas12-release]: {{ page.crelease_notes }}/tag/{{ page.latest_ctag }}

<br/>

La [lecture en continu (streaming readout)](/home/documentation/sro/plugins/) nécessite les interfaces SRO de
GEMC 0.5 ainsi que les plugins propres à l'expérience recompilés avec la même installation de GEMC. L'encodeur
JLAB de FT-Cal fait partie de `clas12-systems` ; installer `pygemc` seul ne fournit pas l'implémentation SRO native.

Les [exemples de vertex et d'angles](/home/examples/basic/generator_manipulations)
comprennent 11 cartes de pilotage et des graphiques Analyzer préparés. Utilisez GEMC 0.5 ou une version ultérieure ;
les graphiques de l'interface graphique nécessitent Qt Charts. Les simulations par lots et les vérifications CSV
de ces exemples fonctionnent également sans Qt Charts.

À venir dans la prochaine version : les outils Qt Linguist compilent les catalogues de traduction de l'interface
graphique pendant la compilation ; les données de traduction Qt traduisent les boîtes de dialogue standard.
Les commandes d'installation de paquets ci-dessous incluent ces deux éléments. Qt fourni par Homebrew comprend
ces outils et ces catalogues. La langue de l'interface graphique est détectée automatiquement ; l'option
facultative `-language=<code>` permet de la choisir explicitement.

## Table des matières

- [Installer l'API Python](#install-the-python-api)
- [Télécharger une distribution binaire précompilée](#download-a-precompiled-binary-distribution)
- [Compiler à partir des sources](#build-from-source)
- [Exécuter dans un conteneur Docker](#run-in-a-docker-container)
- [Exécuter avec Apptainer](#run-using-apptainer)

- *Annexe* :
  - [Prérequis logiciels pour l'installation binaire](#software-prerequisites-for-binary-installation)
  - [Prérequis logiciels et installation de Geant4 pour la compilation de
    GEMC](#software-prerequisites-and-geant4-installation-for-the-gemc-build)
  - [Plateformes prises en charge et testées](#supported-and-tested-platforms)

<br/><br/>

## Installer l'API Python

<br/>

`pygemc` est disponible sur [PyPI](https://pypi.org/project/pygemc/).
Utilisez un environnement virtuel pour les installations directes avec `pip` :

```shell
python3 -m venv ~/venv/pygemc
source ~/venv/pygemc/bin/activate
python -m pip install pygemc
```

Les modules Jupyter facultatifs utilisés pour l'export VTK de PyVista peuvent être installés avec :

```shell
python -m pip install "pygemc[jupyter]"
```

Les dépendances facultatives pour l'analyse de fichiers ROOT peuvent être installées avec :

```shell
python -m pip install "pygemc[root]"
```

L'installation depuis [PyPI](https://pypi.org/project/pygemc/) ne fournit pas l'exécutable `gemc`, mais permet de
créer et de visualiser des géométries ou d'analyser des résultats.

<br/>

## Télécharger une distribution binaire précompilée

Les archives binaires tar contiennent l'exécutable `gemc` et les exemples (mais pas `pygemc`). Les versions Linux
sont disponibles pour `amd64` et `arm64` ; la version macOS est native pour Apple Silicon (`arm64`).

Veillez à consulter les [prérequis logiciels pour l'installation binaire](#software-prerequisites-for-binary-installation)
avant de décompresser l'archive.

Choisissez d'abord un répertoire d'installation :

```shell
gemc_home=/path/to/gemc
mkdir -p "$gemc_home"
cd "$gemc_home"
```

Ensuite, utilisez les commandes de l'onglet correspondant à votre distribution Linux et à l'architecture de
votre processeur. Cela installera GEMC et les fichiers Geant4 data.

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

Le nom de l'archive macOS contient les versions de macOS et de Clang de la machine de compilation ; il varie donc
au fil du temps. Déterminez-le à partir de la version `{{ page.binary_tag }}`, puis téléchargez et décompressez l'archive :

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
Après l'installation, chargez le fichier d'environnement de GEMC dans le shell courant. Ajoutez cette ligne à
`.bashrc` ou `.zshrc` pour que l'environnement soit disponible dans chaque shell :

```shell
source /path/to/gemc/gemc.env
```

Exécutez quelques vérifications pour confirmer l'installation :

```shell
gemc -v
test_gdynamic_plugin_load
test_gdata_event_verbose
```


<br/>

## Compiler à partir des sources

Vous aurez besoin de Geant4 pour compiler GEMC. Consultez les
[prérequis logiciels et l'installation de Geant4 pour la compilation de
GEMC](#software-prerequisites-and-geant4-installation-for-the-gemc-build)
dans l'annexe pour connaître la liste complète des prérequis.

<br/>

### 1. Obtenir les sources

Téléchargez le code :

{% capture tab1 %}
Téléchargez la dernière version :

```shell
git clone -c advice.detachedHead=false --branch {{ page.latest_tag }} {{ page.repo_link }}
cd src
```

{% endcapture %}

{% capture tab2 %}
Clonez le dépôt pour compiler la version de développement quotidienne :

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

### 2. Configurer la compilation et installer GEMC

Le système de compilation [Meson](https://mesonbuild.com) est utilisé pour compiler et installer GEMC.

La phase de **configuration** vérifiera les dépendances requises et récupérera les bibliothèques externes.
Ici, nous utilisons un répertoire `build`.

```shell
meson setup build --prefix=/path/to/install/gemc
```

La phase d'**installation** compilera et installera GEMC. Ici, nous utilisons `-q` pour une compilation silencieuse.

```shell
meson install -C build -q
```

Après l'installation, vous pouvez exécuter `meson test -C build` pour tester GEMC avec la configuration choisie.

<br/>

### Options de compilation

- L'option de configuration `-Droot=enabled` ajoutera la prise en charge de ROOT (ROOT doit être installé sur votre système).
- L'option de configuration `-Di_test=true` activera les interfaces graphiques dans les tests.
- Utilisez `-v` lors de la compilation ou des tests pour obtenir une sortie détaillée.
- Pour supprimer le répertoire de compilation et recommencer, utilisez `rm -rf build`, puis relancez la configuration.
- Utilisez `-jN` pour définir le nombre de threads lors de la compilation.

<br/>

### Après l'installation

Ajoutez ces lignes au fichier de configuration de votre shell (par exemple `~/.bashrc` ou `~/.zshrc`) :

```shell
export PATH=/path/to/install/gemc/bin:/path/to/install/gemc/python_env/bin:$PATH
```

La seconde entrée de PATH ajoute l'environnement virtuel Python fourni afin que `python3`
désigne l'interpréteur de cet environnement, ce qui rend `import pygemc`
disponible dans vos scripts.

Vérifiez le simulateur et les outils Python installés avec :

```shell
gemc -v
gemc-system-template --help
gemc-analyzer --help
```


<br/>

### Systèmes de détecteurs CLAS12 à partir des sources

Les systèmes de détecteurs CLAS12
([`clas12-systems`](https://github.com/gemc/clas12-systems)) 0.3 se compilent selon la même procédure Meson et ne
nécessitent plus de GEMC préinstallé. Dans un environnement ne disposant que de Geant4 — par exemple une image
Docker [`g4install`](https://github.com/gemc/g4install) — la compilation inclut automatiquement GEMC à partir du
sous-projet `gemc` et l'installe dans le même préfixe, ce qui permet d'installer la géométrie des détecteurs et les
plugins entièrement à partir de zéro. Seul Geant4 doit déjà être présent (il n'est jamais compilé) ; GEMC est
recherché, dans l'ordre, à l'emplacement explicitement indiqué par `-Duse-gemc-location=<dir>`, parmi les
installations déjà disponibles via `PATH`/pkg-config, puis dans le sous-projet compilé à partir des sources.

```shell
git clone --depth=1 --branch {{ page.latest_ctag }} https://github.com/gemc/clas12-systems
cd clas12-systems
meson setup build --prefix="$PWD/install"   # builds GEMC too if none is installed
meson compile -C build
meson install -C build
```

À venir dans la prochaine version : lors de la compilation avec un GEMC déjà installé, la procédure de compilation
de CLAS12 installe ou met également à jour `pygemc` et ses outils en ligne de commande sous `python_env`, selon la
même organisation que l'installation autonome de GEMC.


<br/><br/>

## Exécuter dans un conteneur Docker

Vous pouvez utiliser Docker pour exécuter GEMC. Les images disponibles sont répertoriées ci-dessous.
Les architectures `arm64` et `amd64` sont prises en charge (sauf pour les images Arch Linux, disponibles
uniquement pour `amd64` [^1]).

{:.zebra}

| Système d'exploitation | Version de GEMC | Adresse du registre | arm64 | amd64 |
|----|--------------|------------------|-------|-------|
{% for img in site.data.docker.images -%}
| {{ img.id }} {{ img.osversion }} | {{ img.gemcv }} | ```{{ img.tag }}``` | {{ img.arm64 }} | {{ img.amd64 }} |
{% endfor %}

Les adresses ci-dessus désignent les images [Docker Hub](https://hub.docker.com/r/gemc/gemc), publiées dans le cadre
du programme [Docker-Sponsored Open Source](https://www.docker.com/community/open-source/application/), qui autorise
un nombre illimité de téléchargements anonymes. Ces images sont des copies de référence de celles produites sur
[GitHub Container Registry](https://github.com/gemc/src/pkgs/container/src) : les deux registres proposent des
contenus et des étiquettes identiques. Pour les télécharger depuis GHCR, remplacez le préfixe `docker.io/gemc/gemc:`
par `ghcr.io/gemc/src:` en conservant la même étiquette, par exemple `ghcr.io/gemc/src:dev-ubuntu-24.04`.

Il est recommandé de monter un répertoire local pour enregistrer et conserver votre travail.
À titre d'illustration, les commandes ci-dessous associent le chemin du conteneur `{{ page.docker_remote_mount }}`
à `{{ page.docker_local_mount }}` et utilisent l'image `{{ site.data.docker.images[0].tag }}`.

[^1]: Sur un Mac Apple Silicon, ajoutez l'option `--platform linux/amd64` à la commande `docker run` pour utiliser les
images `archlinux amd64`.

<br/>

### Mode par lots

```
docker run -it --rm -v {{ page.docker_local_mount }}:{{ page.docker_remote_mount}} {{ site.data.docker.images[0].tag }} bash
```

<br/>

### Interface graphique dans le navigateur

Définissez ces variables pour faciliter la session interactive. Choisissez votre propre mot de passe :

```shell
VPORTS=(-p 6080:6080 -p 5900:5900)
VNC_PASS=(-e X11VNC_PASSWORD=change-me)
VNC_BIND=(-e VNC_BIND=0.0.0.0)
GEO_FLAGS=(-e GEOMETRY=1920x1200)
```

```shell
docker run -it --rm -v {{ page.docker_local_mount }}:{{ page.docker_remote_mount}} $VPORTS $VNC_BIND $VNC_PASS $GEO_FLAGS {{ site.data.docker.images[0].tag }}
```

Ouvrez ensuite [`http://localhost:6080/vnc.html`](http://localhost:6080/vnc.html) dans votre navigateur pour accéder
à l'interface graphique.

<br/>



## Exécuter avec Apptainer

Les hôtes Linux peuvent utiliser `apptainer` (anciennement `singularity`) pour exécuter des conteneurs Docker.
Vous pouvez l'utiliser avec les images Docker ci-dessus. Il fonctionne de manière similaire à Docker, mais le
script du point d'entrée doit être chargé explicitement dans le shell courant.

```
apptainer exec --cleanenv --bind {{ page.docker_local_mount }}:{{ page.docker_remote_mount}} docker://{{ site.data.docker.images[0].tag }} bash
```

Ensuite :

```
source /usr/local/bin/docker-entrypoint.sh
gemc -v
```

<br/>

> [!WARNING]
> L'interface graphique, en particulier les fenêtres OpenGL, peut ne pas fonctionner correctement dans Apptainer
> lorsque vous vous connectez via un hôte distant.


<br/>

<blockquote class="doc-important" markdown="1">
**Remarque**

Apptainer utilise un répertoire de cache par défaut pour stocker les images. S'il est plein, placez le cache et les
répertoires temporaires à un emplacement disposant de suffisamment d'espace disque.
Par exemple, faites pointer `sim_cache` vers un emplacement disposant de suffisamment d'espace :

```shell
	export sif_cache=/path/to/$USER/cache
```

définissez ensuite ces variables :

```shell
	export APPTAINER_CACHEDIR=$sif_cache/apptainer-cache
	export APPTAINER_TMPDIR=$sif_cache/apptainer-tmp
	export TMPDIR=$sif_cache/apptainer-tmp
```

et relancez apptainer.
</blockquote>


<br/><br/><br/>

# Annexe

<br/>

## Prérequis logiciels pour l'installation binaire

<br/>

Les installations par archive binaire ne nécessitent que les paquets d'exécution requis par l'exécutable `gemc` et
les outils permettant de télécharger et de décompresser l'archive. ROOT est délibérément exclu de cette liste.

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

Le binaire est lié à Qt, SQLite, expat, zlib et TBB fournis par Homebrew ; XQuartz fournit l'environnement
d'exécution X11/OpenGL utilisé pour la visualisation.

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

## Prérequis logiciels et installation de Geant4 pour la compilation de GEMC

<br/>

- Outils de compilation et compilateurs :

    - Compilateur C++ et bibliothèque standard prenant en charge C++20 pour GEMC 0.5 ou une version ultérieure —
      GCC 11+, Clang 13+ ou Apple Clang 14+ ; chaque plateforme prise en charge fournit déjà un compilateur adapté
    - [CMake](https://cmake.org) 3.16 ou une version ultérieure
    - [Meson](https://mesonbuild.com) 1.10.1 ou une version ultérieure

<br/>

- Paquets système (généralement installés avec le gestionnaire de paquets de votre système) :

    - expat : 2.0.1 ou une version ultérieure
    - zlib : 1.2.3 ou une version ultérieure
    - [Qt6](https://www.qt.io) : 6.4.2 ou une version ultérieure (requis pour l'interface graphique) ; SVG fournit
      les icônes de la barre d'outils et Charts active l'Analyzer de l'interface graphique, mais les deux modules
      sont facultatifs
    - [ROOT](https://root.cern) : 6.36.04 ou une version ultérieure (facultatif, requis pour la sortie ROOT)

<br/>

Commandes d'installation en une ligne pour les paquets de base et les dépendances sur macOS et quelques distributions Linux courantes :

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

- Bibliothèques externes, compilées à partir des sources selon la même norme C++ que GEMC (C++20 pour GEMC 0.5 ou une version ultérieure) :

    - [CLHEP](https://proj-clhep.web.cern.ch/proj-clhep/) : 2.4.6.0 ou une version ultérieure
    - [Xerces-C](https://xerces.apache.org/xerces-c/) : 3.2 ou une version ultérieure
    - [Geant4](https://geant4.web.cern.ch) : 11.3.2 ou une version ultérieure

<br/>

> [!IMPORTANT]
> GEMC peut utiliser n'importe quelle installation personnalisée de `CLHEP`/`Xerces-C`/`Geant4`, mais
> **nous recommandons d'utiliser le dépôt [g4install](https://github.com/gemc/g4install) pour installer Geant4**,
> car il permet la coexistence de plusieurs versions de Geant4 et fournit des scripts d'installation.

<br/>

## Plateformes prises en charge et testées

- macOS : 26 (Apple Silicon, `arm64`)
  {% for img in site.data.docker.images -%}
  {% if img.gemcv == "dev" %}
- {{ img.id }} : {{ img.osversion }}
  {% endif %}>
  {% endfor %}

<br/>
<br/>
<br/>
