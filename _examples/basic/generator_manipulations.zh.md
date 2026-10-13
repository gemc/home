---
layout: default
title: "Generator manipulations"
permalink: /examples/basic/generator_manipulations.html
lang: zh
human_reviewed: false
---

# 生成器操作
<hr style="height:4px;border:0;background:#4a90e2;">

这些示例需使用 GEMC 0.5 或更高版本。
有关可执行文件和 Python 环境，请参阅[安装指南]({{ site.baseurl }}/installation/)。

十一张相互独立的控制卡分别演示顶点展宽、固定角度和角度采样。
每张卡都在同一个小型管状靶内生成一个 1 GeV 的 geantino，用以表示一次靶事件。
下面的图表来自新运行的模拟：
每张卡采样 5,000 次，绘图前均与生成粒子记录进行核对。每个用例还包含
对应的 100 个事件的 GEMC 视图。

{% assign source = "https://github.com/gemc/src/tree/main/examples/basic/generator_manipulations" %}
{% assign source_files = source | replace: "/tree/", "/blob/" %}
{% assign cases = site.data.generator_cases %}

[浏览示例源码]({{ source }})，其中包含几何结构、完整的 YAML 控制卡和自动化检查。

## 快速开始

从 GEMC 安装目录中复制该示例，并生成其 ASCII 几何结构：

```shell
cp -r "$GEMC_HOME/examples/basic/generator_manipulations" .
cd generator_manipulations
python generator_manipulations.py -f ascii
gemc uniform_z.yaml -gui
```

使用 GUI 的 beam-on 控件生成事件，然后打开 Analyzer。XY 展宽控制卡会配置一张二维图，
以 Y 为纵轴、X 为横轴。Z 展宽和固定角度控制卡会配置三个直方图；其他控制卡则配置四张图。
所有控制卡都启用跨 beam-on 调用的数据累积功能。GUI Analyzer 需要 Qt Charts。
运行任意控制卡时，省略 %%-gui%% 即可改为生成一个使用固定随机种子的、包含 5,000 个事件的 CSV 样本：

```shell
gemc uniform_z.yaml
```

每张控制卡都有各自的输出前缀。例如，%%uniform_z%% 会产生生成粒子信息和真实信息
CSV 数据流，用于核对靶记录的顶点是否与采样生成的顶点完全一致。

## 几何结构与记录量

真空世界体中包含一个液氢管，以原点为中心，半径为 25 mm，全长为
40 mm，以 20% 的不透明度显示，以便透过它看到轨迹。
其 %%flux%% 灵敏探测设置会记录在靶内产生的粒子。展宽用于模拟靶事件的产生
顶点。
geantino 不发生散射，也不产生次级粒子；%%recordZeroEdep: true%% 会保留它们在靶中的命中记录。
在这些配置下，每个采样生成的粒子都会产生一个命中记录。

{% include figure.html
src="/assets/images/examples/generator_manipulations/gemc_view.png"
alt="Geantinos originating at smeared vertices inside the transparent cylindrical target"
caption="The shared tube target with 100 events from the uniform-Z card, rendered by GEMC."
%}

{% assign vtk = "/assets/images/examples/generator_manipulations/generator_manipulations.vtksz" %}
<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}{{ vtk }}"
  title="Interactive view of the tube target"
  width="100%" height="420" loading="lazy"
  style="border:1px solid #d0d7de;">
</iframe>

顶点图使用靶真实信息中的 %%vx%%、%%vy%% 和 %%vz%%，单位为 mm。这些是原始的
径迹顶点。%%avgx%%、%%avgy%% 和 %%avgz%% 字段则描述粒子在靶内的位置。
角度图使用保留下来的动量分量 %%px%%、%%py%% 和 %%pz%%，单位为 MeV/c。

网站图表使用 `pygemc` Analyzer 的绘图函数，变量和布局在每张控制卡的
%%ganalysis%% 块中定义。这些离线图使用的数据字段与 GUI 中显示的相同。网站的
Z 展宽图将 X 和 Y 直方图放在上方，下方的 Z 直方图横跨两列；固定角度图则将
三个直方图排成一行。GUI 使用单面板或四绘图区布局。

## 顶点用例

展宽控制卡使用偏移后的中心 (2, -3, 0) mm，以展示随机偏移量如何叠加到
标称位置上。Z 展宽使用 theta = 90 度；XY 和球体展宽使用 theta = 45 度。
所有顶点展宽控制卡都使用 phi = 90 度。
均匀 XY 展宽和高斯 XY 展宽分别独立改变两个横向坐标，并显示以 Y 为纵轴、X 为横轴的二维
分布图。单独的均匀 Z 展宽和高斯 Z 展宽控制卡用于独立展示纵向展宽。

- %%uniform%%：每个非零的 %%delta_vx%%、%%delta_vy%% 或 %%delta_vz%% 都是相对于其中心的半宽。
- %%gaussian%%：每个 delta 都是标准差。一维绘图窗口显示五个标准差的范围；
  这些显示范围不会截断生成分布。高斯 Z 展宽使用标准差 sigma = 3 mm，因此靶的半长
  超过六个标准差。高斯分布的尾部无界；会检查使用固定随机种子生成的样本是否全部位于靶内。
- %%sphere%%：点在半径为
  %%sqrt(delta_vx^2 + delta_vy^2 + delta_vz^2)%% 的球体内均匀分布。展宽参数 (1, 2, 2) mm 对应半径 3 mm，而非
  椭球的三个半轴。坐标投影呈抛物线形，径向累积分布函数（CDF）为 %%(r/R)^3%%。

{% assign vertex_cases = cases | where: "group", "Vertices" %}
{% for case in vertex_cases %}
### {{ case.title }}

{{ case.expected }}

[完整的 {{ case.name }}.yaml]({{ source_files }}/{{ case.name }}.yaml)

<details markdown="1">
<summary>粒子设置</summary>

{% highlight yaml %}{{ case.particle }}{% endhighlight %}

</details>

{% capture event_caption %}GEMC：{{ case.title }} 的 {{ case.view_events }} 个事件。{% endcapture %}
{% include figure.html src=case.event_image alt=case.title caption=event_caption link=case.event_image %}
{% include figure.html src=case.image alt=case.title caption=case.expected link=case.image %}
{% endfor %}

## 角度用例

角度控制卡将顶点固定在靶中心 (0, 0, 0) mm。%%randomThetaModel%% 支持 %%uniform%%、
%%gaussian%% 和 %%cosine%%。
对于 %%uniform%%，%%delta_theta%% 是半宽；对于 %%gaussian%%，它是标准差。
%%cosine%% 模型在 theta +/- delta_theta 范围内对 cos(theta) 进行均匀采样，因此 theta 的概率密度正比于
sin(theta)，且角度范围限制在 [0, 180] 度内。
theta 展宽控制卡使用 %%delta_theta: 20*deg%% 和标称 theta = 2 度。均匀采样范围为
[-18, 22] 度；高斯采样的均值为 2 度，标准差为 20 度。负 theta 会反转
横向动量：重建出的极角为非负值，方位角偏移 180 度。
余弦采样范围为 [0, 22] 度，因为采样值被限制在物理极角范围内。
phi 始终采用均匀采样，半宽为 %%delta_phi%%；没有 %%randomPhiModel%%。

对于动量 p，预期的分量为：

```text
px = p sin(theta) cos(phi)
py = p sin(theta) sin(phi)
pz = p cos(theta)
```

固定 theta 和 phi 的控制卡将两个角度分别设为 3 度和 45 度，并仅显示三个
动量直方图。均匀、高斯和余弦 theta 采样用例的二维图均以 %%px%% 为纵轴、%%pz%% 为横轴。
余弦 theta 采样用例还会得到均匀的
%%pz%% 分布。固定 theta 并对 phi 进行展宽时，会在
%%px%%/%%py%% 投影中描出一段圆弧。角度回绕用例跨越 360 度时，动量仍保持连续。
生成粒子数据组中的角度以弧度存储；控制卡则显式使用度作为单位。

{% assign angular_cases = cases | where: "group", "Angles" %}
{% for case in angular_cases %}
### {{ case.title }}

{{ case.expected }}

[完整的 {{ case.name }}.yaml]({{ source_files }}/{{ case.name }}.yaml)

<details markdown="1">
<summary>粒子设置</summary>

{% highlight yaml %}{{ case.particle }}{% endhighlight %}

</details>

{% capture event_caption %}GEMC：{{ case.title }} 的 {{ case.view_events }} 个事件。{% endcapture %}
{% include figure.html src=case.event_image alt=case.title caption=event_caption link=case.event_image %}
{% include figure.html src=case.image alt=case.title caption=case.expected link=case.image %}
{% endfor %}

## 验证与复现

在已配置好的 GEMC 源码树中，运行全部 11 项检查：

```shell
meson test -C build --suite generator_manipulations --print-errorlogs
```

这些检查要求每个顶点都位于靶内，且每次采样生成的粒子在靶中恰好产生一个命中记录。检查会匹配事件 ID 和
顶点，比较动量分量，重建 theta 和 phi 并按 360 度取模进行比较，还会检验预期的
概率分布。
XY 检查还会验证横向采样值之间不相关。测试会在临时目录中生成新的几何结构和
输出，因此每个用例也都能独立运行。

要从网站仓库重新生成本页的图像和粒子设置：

```shell
python3 scripts/generate_example_assets.py generator_manipulations
```

网站的[资源指南]({{ site.baseurl }}/assets/assets.md)说明了所需的本地环境。
另请参阅[内部生成器指南]({{ site.baseurl }}/documentation/generator/internal)。
