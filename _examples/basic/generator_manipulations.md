---
layout: default
title: "Generator manipulations"
---

# Generator manipulations
<hr style="height:4px;border:0;background:#4a90e2;">

**Upcoming in the next release.** Use a current development build of `gemc` for these examples.
See the [installation guide]({{ site.baseurl }}/installation/) for the executable and Python environment.

Eleven independent steering cards isolate vertex smearing, fixed angles, and angular sampling.
Each generates a 1 GeV geantino inside the same small tube target to represent a target event.
The plots below come from fresh simulations:
5,000 throws per card, checked against the generated-particle records before plotting. Every case also includes
its own GEMC view of 100 events.

{% assign source = "https://github.com/gemc/src/tree/main/examples/basic/generator_manipulations" %}
{% assign source_files = source | replace: "/tree/", "/blob/" %}
{% assign cases = site.data.generator_cases %}

[Browse the source example]({{ source }}), including the geometry, complete YAML cards, and automated checks.

## Quickstart

Copy the example from a development installation and generate its ASCII geometry:

```shell
cp -r "$GEMC_HOME/examples/basic/generator_manipulations" .
cd generator_manipulations
python generator_manipulations.py -f ascii
gemc uniform_z.yaml -gui
```

Generate events with the GUI beam-on control, then open the Analyzer. The XY smearing cards prepare one 2D
Y-versus-X plot; the remaining cards prepare four plots. All cards enable accumulation across beam-on calls. Qt
Charts is required for the GUI Analyzer.
Run any card without %%-gui%% to produce a seeded 5,000-event CSV sample instead:

```shell
gemc uniform_z.yaml
```

Each card has its own output prefix. For example, %%uniform_z%% produces the generated and true-information
CSV streams used to check that the target records exactly the vertices that were thrown.

## Geometry and recorded quantities

The vacuum world contains one liquid hydrogen tube, centered at the origin, with radius 25 mm and full length
40 mm, displayed at 20% opacity to keep trajectories visible through it.
Its %%flux%% sensitivity records particles originating inside it. Smearing represents the production
vertices of target events.
Geantinos do not scatter or create secondary particles; %%recordZeroEdep: true%% keeps their target hits.
This gives one hit per thrown particle for these configurations.

{% include figure.html
src="assets/images/examples/generator_manipulations/gemc_view.png"
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

Vertex plots use %%vx%%, %%vy%%, and %%vz%% from the target's true information, in mm. These are the original
track vertices. The fields %%avgx%%, %%avgy%%, and %%avgz%% instead describe the positions inside the target.
Angular plots use the preserved momentum components %%px%%, %%py%%, and %%pz%%, in MeV/c.

The website figures use the `pygemc` Analyzer plotting functions with the variables and layout defined in each
card's %%ganalysis%% block. They are offline plots of the same data fields shown in the GUI.

## Vertex cases

The smearing cards use the displaced center (2, -3, 0) mm to show that random offsets are added to the
nominal position. Z smearing uses theta = 90 degrees; XY and sphere smearing use theta = 45 degrees.
All vertex-smearing cards use phi = 90 degrees.
Uniform and Gaussian XY vary both transverse coordinates independently and display 2D Y-versus-X
maps. Separate uniform-Z and Gaussian-Z cards isolate the longitudinal spread.

- %%uniform%%: each nonzero %%delta_vx%%, %%delta_vy%%, or %%delta_vz%% is a half-width about its center.
- %%gaussian%%: each delta is a standard deviation. The one-dimensional plot windows show five sigma;
  these display limits do not truncate generation. Gaussian Z uses sigma = 3 mm, so the target half-length
  contains more than six sigma. Gaussian tails are unbounded; the seeded samples are checked for containment.
- %%sphere%%: points are uniform throughout a sphere of radius
  %%sqrt(delta_vx^2 + delta_vy^2 + delta_vz^2)%%. Spreads (1, 2, 2) mm give radius 3 mm, rather than
  three ellipsoid axes. The coordinate projections are parabolic and the radial CDF is %%(r/R)^3%%.

{% assign vertex_cases = cases | where: "group", "Vertices" %}
{% for case in vertex_cases %}
### {{ case.title }}

{{ case.expected }}

[Complete {{ case.name }}.yaml]({{ source_files }}/{{ case.name }}.yaml)

<details markdown="1">
<summary>Particle settings</summary>

{% highlight yaml %}{{ case.particle }}{% endhighlight %}

</details>

{% capture event_caption %}GEMC: {{ case.view_events }} events for {{ case.title }}.{% endcapture %}
{% include figure.html src=case.event_image alt=case.title caption=event_caption link=case.event_image %}
{% include figure.html src=case.image alt=case.title caption=case.expected link=case.image %}
{% endfor %}

## Angular cases

The angular cards fix the vertex at the target center, (0, 0, 0) mm. %%randomThetaModel%% supports %%uniform%%,
%%gaussian%%, and %%cosine%%.
For %%uniform%%, %%delta_theta%% is a half-width; for %%gaussian%%, it is a standard deviation.
The %%cosine%% model is uniform in cos(theta) within theta +/- delta_theta, giving a density proportional to
sin(theta), restricted to [0, 180] degrees.
The theta-smearing cards use %%delta_theta: 20*deg%% and nominal theta = 2 degrees. Uniform sampling spans
[-18, 22] degrees; Gaussian sampling has mean 2 degrees and sigma 20 degrees. Negative theta reverses the
transverse momentum: the reconstructed polar angle is nonnegative, with azimuth shifted by 180 degrees.
Cosine sampling spans [0, 22] degrees because its draws are restricted to physical polar angles.
Phi always uses uniform sampling with half-width %%delta_phi%%; there is no %%randomPhiModel%%.

For momentum p, the expected components are:

```text
px = p sin(theta) cos(phi)
py = p sin(theta) sin(phi)
pz = p cos(theta)
```

The fixed theta and phi card sets both angles to 3 and 45 degrees, respectively. Gaussian and cosine theta
show %%px%% vertically against %%pz%% horizontally in their 2D plots. The cosine-theta case also gives a flat
%%pz%% distribution. Fixed theta with a phi spread traces an arc
in the %%px%%/%%py%% projection. The wraparound case crosses 360 degrees without a discontinuity in momentum.
Generated-bank angles are stored in radians; the steering cards use explicit degrees.

{% assign angular_cases = cases | where: "group", "Angles" %}
{% for case in angular_cases %}
### {{ case.title }}

{{ case.expected }}

[Complete {{ case.name }}.yaml]({{ source_files }}/{{ case.name }}.yaml)

<details markdown="1">
<summary>Particle settings</summary>

{% highlight yaml %}{{ case.particle }}{% endhighlight %}

</details>

{% capture event_caption %}GEMC: {{ case.view_events }} events for {{ case.title }}.{% endcapture %}
{% include figure.html src=case.event_image alt=case.title caption=event_caption link=case.event_image %}
{% include figure.html src=case.image alt=case.title caption=case.expected link=case.image %}
{% endfor %}

## Verify and reproduce

From a configured GEMC source tree, run all 11 checks:

```shell
meson test -C build --suite generator_manipulations --print-errorlogs
```

The checks require every vertex inside the target and one target hit per throw. They match event IDs and
vertices, compare momentum components, reconstruct theta and phi modulo 360 degrees, and test the expected
probability distributions.
The XY checks also verify that the transverse samples are uncorrelated. The tests generate fresh geometry and
output in temporary directories, so each case also works in isolation.

To regenerate this page's images and particle settings from the website repository:

```shell
python3 scripts/generate_example_assets.py generator_manipulations
```

The website's [asset guide]({{ site.baseurl }}/assets/assets.md) documents the required local environments.
See also the [internal generator guide]({{ site.baseurl }}/documentation/generator/internal).
