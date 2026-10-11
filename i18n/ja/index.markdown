---
layout: default
lang: ja
human_reviewed: false
---

[test]: https://github.com/gemc/src/actions/workflows/test.yml

[test-badge]: https://github.com/gemc/src/actions/workflows/test.yml/badge.svg

[deploy]: https://github.com/gemc/src/actions/workflows/deploy.yml

[deploy-badge]: https://github.com/gemc/src/actions/workflows/deploy.yml/badge.svg

[DockerHub]: https://hub.docker.com/r/gemc/gemc

[DockerHub-badge]: https://img.shields.io/docker/pulls/gemc/gemc.svg

[Docs]: https://github.com/gemc/src/actions/workflows/doxygen.yml

[Docs-badge]: https://github.com/gemc/src/actions/workflows/doxygen.yml/badge.svg

[Nightly]: https://github.com/gemc/src/actions/workflows/dev_release.yml

[Nightly-badge]: https://github.com/gemc/src/actions/workflows/dev_release.yml/badge.svg

[Site]: https://github.com/gemc/home/actions/workflows/jekyll.yml

[Site-badge]: https://github.com/gemc/home/actions/workflows/jekyll.yml/badge.svg

[Sanitize]: https://github.com/gemc/src/actions/workflows/sanitize.yml

[Sanitize-badge]: https://github.com/gemc/src/actions/workflows/sanitize.yml/badge.svg

[CodeQL]: https://github.com/gemc/src/actions/workflows/codeql.yml

[CodeQL-badge]: https://github.com/gemc/src/actions/workflows/codeql.yml/badge.svg

[Binary-Tarballs]: https://github.com/gemc/src/actions/workflows/binary_tarballs.yml

[Binary-Tarballs-badge]: https://github.com/gemc/src/actions/workflows/binary_tarballs.yml/badge.svg

[macOS-Tarball]: https://github.com/gemc/src/actions/workflows/macos_tarball.yml

[macOS-Tarball-badge]: https://github.com/gemc/src/actions/workflows/macos_tarball.yml/badge.svg

[Release-Tarballs]: https://github.com/gemc/src/actions/workflows/release_tarballs.yml

[Release-Tarballs-badge]: https://github.com/gemc/src/actions/workflows/release_tarballs.yml/badge.svg?event=release

[PyPI]: https://pypi.org/project/pygemc/

[PyPI-badge]: https://img.shields.io/pypi/v/pygemc.svg?cacheSeconds=300

[PyGemc-Nightly]: https://github.com/gemc/pygemc/actions/workflows/dev_release.yml

[PyGemc-Nightly-badge]: https://github.com/gemc/pygemc/actions/workflows/dev_release.yml/badge.svg

[PyGemc-Publish]: https://github.com/gemc/pygemc/actions/workflows/publish_pypi.yml

[PyGemc-Publish-badge]: https://github.com/gemc/pygemc/actions/workflows/publish_pypi.yml/badge.svg

[PyGemc-Tests]: https://github.com/gemc/pygemc/actions/workflows/pygemc_tests.yml

[PyGemc-Tests-badge]: https://github.com/gemc/pygemc/actions/workflows/pygemc_tests.yml/badge.svg


{% include gemc-logo.svg %}

<small>本サイトは **GEMC** バージョン 3 以降を対象としたドキュメントです。
**CLAS12 シミュレーション** には [GEMC2 clas12Tags リポジトリ](https://github.com/gemc/clas12Tags) をご利用ください。</small>

<br/>

## Python API によるデータベース駆動の Geant4 シミュレーション

**GEMC** は Python から使いやすい [Geant4](https://geant4.web.cern.ch) のラッパーで、C++/Geant4 の習得を不要にします。
ユーザーは Python で検出器システム全体のジオメトリ、材料、デジタイゼーションを構築します。
API は、GEMC がシミュレーションパイプライン全体を実行するために使用するデータベースに、データを自動的に登録します。

主な特長:

- ジオメトリと材料を作成するための Python API
- ASCII、SQLite、GDML、CAD メッシュファイルからのジオメトリインポート
- 組み込みの感応検出器: %%flux%%、%%dosimeter%%、%%particle_counter%%、%%gPhotonDetector%%
- 出力フォーマット: ASCII、CSV、JSON、[ROOT](https://root.cern)
- シミュレーション出力の読み込みとプロットを行う組み込み Python `analyzer` モジュール
- [`pyvista`](https://pyvista.org) によるジオメトリの可視化
- ジオメトリのバリエーションおよびラン番号に依存する構成
- CI でテストされたビルドと Docker によるデプロイ

<br/><br/>

## GEMC を試す

インストールは不要です。バッジをクリックすると、ブラウザ内で **JupyterLab** セッションが起動し、その場で操作できます:

{% assign visible_examples = site.data.examples | where: "display", true %}


<table class="zebra compact-table">
  <tbody>
    {% for example in visible_examples %}
    <tr>
      <td>
        <a href="{{ example.binder }}" target="_blank" rel="noopener noreferrer">
          <img src="{{ example.badge }}" alt="{{ example.title }}">
        </a>
      </td>
      <td>{{ example.header }}</td>
    </tr>
    {% endfor %}
  </tbody>
</table>

<br/>

### コンテナイメージ

ローカルまたは HPC 上での JupyterLab セッションには、ビルド済みのマルチアーキテクチャイメージをご利用ください:

```shell
# Docker
docker run --rm -p 8888:8888 ghcr.io/gemc/binder-tutorials:latest

# Apptainer
apptainer pull gemc-binder-tutorials.sif docker://ghcr.io/gemc/binder-tutorials:latest
apptainer exec gemc-binder-tutorials.sif jupyter lab --ip=0.0.0.0 --no-browser
```

<br/><br/>

## インタラクティブ 3D ギャラリー

各サムネイル内でマウスホイールまたは矢印キーを使ってカメラを回転できます。ドキュメントを見るにはタイトルの
リンクをクリックしてください。

{% assign gallery_examples = site.data.examples | where: "gallery", true %}

<div class="gallery-grid">
  {% for example in gallery_examples %}
    <article class="gallery-card">
      <h3 class="gallery-card-title"><a href="{{ example.link }}">{{ example.title }}</a></h3>
      <iframe src="/home/assets/vtkjs-viewer.html?fileURL={{ example.vtksz }}"
        title="Interactive VTK.js view of {{ example.title }}"
        loading="lazy"></iframe>
      {% if example.header %}
        <p class="gallery-card-desc meta">{{ example.header }}</p>
      {% endif %}
    </article>
  {% endfor %}
</div>

<br/><br/>

## `pygemc`: Python API

GEMC の Python API である `pygemc` は、ジオメトリと材料のデータベース構築機能、`pyvista` によるジオメトリ可視化、
`gemc-system-template`、`gemc-analyzer` を提供します。解析ツールは GEMC の CSV および ROOT 出力を読み込み、
選択した変数のヒストグラムをプロットできます。

{% include figure.html
src="assets/images/gemc_showcase.gif"
alt="Python API example"
caption="  
The code fills the database with the world volume, a liquid hydrogen target, and a flux plane. <br/>
The `pyvista` option gives immediate geometry visualization. <br/>
In the GEMC simulation, hits are created from particles generated by a beam of protons impinging
on the liquid hydrogen target.<br/>
The total deposited energy is plotted with the `analyzer` module."
%}

以下の抜粋は、ターゲット下流にある、粒子フラックスを測定する感応面を定義しています。GEMC は、生成された飛跡が
このボリュームを横切るたびに %%flux%% ヒットを記録します。

```python
# Place a thin scoring plane downstream of the target.
flux_z = 50
flux_dx = 1
flux_dim = world_size * 0.8

# Define the plane as an air box inside the world volume.
gvolume = GVolume("FluxPlane")
gvolume.mother = "root"
gvolume.description = "Flux Scoring Plane"
gvolume.make_box(flux_dim * 0.5, flux_dim * 0.5, flux_dx * 0.5)
gvolume.material = "G4_AIR"
gvolume.color = "FAFAD2"
gvolume.set_position(0, 0, flux_z)

# Turn the volume into a GEMC flux detector and tag its output column.
gvolume.digitization = "flux"
gvolume.set_identifier("flux_plane", 1)
gvolume.publish(cfg)
 ```

<br/><br/>

## データベース

検出器の定義はデータベースに保存されます。一般的なワークフローでは、ユーザーが記述するステップは 1 つだけです:

{% include figure.html
src="assets/images/gemcArchitecture.svg"
alt="Database-driven architecture"
caption="
Users define detector databases through the Python API (Step 1).
GEMC then builds Geant4 objects, transports particles to create hits, applies digitization and electronics emulation,
and streams the output data (Steps 2–5).
"
%}

<br/>


> [!NOTE]
> シミュレーションの実行には、C++ や Geant4 の事前知識は不要です。
> 基本的な Python の知識があると、複雑なセットアップを整理するのに役立ちます。
> ユーザーは **独自のハードウェアエミュレーションルーチンを定義する** こともできます。その場合、複雑な
> デジタイゼーションには基本的な C++ の知識があると役立ちます。

<br/><br/>

## ジオメトリのバリエーション

検出器は、構成要素の位置の移動、材料の変更、
ボリュームの追加・削除といった構成変更を加えて、複数の実験で再利用できます。
GEMC は、%%variation%% 文字列および／または %%run%% 番号を使ってこうしたジオメトリの各バージョンに対応し、
さまざまなシミュレーションの
設定に適応します。

{% include figure.html
src="assets/images/clas12v.gif"
alt="Python API example"
caption="The animation shows two variations of the CLAS12 Central Detector.
The geometries are identical except for the target position. Users select them
with a variation string or run number in the configuration file or command-line options."
%}

<br/><br/>

## 最新ニュース

<div class="news-feed news-feed--compact news-feed--homepage">
  {% assign shown_posts = 0 %}

{% for post in site.posts %}
{% assign show_post = false %}
{% if post.categories contains "news" %}
{% assign show_post = true %}
{% elsif post.categories contains "release" %}
{% assign show_post = true %}
{% elsif post.categories contains "roadmap" %}
{% assign show_post = true %}
{% endif %}

    {% if show_post %}
      {% include news-card.html post=post compact=true %}
      {% assign shown_posts = shown_posts | plus: 1 %}
    {% endif %}

    {% if shown_posts == 3 %}
      {% break %}
    {% endif %}

{% endfor %}
</div>

<p class="news-links">
  <a href="{{ "/news/" | relative_url }}">すべてのニュース</a>
  ·
  <a href="{{ "/feed.xml" | relative_url }}">RSS フィード</a>
</p>

<br/><br/>

## 継続的インテグレーション

GEMC は、GitHub CI によって複数のプラットフォーム上、かつ ARM64 と AMD64 の両アーキテクチャで、Docker
イメージとしてビルド、テスト、デプロイされます。

**gemc**

{:.zebra}

| テスト      | [![test][test-badge]][test]                                  |
| サニタイザー  | [![Sanitize][Sanitize-badge]][Sanitize]                      |
| CodeQL | [![CodeQL][CodeQL-badge]][CodeQL]                            |
| イメージのデプロイ | [![deploy][deploy-badge]][deploy]                            |
| バイナリ tar アーカイブ | [![Binary Tarballs][Binary-Tarballs-badge]][Binary-Tarballs] |
| macOS tar アーカイブ | [![macOS Tarball][macOS-Tarball-badge]][macOS-Tarball]       |
| ナイトリーリリース | [![Nightly][Nightly-badge]][Nightly]                         |
| ホームページ | [![Site][Site-badge]][Site]                                  |
| Docker プル数 | [![Docker Pulls][DockerHub-badge]][DockerHub]                |
| Doxygen | [![Docs][Docs-badge]][Docs]                                  |
| リリース tar アーカイブ | [![Release Tarballs][Release-Tarballs-badge]][Release-Tarballs] |

**pygemc**

{:.zebra}

| ナイトリー開発版リリース | [![Nightly Dev Release][PyGemc-Nightly-badge]][PyGemc-Nightly]   |
| PyPI への公開     | [![Publish PyPI][PyGemc-Publish-badge]][PyGemc-Publish]          |
| テスト | [![pygemc tests][PyGemc-Tests-badge]][PyGemc-Tests]               |
| PyPI | [![pygemc PyPI][PyPI-badge]][PyPI]                               |

<br/><br/>

## 参考文献

GEMC を使用する場合は、必ず以下の論文を引用してください:

> M. Ungaro and the CLAS Collaboration, "The CLAS12 Geant4 simulation," *Nuclear Instruments and
> Methods in Physics Research Section A: Accelerators, Spectrometers, Detectors and Associated
> Equipment* **959**, 163422 (2020). <https://doi.org/10.1016/j.nima.2020.163422>

BibTeX:

```bibtex
@article{UNGARO2020163422,
  title = {The CLAS12 Geant4 simulation},
  journal = {Nuclear Instruments and Methods in Physics Research Section A: Accelerators,
             Spectrometers, Detectors and Associated Equipment},
  volume = {959},
  pages = {163422},
  year = {2020},
  issn = {0168-9002},
  doi = {https://doi.org/10.1016/j.nima.2020.163422},
  url = {https://www.sciencedirect.com/science/article/pii/S0168900220300279},
  author = {M. Ungaro and {CLAS Collaboration}},
  keywords = {Geant4, GEMC, Simulation, Software, Database, Monte Carlo, CAD, STL, GDML, MYSQL, C++}
}
```

Bibitem:

```latex
\bibitem{UNGARO2020163422}
M. Ungaro and the CLAS Collaboration,
\newblock The CLAS12 Geant4 simulation.
\newblock Nuclear Instruments and Methods in Physics Research Section A \textbf{959}, 163422 (2020).
\newblock \doi{10.1016/j.nima.2020.163422}
```

<br/><br/>

## ソースコードとライセンス

[GEMC ソースコード](https://github.com/gemc/src) は
[Apache License, Version 2.0](/home/license/) の下でライセンスされています。帰属表示およびサードパーティへの
謝辞については [NOTICE](/home/license/#notice) をご覧ください。本ソフトウェアは、Geant4、CLHEP、Qt、ROOT、
SQLite、Assimp など、個別のライセンスが適用されるサードパーティコンポーネントにも依存しています。

<br/><br/>

<hr/>
