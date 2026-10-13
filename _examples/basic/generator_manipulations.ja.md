---
layout: default
title: "Generator manipulations"
permalink: /examples/basic/generator_manipulations.html
lang: ja
human_reviewed: false
---

# ジェネレータの操作
<hr style="height:4px;border:0;background:#4a90e2;">

これらの例では GEMC 0.5 以降を使用してください。
実行ファイルと Python 環境については、[インストールガイド]({{ site.baseurl }}/installation/)を参照してください。

11 個の独立したステアリングカードで、頂点スメアリング、固定角度、角度サンプリングを個別に扱います。
各カードは、同じ小さなチューブ状ターゲット内に 1 GeV の geantino を生成し、ターゲットイベントを表現します。
以下のプロットは、新たに実行したシミュレーションから得られたものです。
カードごとに 5,000 回の生成を行い、プロット前に生成粒子の記録と照合しています。各ケースには、
100 イベントを表示した GEMC ビューも含まれています。

{% assign source = "https://github.com/gemc/src/tree/main/examples/basic/generator_manipulations" %}
{% assign source_files = source | replace: "/tree/", "/blob/" %}
{% assign cases = site.data.generator_cases %}

ジオメトリ、完全な YAML カード、自動チェックを含む[サンプルのソース]({{ source }})を参照できます。

## クイックスタート

GEMC のインストール先からサンプルをコピーし、ASCII ジオメトリを生成します。

```shell
cp -r "$GEMC_HOME/examples/basic/generator_manipulations" .
cd generator_manipulations
python generator_manipulations.py -f ascii
gemc uniform_z.yaml -gui
```

GUI の beam-on コントロールでイベントを生成し、Analyzer を開きます。XY スメアリングカードでは、
Y 対 X の 2D プロットを 1 つ用意します。Z スメアリングと固定角度のカードではヒストグラムを 3 つ、
その他のカードではプロットを 4 つ用意します。
すべてのカードで、複数の beam-on 呼び出しにわたる蓄積が有効になっています。GUI Analyzer には Qt Charts が必要です。
%%-gui%% なしで任意のカードを実行すると、代わりに乱数シードを設定した 5,000 イベントの CSV サンプルが生成されます。

```shell
gemc uniform_z.yaml
```

各カードには固有の出力プレフィックスがあります。たとえば %%uniform_z%% は、生成時の頂点がターゲットに
正確に記録されていることを確認するための、生成情報と真値情報の CSV ストリームを出力します。

## ジオメトリと記録される物理量

真空のワールドには、原点を中心とする半径 25 mm、全長 40 mm の液体水素チューブが 1 つ配置されています。
内部を通る軌跡が見えるように、不透明度 20% で表示されます。
%%flux%% の感度設定により、内部で発生した粒子が記録されます。スメアリングは、ターゲットイベントの
生成頂点を表現します。
geantino は散乱せず、二次粒子も生成しません。%%recordZeroEdep: true%% により、ターゲット内でのヒットが保持されます。
これらの設定では、生成粒子 1 個につき 1 ヒットが得られます。

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

頂点プロットでは、ターゲットの真値情報に含まれる %%vx%%、%%vy%%、%%vz%% を mm 単位で使用します。
これらは元のトラックの生成頂点です。一方、%%avgx%%、%%avgy%%、%%avgz%% はターゲット内部の位置を表します。
角度プロットでは、保持された運動量成分 %%px%%、%%py%%、%%pz%% を MeV/c 単位で使用します。

ウェブサイトの図は、各カードの %%ganalysis%% ブロックで定義された変数とレイアウトを用いて、
`pygemc` Analyzer のプロット関数で作成されています。GUI に表示されるものと同じデータフィールドを
オフラインでプロットしたものです。ウェブサイトの Z スメアリングの図では、X と Y の下に、
2 列にまたがる Z ヒストグラムを配置します。固定角度の図では、3 つのヒストグラムを横 1 列に配置します。
GUI では、単一パネルまたは 4 枠のレイアウトを使用します。

## 頂点のケース

スメアリングカードでは、中心を (2, -3, 0) mm にずらし、公称位置にランダムなオフセットが
加算されることを示します。Z スメアリングでは theta = 90 度、XY および球内のスメアリングでは
theta = 45 度を使用します。
すべての頂点スメアリングカードで phi = 90 度を使用します。
一様分布およびガウス分布による XY スメアリングでは、2 つの横方向座標を独立に変化させ、
Y 対 X の 2D マップを表示します。別々の uniform-Z カードと Gaussian-Z カードで、縦方向の広がりを個別に扱います。

- %%uniform%%: 非ゼロの各 %%delta_vx%%、%%delta_vy%%、%%delta_vz%% は、中心からの分布の半幅です。
- %%gaussian%%: 各 delta は標準偏差です。1 次元プロットの表示範囲は 5 シグマです。
  この表示範囲によって生成範囲が制限されることはありません。ガウス分布による Z スメアリングでは sigma = 3 mm を使用するため、
  ターゲットの半長は 6 シグマを超えます。ガウス分布の裾は無限に広がるため、乱数シードを設定したサンプルが
  ターゲット内に収まることを確認します。
- %%sphere%%: 点は、半径
  %%sqrt(delta_vx^2 + delta_vy^2 + delta_vz^2)%% の球の内部全体に一様に分布します。広がり (1, 2, 2) mm は、
  楕円体の 3 つの軸を指定するのではなく、半径 3 mm を与えます。各座標軸への射影分布は放物線状で、動径の累積分布関数（CDF）は %%(r/R)^3%% です。

{% assign vertex_cases = cases | where: "group", "Vertices" %}
{% for case in vertex_cases %}
### {{ case.title }}

{{ case.expected }}

[{{ case.name }}.yaml の全内容]({{ source_files }}/{{ case.name }}.yaml)

<details markdown="1">
<summary>粒子設定</summary>

{% highlight yaml %}{{ case.particle }}{% endhighlight %}

</details>

{% capture event_caption %}GEMC: {{ case.view_events }} イベント（{{ case.title }}）。{% endcapture %}
{% include figure.html src=case.event_image alt=case.title caption=event_caption link=case.event_image %}
{% include figure.html src=case.image alt=case.title caption=case.expected link=case.image %}
{% endfor %}

## 角度のケース

角度カードでは、頂点をターゲット中心 (0, 0, 0) mm に固定します。%%randomThetaModel%% は %%uniform%%、
%%gaussian%%、%%cosine%% をサポートします。
%%uniform%% では %%delta_theta%% は分布の半幅、%%gaussian%% では標準偏差です。
%%cosine%% モデルでは、theta +/- delta_theta の範囲を [0, 180] 度に制限し、その範囲内で cos(theta) を
一様にサンプリングするため、theta の確率密度は sin(theta) に比例します。
theta スメアリングカードでは %%delta_theta: 20*deg%% と公称 theta = 2 度を使用します。一様サンプリングの範囲は
[-18, 22] 度で、ガウスサンプリングは平均 2 度、sigma 20 度です。負の theta は横方向の運動量を反転させます。
再構成された極角は非負となり、方位角は 180 度ずれます。
cosine サンプリングでは、サンプリング範囲が物理的な極角に制限されるため、範囲は [0, 22] 度になります。
phi には常に半幅 %%delta_phi%% の一様サンプリングを使用します。%%randomPhiModel%% はありません。

運動量 p に対して、期待される成分は次のとおりです。

```text
px = p sin(theta) cos(phi)
py = p sin(theta) sin(phi)
pz = p cos(theta)
```

theta と phi を固定するカードでは、それぞれの角度を 3 度と 45 度に設定し、3 つの運動量ヒストグラムのみを
表示します。一様分布、ガウス分布、cosine モデルによる theta サンプリングでは、2D プロットの縦軸に %%px%%、
横軸に %%pz%% を表示します。cosine-theta のケースでは、
%%pz%% 分布も一様になります。theta を固定して phi に広がりを持たせると、
%%px%%/%%py%% 平面への射影は円弧を描きます。ラップアラウンドのケースでは、運動量に不連続を生じることなく 360 度をまたぎます。
生成粒子バンクの角度はラジアンで保存されます。ステアリングカードでは、単位を明示して度を使用します。

{% assign angular_cases = cases | where: "group", "Angles" %}
{% for case in angular_cases %}
### {{ case.title }}

{{ case.expected }}

[{{ case.name }}.yaml の全内容]({{ source_files }}/{{ case.name }}.yaml)

<details markdown="1">
<summary>粒子設定</summary>

{% highlight yaml %}{{ case.particle }}{% endhighlight %}

</details>

{% capture event_caption %}GEMC: {{ case.view_events }} イベント（{{ case.title }}）。{% endcapture %}
{% include figure.html src=case.event_image alt=case.title caption=event_caption link=case.event_image %}
{% include figure.html src=case.image alt=case.title caption=case.expected link=case.image %}
{% endfor %}

## 検証と再現

設定済みの GEMC ソースツリーから、11 個すべてのチェックを実行します。

```shell
meson test -C build --suite generator_manipulations --print-errorlogs
```

これらのチェックでは、すべての頂点がターゲット内にあり、生成 1 回につきターゲットヒットが 1 つあることを
確認します。イベント ID と頂点を照合し、運動量成分を比較し、theta と phi を 360 度を法として再構成し、
期待される確率分布を検定します。
XY のチェックでは、横方向のサンプル間に相関がないことも確認します。テストは一時ディレクトリ内に
新しいジオメトリと出力を生成するため、各ケースは単独でも動作します。

このページの画像と粒子設定をウェブサイトリポジトリから再生成するには、次を実行します。

```shell
python3 scripts/generate_example_assets.py generator_manipulations
```

必要なローカル環境については、ウェブサイトの[アセットガイド]({{ site.baseurl }}/assets/assets.md)に記載されています。
[内部ジェネレータガイド]({{ site.baseurl }}/documentation/generator/internal)も参照してください。
