---
layout: default
permalink: /
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

<small>本サイトは **GEMC** バージョン3以降のドキュメントです。
**CLAS12シミュレーション**には、[GEMC2 clas12Tagsリポジトリ](https://github.com/gemc/clas12Tags)を使用してください。</small>

<br/>

## Python APIによるデータベース駆動型Geant4シミュレーション

<!-- Upcoming with the next release: revised introduction. -->

**GEMC** は、検出器および放射線輸送のシミュレーションを行う、
データベース駆動型の[Geant4](https://geant4.web.cern.ch)アプリケーションです。
Python APIを使うと、Geant4コードを書かずに複雑な検出器構成を定義できます。

検出器の記述は実行ファイルから分離されています。Pythonで作成し、
ASCIIまたはSQLiteデータベースに保存すると、GEMCが実行時に読み込んでGeant4シミュレーションを実行します。

<br/>

## 主な特長

- Pythonを中心とした検出器定義
- [`pyvista`](https://pyvista.org)によるジオメトリのプレビューとVTKへのエクスポート
- ASCIIおよびSQLiteデータベース
- GDMLおよびCADファイルからのジオメトリのインポート
- Geant4/Qtによる対話的な可視化とオフスクリーン画像生成
- 組み込みの有感検出器：%%flux%%、%%dosimeter%%、%%particle_counter%%、%%gPhotonDetector%%
- ASCII、CSV、JSON、[ROOT](https://root.cern)形式でのシミュレーション出力
- GUI、コマンドライン、YAMLおよびLUNDファイルからのイベント生成
- 多重極磁場やASCII形式の磁場マップを含む磁場サポート
- シミュレーション出力（CSV、ROOT）の読み込みとプロットを行うPythonの`analyzer`モジュール
- ジオメトリのバリエーションとラン番号に応じた設定

GEMCは、独自のGeant4アプリケーションを書かずに検出器システムの試作を行えるよう支援することを目指しています。
C++プラグインにより、独自の検出器応答、磁場、イベント生成器、出力形式にも対応できます。


<br/>

## GEMCを試す

インストールは不要です。バッジをクリックすると、ブラウザ上で **JupyterLab** セッションを起動できます：

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

ローカル環境またはHPC環境でのJupyterLabセッションには、ビルド済みのマルチアーキテクチャイメージを使用してください：

```shell
# Docker
docker run --rm -p 8888:8888 ghcr.io/gemc/binder-tutorials:latest

# Apptainer
apptainer pull gemc-binder-tutorials.sif docker://ghcr.io/gemc/binder-tutorials:latest
apptainer exec gemc-binder-tutorials.sif jupyter lab --ip=0.0.0.0 --no-browser
```

<br/><br/>

## インタラクティブ3Dギャラリー

各サムネイル内で、マウスホイールまたは矢印キーを使ってカメラを回転できます。
タイトルのリンクをクリックすると、ドキュメントが表示されます。

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

## `pygemc`：Python API

GEMCのPython APIである`pygemc`は、ジオメトリおよび物質のデータベース作成機能、
`pyvista`によるジオメトリの可視化、`gemc-system-template`、`gemc-analyzer`を提供します。
解析ツールはGEMCのCSVおよびROOT出力を読み込み、選択した変数のヒストグラムを描画できます。

{% include figure.html
src="/assets/images/gemc_showcase.gif"
alt="Python API example"
caption="  
The code fills the database with the world volume, a liquid hydrogen target, and a flux plane. <br/>
The `pyvista` option gives immediate geometry visualization. <br/>
In the GEMC simulation, hits are created from particles generated by a beam of protons impinging
on the liquid hydrogen target.<br/>
The total deposited energy is plotted with the `analyzer` module."
%}

以下のコード抜粋では、標的の下流にある有感なフラックス検出面を定義しています。
生成されたトラックがこのボリュームを横切るたびに、GEMCは %%flux%% ヒットを記録します。

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

検出器定義はデータベースに保存されます。標準的なワークフローでは、ユーザーが記述を行うのは1つのステップです：

{% include figure.html
src="/assets/images/gemcArchitecture.svg"
alt="Database-driven architecture"
caption="
Users define detector databases through the Python API (Step 1).
GEMC then builds Geant4 objects, transports particles to create hits, applies digitization and electronics emulation,
and streams the output data (Steps 2–5).
"
%}

<br/>


> [!NOTE]
> シミュレーションの実行に、C++やGeant4の事前知識は必要ありません。
> 基本的なPythonの知識があると、複雑な構成を整理するのに役立ちます。
> ユーザーは **独自のハードウェアエミュレーションルーチンを定義する** こともできます。
> この場合、複雑なデジタイゼーション処理には基本的なC++の知識が役立ちます。

<br/><br/>

## ジオメトリのバリエーション

検出器は、構成要素の位置の変更、物質の変更、ボリュームの追加や削除といった設定変更を加えることで、
複数の実験で再利用できます。
GEMCは、%%variation%% 文字列や %%run%% 番号を用いてこれらのジオメトリのバージョンに対応し、
さまざまなシミュレーション構成に適応できます。

{% include figure.html
src="/assets/images/clas12v.gif"
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
  <a href="{{ "/feed.xml" | relative_url }}">RSSフィード</a>
</p>

<br/><br/>

## 継続的インテグレーション

GEMCは、GitHub CIにより、複数のプラットフォームとARM64およびAMD64の両アーキテクチャで
ビルドとテストが行われ、Dockerイメージとしてデプロイされます。

**gemc**

{:.zebra}

| テスト | [![テスト][test-badge]][test] |
| サニタイザー | [![サニタイザー][Sanitize-badge]][Sanitize] |
| CodeQL | [![CodeQL][CodeQL-badge]][CodeQL] |
| イメージのデプロイ | [![デプロイ][deploy-badge]][deploy] |
| バイナリのtarアーカイブ | [![バイナリのtarアーカイブ][Binary-Tarballs-badge]][Binary-Tarballs] |
| macOS用tarアーカイブ | [![macOS用tarアーカイブ][macOS-Tarball-badge]][macOS-Tarball] |
| ナイトリーリリース | [![ナイトリー][Nightly-badge]][Nightly] |
| ホームページ | [![サイト][Site-badge]][Site] |
| Dockerプル数 | [![Dockerプル数][DockerHub-badge]][DockerHub] |
| Doxygen | [![ドキュメント][Docs-badge]][Docs] |
| リリースのtarアーカイブ | [![リリースのtarアーカイブ][Release-Tarballs-badge]][Release-Tarballs] |

**pygemc**

{:.zebra}

| 開発版ナイトリーリリース | [![開発版ナイトリーリリース][PyGemc-Nightly-badge]][PyGemc-Nightly] |
| PyPIへの公開 | [![PyPIへの公開][PyGemc-Publish-badge]][PyGemc-Publish] |
| テスト | [![pygemcテスト][PyGemc-Tests-badge]][PyGemc-Tests] |
| PyPI | [![pygemc PyPI][PyPI-badge]][PyPI] |

<br/><br/>

## 参考文献

GEMCを使用する場合は、必ず以下の論文を引用してください：

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

[GEMCのソースコード](https://github.com/gemc/src)は、
[Apache License, Version 2.0](/home/license/)に基づいて提供されています。帰属表示と
サードパーティへの謝辞については、[NOTICE](/home/license/#notice)を参照してください。
本ソフトウェアは、Geant4、CLHEP、Qt、ROOT、SQLite、Assimpなど、個別のライセンスが適用されるサードパーティ製コンポーネントにも依存しています。

<br/><br/>

<hr/>
