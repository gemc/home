---
layout: default
title: "インストール"
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
lang: ja
human_reviewed: false
---

### ライセンス

[ライセンス条件](/home/license/)をご覧ください。

<br/>

### リリースノート

- `gemc` [{{ page.latest_tag }}][gemc-release] {{ page.latest_release_date }}{: .meta }
- `pygemc` [{{ page.latest_pytag }}][pygemc-release] {{ page.latest_prelease_date }}{: .meta }
- `clas12-systems` [{{ page.latest_ctag }}][clas12-release] {{ page.latest_crelease_date }}{: .meta }
- [`dev`]({{ page.release_notes }}/tag/{{ page.development_tag }}) {{ page.development_release_date }}{: .meta }

[gemc-release]: {{ page.release_notes }}/tag/{{ page.latest_tag }}
[pygemc-release]: {{ page.prelease_notes }}/tag/{{ page.latest_pytag }}
[clas12-release]: {{ page.crelease_notes }}/tag/{{ page.latest_ctag }}

<br/>

[ストリーミング読み出し](/home/documentation/sro/plugins/)には、GEMC 0.5 の SRO インターフェイスと、
同じ GEMC インストールを使用して再ビルドした実験用プラグインが必要です。FT-Cal の JLAB エンコーダは
`clas12-systems` に含まれます。`pygemc` のみをインストールしても、ネイティブの SRO 実装は提供されません。

[頂点および角度の例](/home/examples/basic/generator_manipulations)には、
11 個のステアリングカードと準備済みの Analyzer プロットが含まれます。GEMC 0.5 以降を使用してください。
GUI のプロットには Qt Charts が必要です。これらのバッチシミュレーションと CSV チェックは Qt Charts がなくても動作します。

## 目次

- [Python API のインストール](#install-the-python-api)
- [コンパイル済みバイナリ配布物のダウンロード](#download-a-precompiled-binary-distribution)
- [ソースからのビルド](#build-from-source)
- [Docker コンテナでの実行](#run-in-a-docker-container)
- [Apptainer を使った実行](#run-using-apptainer)

- *付録*:
  - [バイナリインストールのためのソフトウェア要件](#software-prerequisites-for-binary-installation)
  - [GEMC ビルドのためのソフトウェア要件と Geant4
    インストール](#software-prerequisites-and-geant4-installation-for-the-gemc-build)
  - [サポート対象およびテスト済みのプラットフォーム](#supported-and-tested-platforms)

<br/><br/>

## Python API のインストール

<br/>

`pygemc` は [PyPI](https://pypi.org/project/pygemc/) から入手できます。
直接 `pip` でインストールする場合は仮想環境を使用してください:

```shell
python3 -m venv ~/venv/pygemc
source ~/venv/pygemc/bin/activate
python -m pip install pygemc
```

PyVista の VTK エクスポートで使用されるオプションの Jupyter モジュールは、次のコマンドでインストールできます:

```shell
python -m pip install "pygemc[jupyter]"
```

オプションの ROOT ファイル解析用の依存パッケージは、次のコマンドでインストールできます:

```shell
python -m pip install "pygemc[root]"
```

[PyPI](https://pypi.org/project/pygemc/) からのインストールでは `gemc` 実行ファイルはインストールされませんが、
`pygemc` を使ってジオメトリの作成と可視化、または結果の解析を行えます。

<br/>

## コンパイル済みバイナリ配布物のダウンロード

バイナリの tarball には `gemc` 実行ファイルと例が含まれます（ただし `pygemc` は含まれません）。Linux 向けの
ビルドは `amd64` と `arm64` で提供され、macOS 向けのビルドは Apple Silicon（`arm64`）ネイティブです。

tarball を展開する前に、必ず[バイナリインストールのためのソフトウェア要件](#software-prerequisites-for-binary-installation)
を確認してください。

まずインストール先のディレクトリを選択します:

```shell
gemc_home=/path/to/gemc
mkdir -p "$gemc_home"
cd "$gemc_home"
```

次に、お使いの Linux ディストリビューションと CPU アーキテクチャに合ったタブのコマンドを使用します。
これにより GEMC と Geant4 data ファイルがインストールされます。

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

macOS のアセット名には、ビルドホストの macOS および Clang のバージョンが含まれるため、正確な名前は時期によって変わります。
`{{ page.binary_tag }}` リリースから名前を取得し、ダウンロードして展開してください:

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
インストール後に、GEMC 環境ファイルを source コマンドで読み込んでください。すべてのシェルで利用できるようにするには、
`.bashrc` または `.zshrc` にこの行を追加します:

```shell
source /path/to/gemc/gemc.env
```

インストールを検証するために、いくつかのチェックを実行します:

```shell
gemc -v
test_gdynamic_plugin_load
test_gdata_event_verbose
```


<br/>

## ソースからのビルド

GEMC をビルドするには Geant4 が必要です。要件の完全な一覧については、付録の
[GEMC ビルドのためのソフトウェア要件と Geant4
インストール](#software-prerequisites-and-geant4-installation-for-the-gemc-build)
を確認してください。

<br/>

### 1. ソースの取得

コードをダウンロードします:

{% capture tab1 %}
最新リリースをダウンロードします:

```shell
git clone -c advice.detachedHead=false --branch {{ page.latest_tag }} {{ page.repo_link }}
cd src
```

{% endcapture %}

{% capture tab2 %}
ナイトリー開発版をビルドするにはリポジトリをクローンします:

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

### 2. ビルドの構成と GEMC のインストール

GEMC のコンパイルとインストールには [Meson](https://mesonbuild.com) ビルドシステムを使用します。

**setup** フェーズでは、必要な依存関係をチェックし、外部ライブラリを取得します。
ここでは `build` ディレクトリを使用します。

```shell
meson setup build --prefix=/path/to/install/gemc
```

**install** フェーズでは GEMC をビルドしてインストールします。ここでは `-q` を使用してビルド時の出力を抑えます。

```shell
meson install -C build -q
```

必要に応じて、インストール後に `meson test -C build` を実行して、構成した GEMC ビルドをテストします。

<br/>

### ビルドオプション

- setup オプション `-Droot=enabled` を指定すると ROOT サポートが追加されます（システムに ROOT がインストールされている必要があります）。
- setup オプション `-Di_test=true` を指定すると、テストで GUI インターフェイスが有効になります。
- ビルド/テスト時に `-v` を使用すると詳細な出力が得られます。
- ビルドディレクトリを消去してやり直すには、`rm -rf build` を実行してから setup を再実行します。
- コンパイル時のスレッド数を設定するには `-jN` を使用します。

<br/>

### インストール後の作業

シェルの設定ファイル（例: `~/.bashrc` または `~/.zshrc`）に次の行を追加してください:

```shell
export PATH=/path/to/install/gemc/bin:/path/to/install/gemc/python_env/bin:$PATH
```

2 番目の PATH エントリは、バンドルされた Python 仮想環境を追加します。これにより `python3` が
仮想環境のインタープリタを指すようになり、スクリプト内で `import pygemc` を
使用できるようになります。

インストールされたシミュレータと Python ツールを次のコマンドで確認します:

```shell
gemc -v
gemc-system-template --help
gemc-analyzer --help
```


<br/>

### ソースからの CLAS12 検出器システムのビルド

CLAS12 検出器システム
（[`clas12-systems`](https://github.com/gemc/clas12-systems)）0.3 は、同じ Meson の手順でビルドでき、
GEMC の事前インストールが不要になりました。Geant4 だけがインストールされた環境（例えば
[`g4install`](https://github.com/gemc/g4install) Docker イメージ）では、ビルド時に `gemc` サブプロジェクトから
GEMC を自動的にコンパイルし、同じインストール先プレフィックスにインストールするため、検出器のジオメトリとプラグインを
ゼロからインストールできます。Geant4 のみを事前にインストールしておく必要があります（Geant4 自体はビルドされません）。
使用する GEMC は、明示的な `-Duse-gemc-location=<dir>`、`PATH`/pkg-config で見つかるインストール済みの GEMC、
最後にソースからビルドするサブプロジェクトの順で選択されます。

```shell
git clone --depth=1 --branch {{ page.latest_ctag }} https://github.com/gemc/clas12-systems
cd clas12-systems
meson setup build --prefix="$PWD/install"   # builds GEMC too if none is installed
meson compile -C build
meson install -C build
```


<br/><br/>

## Docker コンテナでの実行

Docker を使って GEMC を実行できます。利用可能なイメージを以下に示します。
`arm64` と `amd64` の両方がサポートされています（Arch Linux イメージは `amd64` のみ [^1]）。

{:.zebra}

| OS | GEMC バージョン | レジストリアドレス | arm64 | amd64 |
|----|--------------|------------------|-------|-------|
{% for img in site.data.docker.images -%}
| {{ img.id }} {{ img.osversion }} | {{ img.gemcv }} | ```{{ img.tag }}``` | {{ img.arm64 }} | {{ img.amd64 }} |
{% endfor %}

上記のアドレスは [Docker Hub](https://hub.docker.com/r/gemc/gemc) のイメージを指し、
[Docker-Sponsored Open Source](https://www.docker.com/community/open-source/application/) プログラムを通じて
公開されているため、匿名での無制限のプルが可能です。これらは、正式な
[GitHub Container Registry](https://github.com/gemc/src/pkgs/container/src) ビルドのミラーです。2 つのレジストリは
同一の内容とタグを保持しています。代わりに GHCR からプルするには、`docker.io/gemc/gemc:` プレフィックスを
`ghcr.io/gemc/src:` に置き換え、同じタグを使用します。例: `ghcr.io/gemc/src:dev-ubuntu-24.04`。

作業内容を保存・保管するために、ローカルディレクトリをバインドすることをおすすめします。
例として、以下のコマンドではコンテナのパス `{{ page.docker_remote_mount }}` を
`{{ page.docker_local_mount }}` にバインドし、イメージ `{{ site.data.docker.images[0].tag }}` を使用します。

[^1]: Apple Silicon の Mac では、`archlinux amd64` イメージを使用する場合、`docker run` コマンドに
`--platform linux/amd64` オプションを追加してください。

<br/>

### バッチモード

```
docker run -it --rm -v {{ page.docker_local_mount }}:{{ page.docker_remote_mount}} {{ site.data.docker.images[0].tag }} bash
```

<br/>

### ブラウザのグラフィカルインターフェイス

対話型セッションで使う補助変数を次のように設定します。パスワードはご自身で選んでください:

```shell
VPORTS=(-p 6080:6080 -p 5900:5900)
VNC_PASS=(-e X11VNC_PASSWORD=change-me)
VNC_BIND=(-e VNC_BIND=0.0.0.0)
GEO_FLAGS=(-e GEOMETRY=1920x1200)
```

```shell
docker run -it --rm -v {{ page.docker_local_mount }}:{{ page.docker_remote_mount}} $VPORTS $VNC_BIND $VNC_PASS $GEO_FLAGS {{ site.data.docker.images[0].tag }}
```

次に、ブラウザで [`http://localhost:6080/vnc.html`](http://localhost:6080/vnc.html) にアクセスして、
グラフィカルインターフェイスを利用します。

<br/>



## Apptainer を使った実行

Linux ホストでは `apptainer`（旧称 `singularity`）を使って Docker コンテナを実行できます。
上記の Docker イメージで使用できます。Docker と同様に実行できますが、エントリポイントは明示的に
source コマンドで読み込む必要があります。

```
apptainer exec --cleanenv --bind {{ page.docker_local_mount }}:{{ page.docker_remote_mount}} docker://{{ site.data.docker.images[0].tag }} bash
```

次に:

```
source /usr/local/bin/docker-entrypoint.sh
gemc -v
```

<br/>

> [!WARNING]
> グラフィカルインターフェイス、特に OpenGL ウィンドウは、リモートホスト経由で接続している場合、
> Apptainer で正しく動作しないことがあります。


<br/>

<blockquote class="doc-important" markdown="1">
**注記**

Apptainer はイメージを保存するためにデフォルトのキャッシュディレクトリを使用します。これがいっぱいになった場合は、
十分なディスク容量のある場所にキャッシュディレクトリと一時ディレクトリを設定してください。
例えば、`sim_cache` を十分な容量のある場所に設定します:

```shell
	export sif_cache=/path/to/$USER/cache
```

次にこれらの変数を設定します:

```shell
	export APPTAINER_CACHEDIR=$sif_cache/apptainer-cache
	export APPTAINER_TMPDIR=$sif_cache/apptainer-tmp
	export TMPDIR=$sif_cache/apptainer-tmp
```

そして Apptainer を再度実行します。
</blockquote>


<br/><br/><br/>

# 付録

<br/>

## バイナリインストールのためのソフトウェア要件

<br/>

バイナリ tarball のインストールには、`gemc` 実行ファイルが必要とするランタイムパッケージと、アーカイブを
ダウンロードして展開するためのツールのみが必要です。ROOT は意図的にこの一覧に含めていません。

<br/>

{% capture btab1 %}

```shell
dnf install -y --allowerasing ca-certificates curl gzip tar expat sqlite-libs zlib \
libX11 libXext libXmu libXt mesa-libEGL mesa-libGL qt6-qtbase qt6-qtsvg qt6-qtcharts tbb
```

{% endcapture %}

{% capture btab2 %}

```shell
dnf install -y --allowerasing ca-certificates curl gzip tar expat sqlite-libs zlib \
libX11 libXext libXmu libXt mesa-libEGL mesa-libGL qt6-qtbase qt6-qtsvg qt6-qtcharts tbb
```

{% endcapture %}

{% capture btab3 %}

```shell
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata \
ca-certificates curl gzip tar libexpat1 libsqlite3-0 zlib1g \
libegl1 libgl1 libx11-6 libxext6 libxmu6 libxt6 \
libqt6core6t64 libqt6gui6 libqt6widgets6 libqt6opengl6 libqt6openglwidgets6 \
libqt6svg6 libqt6charts6 libtbb12
```

{% endcapture %}

{% capture btab4 %}

```shell
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata \
ca-certificates curl gzip tar libexpat1 libsqlite3-0 zlib1g \
libegl1 libgl1 libx11-6 libxext6 libxmu6 libxt6 \
libqt6core6t64 libqt6gui6 libqt6widgets6 libqt6opengl6 libqt6openglwidgets6 \
libqt6svg6 libqt6charts6 libtbb12
```

{% endcapture %}

{% capture btab5 %}

```shell
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata \
ca-certificates curl gzip tar libexpat1 libsqlite3-0 zlib1g \
libegl1 libgl1 libx11-6 libxext6 libxmu6 libxt6 \
libqt6core6t64 libqt6gui6 libqt6widgets6 libqt6opengl6 libqt6openglwidgets6 \
libqt6svg6 libqt6charts6 libtbb12
```

{% endcapture %}

{% capture btab6 %}

```shell
pacman-key --init && pacman-key --populate
pacman -Sy --noconfirm archlinux-keyring
pacman -Syu --noconfirm --needed ca-certificates curl gzip tar expat sqlite zlib \
libx11 libxext libxmu libxt mesa qt6-base qt6-svg qt6-charts tbb
```

{% endcapture %}

{% capture btab7 %}

バイナリは Homebrew の Qt、SQLite、expat、zlib、TBB にリンクされています。XQuartz が可視化で使用される
X11/OpenGL ランタイムを提供します。

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

## GEMC ビルドのためのソフトウェア要件と Geant4 インストール

<br/>

- ビルドツールおよびコンパイラ:

    - GEMC 0.5 以降では C++20 をサポートする C++ コンパイラと標準ライブラリ — GCC 11+、Clang 13+、または
      Apple Clang 14+。サポート対象のすべてのプラットフォームには、要件を満たすコンパイラが既に付属しています
    - [CMake](https://cmake.org) 3.16 以降
    - [Meson](https://mesonbuild.com) 1.10.1 以降

<br/>

- システムパッケージ（通常はシステムのパッケージマネージャでインストールします）:

    - expat: 2.0.1 以上
    - zlib: 1.2.3 以上
    - [Qt6](https://www.qt.io): 6.4.2 以上（GUI に必須）。SVG はツールバーのアイコンを提供し、Charts は
      GUI の Analyzer を有効にしますが、どちらのモジュールもオプションです
    - [ROOT](https://root.cern): 6.36.04 以上（オプション、ROOT 出力に必須）

<br/>

macOS および一部の主要な Linux ディストリビューションで、基本パッケージと依存パッケージをインストールするための 1 行コマンド:

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
qt6-charts-dev \
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
qt6-charts-dev \
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
qt6-charts-dev \
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
xterm tigervnc openbox ttf-dejavu qt6-base qt6-svg qt6-charts root gcc-libs tbb
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

- 外部ライブラリ（GEMC と同じ C++ 標準でソースからコンパイルします。GEMC 0.5 以降では C++20）:

    - [CLHEP](https://proj-clhep.web.cern.ch/proj-clhep/): 2.4.6.0 以上
    - [Xerces-C](https://xerces.apache.org/xerces-c/): 3.2 以上
    - [Geant4](https://geant4.web.cern.ch): 11.3.2 以上

<br/>

> [!IMPORTANT]
> GEMC は `CLHEP`/`Xerces-C`/`Geant4` の任意のカスタムインストールを使用できますが、
> **Geant4 のインストールには [g4install](https://github.com/gemc/g4install) リポジトリの使用をおすすめします**。
> 複数の Geant4 バージョンの共存を可能にし、インストールスクリプトも提供しているためです。

<br/>

## サポート対象およびテスト済みのプラットフォーム

- macOS: 26（Apple Silicon、`arm64`）
  {% for img in site.data.docker.images -%}
  {% if img.gemcv == "dev" %}
- {{ img.id }}: {{ img.osversion }}
  {% endif %}>
  {% endfor %}

<br/>
<br/>
<br/>
