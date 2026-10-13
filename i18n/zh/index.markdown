---
layout: default
permalink: /
lang: zh
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

<small>本站提供 **GEMC** 第 3 版及更高版本的文档。
如需进行 **CLAS12 模拟**，请使用 [GEMC2 clas12Tags 仓库](https://github.com/gemc/clas12Tags)。</small>

<br/>

## 数据库驱动的 Geant4 模拟，提供 Python API

**GEMC** 是对 [Geant4](https://geant4.web.cern.ch) 的 Python 友好封装，免去了学习 C++/Geant4
的门槛。用户可以用 Python 构建完整的探测器系统，包括几何、材料和数字化。该
API 会自动填充 GEMC 运行完整模拟流程所需的数据库。

主要特性：

- 用于创建几何和材料的 Python API
- 支持从 ASCII、SQLite、GDML 和 CAD 网格文件导入几何
- 内置灵敏探测器：%%flux%%、%%dosimeter%%、%%particle_counter%% 和 %%gPhotonDetector%%
- 输出格式：ASCII、CSV、JSON 和 [ROOT](https://root.cern)
- 内置 Python `analyzer` 模块，用于读取模拟输出并绘图
- [`pyvista`](https://pyvista.org) 几何可视化
- 几何变体和随运行编号变化的配置
- 经过 CI 测试的构建以及 Docker 部署

<br/><br/>

## 试用 GEMC

无需安装。点击徽章即可在浏览器中启动一个在线 **JupyterLab** 会话：

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

### 容器镜像

若要在本地或 HPC 上运行 JupyterLab 会话，请使用预构建的多架构镜像：

```shell
# Docker
docker run --rm -p 8888:8888 ghcr.io/gemc/binder-tutorials:latest

# Apptainer
apptainer pull gemc-binder-tutorials.sif docker://ghcr.io/gemc/binder-tutorials:latest
apptainer exec gemc-binder-tutorials.sif jupyter lab --ip=0.0.0.0 --no-browser
```

<br/><br/>

## 交互式 3D 展示

使用鼠标滚轮旋转相机，或在每个缩略图内使用方向键。点击标题链接查看
文档。

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

GEMC 的 Python API `pygemc` 提供几何与材料数据库构建器、`pyvista` 几何可视化、
`gemc-system-template` 和 `gemc-analyzer`。该分析器可以读取 GEMC 的 CSV 和 ROOT 输出，并根据
所选变量绘制直方图。

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

下面的代码片段定义了靶下游的灵敏通量平面。每当一条生成的径迹穿过
该几何体时，GEMC 都会记录一次 %%flux%% 命中。

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

## 数据库

探测器定义存储在数据库中。典型的工作流程只有一个需要用户编写的步骤：

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
> 运行模拟不需要事先了解 C++ 或 Geant4。
> 具备基础的 Python 知识有助于组织复杂的配置。
> 用户还可以**定义自己的硬件仿真例程**。在这种情况下，具备基础的 C++ 知识
> 有助于实现复杂的数字化处理。

<br/><br/>

## 几何变体

同一个探测器可以在多个实验中复用，并进行组件位置调整、
材料更换或几何体增删等配置更改。
GEMC 通过 %%variation%% 字符串和/或 %%run%% 编号支持这些几何版本，以适应不同的
模拟
配置。

{% include figure.html
src="/assets/images/clas12v.gif"
alt="Python API example"
caption="The animation shows two variations of the CLAS12 Central Detector.
The geometries are identical except for the target position. Users select them
with a variation string or run number in the configuration file or command-line options."
%}

<br/><br/>

## 最新动态

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
  <a href="{{ "/news/" | relative_url }}">全部动态</a>
  ·
  <a href="{{ "/feed.xml" | relative_url }}">RSS 订阅</a>
</p>

<br/><br/>

## 持续集成

GitHub CI 在多个平台以及 ARM64 和 AMD64 两种
架构上构建、测试 GEMC，并将其部署为 Docker 镜像。

**gemc**

{:.zebra}

| 测试      | [![测试][test-badge]][test]                                  |
| Sanitizer 检查  | [![Sanitizer 检查][Sanitize-badge]][Sanitize]                      |
| CodeQL | [![CodeQL][CodeQL-badge]][CodeQL]                            |
| 镜像部署 | [![部署][deploy-badge]][deploy]                            |
| 二进制 tar 包 | [![二进制 tar 包][Binary-Tarballs-badge]][Binary-Tarballs] |
| macOS tar 包 | [![macOS tar 包][macOS-Tarball-badge]][macOS-Tarball]       |
| 每夜发布 | [![每夜发布][Nightly-badge]][Nightly]                         |
| 主页 | [![网站][Site-badge]][Site]                                  |
| Docker 拉取次数 | [![Docker 拉取次数][DockerHub-badge]][DockerHub]                |
| Doxygen | [![文档][Docs-badge]][Docs]                                  |
| 发布版 tar 包 | [![发布版 tar 包][Release-Tarballs-badge]][Release-Tarballs] |

**pygemc**

{:.zebra}

| 每夜开发版发布 | [![每夜开发版发布][PyGemc-Nightly-badge]][PyGemc-Nightly]   |
| 发布到 PyPI     | [![发布到 PyPI][PyGemc-Publish-badge]][PyGemc-Publish]          |
| 测试 | [![pygemc 测试][PyGemc-Tests-badge]][PyGemc-Tests]               |
| PyPI | [![pygemc PyPI][PyPI-badge]][PyPI]                               |

<br/><br/>

## 参考文献

如果使用 GEMC，请务必引用以下论文：

> M. Ungaro and the CLAS Collaboration, "The CLAS12 Geant4 simulation," *Nuclear Instruments and
> Methods in Physics Research Section A: Accelerators, Spectrometers, Detectors and Associated
> Equipment* **959**, 163422 (2020). <https://doi.org/10.1016/j.nima.2020.163422>

BibTeX：

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

Bibitem：

```latex
\bibitem{UNGARO2020163422}
M. Ungaro and the CLAS Collaboration,
\newblock The CLAS12 Geant4 simulation.
\newblock Nuclear Instruments and Methods in Physics Research Section A \textbf{959}, 163422 (2020).
\newblock \doi{10.1016/j.nima.2020.163422}
```

<br/><br/>

## 源代码与许可证

[GEMC 源代码](https://github.com/gemc/src) 采用
[Apache 许可证 2.0 版](/home/license/)；署名信息及
第三方致谢请参见 [NOTICE](/home/license/#notice)。该软件还依赖采用各自许可证的第三方组件，
包括 Geant4、CLHEP、Qt、ROOT、SQLite 和 Assimp。

<br/><br/>

<hr/>
