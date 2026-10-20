---
layout: default
title: "Installazione"
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
lang: it
human_reviewed: false
---

### Licenza

Consulta le [condizioni di licenza](/home/license/).

<br/>

### Note di rilascio

- `gemc` [{{ page.latest_tag }}][gemc-release] {{ page.latest_release_date }}{: .meta }
- `pygemc` [{{ page.latest_pytag }}][pygemc-release] {{ page.latest_prelease_date }}{: .meta }
- `clas12-systems` [{{ page.latest_ctag }}][clas12-release] {{ page.latest_crelease_date }}{: .meta }
- [`dev`]({{ page.release_notes }}/tag/{{ page.development_tag }}) {{ page.development_release_date }}{: .meta }

[gemc-release]: {{ page.release_notes }}/tag/{{ page.latest_tag }}
[pygemc-release]: {{ page.prelease_notes }}/tag/{{ page.latest_pytag }}
[clas12-release]: {{ page.crelease_notes }}/tag/{{ page.latest_ctag }}

<br/>

La [lettura in streaming](/home/documentation/sro/plugins/) richiede le interfacce SRO di GEMC 0.5 e i plugin
degli esperimenti ricompilati con la stessa installazione di GEMC. L'encoder JLAB di FT-Cal
appartiene a `clas12-systems`; installare solo `pygemc` non fornisce l'implementazione SRO nativa.

Gli [esempi su vertice e angoli](/home/examples/basic/generator_manipulations)
includono 11 schede di configurazione e grafici Analyzer già predisposti. Usa GEMC 0.5 o successivo; i grafici della GUI
richiedono Qt Charts. Le relative simulazioni in batch e i controlli CSV funzionano anche senza Qt Charts.

In arrivo con il prossimo rilascio: gli strumenti Qt Linguist compilano i cataloghi linguistici della GUI durante
la build; i dati di traduzione di Qt localizzano le finestre di dialogo standard. I comandi per i pacchetti qui sotto
includono entrambi. Qt di Homebrew fornisce questi strumenti e cataloghi. La lingua della GUI viene rilevata
automaticamente e può essere impostata manualmente con l'opzione `-language=<code>`.

## Indice

- [Installare l'API Python](#install-the-python-api)
- [Scaricare una distribuzione binaria precompilata](#download-a-precompiled-binary-distribution)
- [Compilare dai sorgenti](#build-from-source)
- [Eseguire in un container Docker](#run-in-a-docker-container)
- [Eseguire con Apptainer](#run-using-apptainer)

- *Appendice*:
  - [Prerequisiti software per l'installazione binaria](#software-prerequisites-for-binary-installation)
  - [Prerequisiti software e installazione di Geant4 per la
    build di GEMC](#software-prerequisites-and-geant4-installation-for-the-gemc-build)
  - [Piattaforme supportate e testate](#supported-and-tested-platforms)

<br/><br/>

## Installare l'API Python

<br/>

`pygemc` è disponibile su [PyPI](https://pypi.org/project/pygemc/).
Usa un ambiente virtuale per le installazioni dirette con `pip`:

```shell
python3 -m venv ~/venv/pygemc
source ~/venv/pygemc/bin/activate
python -m pip install pygemc
```

I moduli Jupyter opzionali usati per l'esportazione VTK di PyVista possono essere installati con:

```shell
python -m pip install "pygemc[jupyter]"
```

Le dipendenze opzionali per l'analisi dei file ROOT possono essere installate con:

```shell
python -m pip install "pygemc[root]"
```

L'installazione da [PyPI](https://pypi.org/project/pygemc/) non include l'eseguibile `gemc`, ma consente di
creare e visualizzare geometrie o analizzare i risultati.

<br/>

## Scaricare una distribuzione binaria precompilata

I tarball binari contengono l'eseguibile `gemc` e gli esempi (ma non `pygemc`). Le build Linux sono disponibili
per `amd64` e `arm64`; la build macOS è nativa per Apple Silicon (`arm64`).

Assicurati di controllare i
[prerequisiti software per l'installazione binaria](#software-prerequisites-for-binary-installation)
prima di estrarre il tarball.

Scegli prima una directory di installazione:

```shell
gemc_home=/path/to/gemc
mkdir -p "$gemc_home"
cd "$gemc_home"
```

Poi usa i comandi della scheda corrispondente alla tua distribuzione Linux e all'architettura della CPU.
Questo installerà GEMC e i file Geant4 data.

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

Il nome dell'archivio macOS include le versioni di macOS e Clang dell'host di build, quindi varia nel tempo.
Individualo nel rilascio `{{ page.binary_tag }}`, poi scaricalo ed estrailo:

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
Dopo l'installazione, carica il file di ambiente di GEMC. Aggiungi questa riga a `.bashrc` o `.zshrc` se
vuoi rendere l'ambiente disponibile in ogni shell:

```shell
source /path/to/gemc/gemc.env
```

Esegui alcuni controlli per verificare l'installazione:

```shell
gemc -v
test_gdynamic_plugin_load
test_gdata_event_verbose
```


<br/>

## Compilare dai sorgenti

Per compilare GEMC avrai bisogno di Geant4. Consulta i
[prerequisiti software e l'installazione di Geant4 per la
build di GEMC](#software-prerequisites-and-geant4-installation-for-the-gemc-build)
nell'appendice per l'elenco completo dei requisiti.

<br/>

### 1. Ottenere i sorgenti

Scarica il codice:

{% capture tab1 %}
Scarica l'ultimo rilascio:

```shell
git clone -c advice.detachedHead=false --branch {{ page.latest_tag }} {{ page.repo_link }}
cd src
```

{% endcapture %}

{% capture tab2 %}
Clona il repository per compilare la versione di sviluppo nightly:

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

### 2. Configurare la build e installare GEMC

Il sistema di build [Meson](https://mesonbuild.com) viene usato per compilare e installare GEMC.

La fase di **configurazione** verificherà le dipendenze richieste e scaricherà le librerie esterne.
Qui usiamo una directory `build`.

```shell
meson setup build --prefix=/path/to/install/gemc
```

La fase di **installazione** compilerà e installerà GEMC. Qui usiamo `-q` per una build silenziosa.

```shell
meson install -C build -q
```

Facoltativamente, dopo l'installazione, esegui `meson test -C build` per testare la build di GEMC configurata.

<br/>

### Opzioni di build

- L'opzione di configurazione `-Droot=enabled` aggiungerà il supporto ROOT (richiede ROOT installato sul sistema).
- L'opzione di configurazione `-Di_test=true` abiliterà le interfacce GUI nei test.
- Usa `-v` in fase di build o test per un output dettagliato.
- Per cancellare la directory di build e ripartire da zero, usa `rm -rf build` e poi ripeti la configurazione.
- Usa `-jN` per impostare il numero di thread durante la compilazione.

<br/>

### Dopo l'installazione

Aggiungi queste righe al file di configurazione della tua shell (ad esempio `~/.bashrc` o `~/.zshrc`):

```shell
export PATH=/path/to/install/gemc/bin:/path/to/install/gemc/python_env/bin:$PATH
```

La seconda voce di PATH aggiunge l'ambiente virtuale Python incluso, in modo che `python3`
venga risolto nell'interprete dell'ambiente virtuale, rendendo `import pygemc`
disponibile nei tuoi script.

Controlla il simulatore installato e gli strumenti Python con:

```shell
gemc -v
gemc-system-template --help
gemc-analyzer --help
```


<br/>

### Sistemi di rivelatori CLAS12 dai sorgenti

I sistemi di rivelatori CLAS12
([`clas12-systems`](https://github.com/gemc/clas12-systems)) 0.3 si compilano con la stessa procedura Meson e non
richiedono più un'installazione preesistente di GEMC. In un ambiente con il solo Geant4, ad esempio un'immagine
Docker di [`g4install`](https://github.com/gemc/g4install), la build compila automaticamente GEMC dal
sottoprogetto `gemc` e lo installa nello stesso prefisso, così la geometria dei rivelatori e i plugin possono
essere installati interamente da zero. Solo Geant4 deve essere già presente (non viene mai compilato); GEMC
viene cercato, nell'ordine, nella posizione esplicita `-Duse-gemc-location=<dir>`, tra le installazioni già
disponibili tramite `PATH`/pkg-config e infine nel sottoprogetto da compilare dai sorgenti.

```shell
git clone --depth=1 --branch {{ page.latest_ctag }} https://github.com/gemc/clas12-systems
cd clas12-systems
meson setup build --prefix="$PWD/install"   # builds GEMC too if none is installed
meson compile -C build
meson install -C build
```

In arrivo con il prossimo rilascio: quando si compila usando un'installazione esistente di GEMC, la build CLAS12
installa o aggiorna anche `pygemc` e i suoi strumenti da riga di comando sotto `python_env`, rispecchiando la
struttura delle directory dell'installazione autonoma di GEMC.


<br/><br/>

## Eseguire in un container Docker

Puoi usare Docker per eseguire GEMC. Le immagini disponibili sono elencate di seguito.
Sono supportate sia `arm64` sia `amd64` (eccetto per le immagini Arch Linux, disponibili solo per `amd64` [^1]).

{:.zebra}

| OS | Versione GEMC | Indirizzo del registro | arm64 | amd64 |
|----|--------------|------------------|-------|-------|
{% for img in site.data.docker.images -%}
| {{ img.id }} {{ img.osversion }} | {{ img.gemcv }} | ```{{ img.tag }}``` | {{ img.arm64 }} | {{ img.amd64 }} |
{% endfor %}

Gli indirizzi qui sopra si riferiscono alle immagini su [Docker Hub](https://hub.docker.com/r/gemc/gemc),
pubblicate nell'ambito del programma
[Docker-Sponsored Open Source](https://www.docker.com/community/open-source/application/), che consente pull
anonimi illimitati. Sono repliche della build di riferimento su
[GitHub Container Registry](https://github.com/gemc/src/pkgs/container/src): i due registri contengono
contenuti e tag identici. Per effettuare il pull da GHCR, sostituisci il prefisso `docker.io/gemc/gemc:` con
`ghcr.io/gemc/src:` mantenendo lo stesso tag, ad esempio `ghcr.io/gemc/src:dev-ubuntu-24.04`.

È consigliato montare una directory locale per salvare e conservare il tuo lavoro.
A titolo illustrativo, i comandi qui sotto associano il percorso del container `{{ page.docker_remote_mount }}` a
`{{ page.docker_local_mount }}` e usano l'immagine `{{ site.data.docker.images[0].tag }}`.

[^1]: Per i Mac con Apple Silicon aggiungi l'opzione `--platform linux/amd64` al comando `docker run` se vuoi usare le
immagini `archlinux amd64`.

<br/>

### Modalità batch

```
docker run -it --rm -v {{ page.docker_local_mount }}:{{ page.docker_remote_mount}} {{ site.data.docker.images[0].tag }} bash
```

<br/>

### Interfaccia grafica nel browser

Imposta queste variabili per facilitare l'uso della sessione interattiva. Scegli una password personale:

```shell
VPORTS=(-p 6080:6080 -p 5900:5900)
VNC_PASS=(-e X11VNC_PASSWORD=change-me)
VNC_BIND=(-e VNC_BIND=0.0.0.0)
GEO_FLAGS=(-e GEOMETRY=1920x1200)
```

```shell
docker run -it --rm -v {{ page.docker_local_mount }}:{{ page.docker_remote_mount}} $VPORTS $VNC_BIND $VNC_PASS $GEO_FLAGS {{ site.data.docker.images[0].tag }}
```

Poi apri il browser all'indirizzo [`http://localhost:6080/vnc.html`](http://localhost:6080/vnc.html) per accedere
all'interfaccia grafica.

<br/>



## Eseguire con Apptainer

Gli host Linux possono usare `apptainer` (precedentemente `singularity`) per eseguire container Docker.
Puoi usarlo con le immagini Docker qui sopra. Funziona in modo simile a Docker, ma lo script di avvio deve
essere caricato esplicitamente nella shell.

```
apptainer exec --cleanenv --bind {{ page.docker_local_mount }}:{{ page.docker_remote_mount}} docker://{{ site.data.docker.images[0].tag }} bash
```

Poi:

```
source /usr/local/bin/docker-entrypoint.sh
gemc -v
```

<br/>

> [!WARNING]
> L'interfaccia grafica, in particolare le finestre OpenGL, potrebbe non funzionare correttamente in Apptainer
> quando ti colleghi tramite un host remoto.


<br/>

<blockquote class="doc-important" markdown="1">
**Nota**

Apptainer usa una directory di cache predefinita per archiviare le immagini. Se si riempie, imposta le directory
della cache e dei file temporanei in una posizione con spazio su disco sufficiente.
Ad esempio, imposta `sim_cache` su una posizione con spazio sufficiente:

```shell
	export sif_cache=/path/to/$USER/cache
```

poi imposta queste variabili:

```shell
	export APPTAINER_CACHEDIR=$sif_cache/apptainer-cache
	export APPTAINER_TMPDIR=$sif_cache/apptainer-tmp
	export TMPDIR=$sif_cache/apptainer-tmp
```

ed esegui di nuovo apptainer.
</blockquote>


<br/><br/><br/>

# Appendice

<br/>

## Prerequisiti software per l'installazione binaria

<br/>

Le installazioni da tarball binario richiedono solo i pacchetti di runtime necessari all'eseguibile `gemc` e gli
strumenti usati per scaricare ed estrarre l'archivio. ROOT è intenzionalmente escluso da questo elenco.

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

Il binario è collegato a Qt, SQLite, expat, zlib e TBB forniti da Homebrew; XQuartz fornisce il runtime X11/OpenGL
usato per la visualizzazione.

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

## Prerequisiti software e installazione di Geant4 per la build di GEMC

<br/>

- Strumenti di build e compilatori:

    - Compilatore C++ e libreria standard con supporto a C++20 per GEMC 0.5 o successivo — GCC 11+, Clang 13+ o
      Apple Clang 14+; ogni piattaforma supportata include già un compilatore adeguato
    - [CMake](https://cmake.org) 3.16 o successivo
    - [Meson](https://mesonbuild.com) 1.10.1 o successivo

<br/>

- Pacchetti di sistema (tipicamente installati con il gestore di pacchetti del sistema):

    - expat: 2.0.1 o superiore
    - zlib: 1.2.3 o superiore
    - [Qt6](https://www.qt.io): 6.4.2 o superiore (richiesto per la GUI); SVG fornisce le icone della barra degli
      strumenti e Charts abilita l'Analyzer della GUI, ma entrambi i moduli sono opzionali
    - [ROOT](https://root.cern): 6.36.04 o superiore (opzionale, richiesto per l'output ROOT)

<br/>

Comandi di installazione in una riga per i pacchetti di base e le dipendenze su macOS e alcune diffuse distribuzioni Linux:

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

- Librerie esterne, compilate dai sorgenti con lo stesso standard C++ di GEMC (C++20 per GEMC 0.5 o successivo):

    - [CLHEP](https://proj-clhep.web.cern.ch/proj-clhep/): 2.4.6.0 o superiore
    - [Xerces-C](https://xerces.apache.org/xerces-c/): 3.2 o superiore
    - [Geant4](https://geant4.web.cern.ch): 11.3.2 o superiore

<br/>

> [!IMPORTANT]
> GEMC può usare qualsiasi installazione personalizzata di `CLHEP`/`Xerces-C`/`Geant4`, tuttavia
> **consigliamo di usare il repository [g4install](https://github.com/gemc/g4install) per installare Geant4**,
> poiché consente la coesistenza di più versioni di Geant4 e fornisce script di installazione.

<br/>

## Piattaforme supportate e testate

- macOS: 26 (Apple Silicon, `arm64`)
  {% for img in site.data.docker.images -%}
  {% if img.gemcv == "dev" %}
- {{ img.id }}: {{ img.osversion }}
  {% endif %}>
  {% endfor %}

<br/>
<br/>
<br/>
