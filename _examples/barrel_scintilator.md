---
layout: default
title: "Sensitive Scintillator Array"
---
{% include directory.html data=site.data.examples columns=5 section_breaks=4 %}

# Sensitive Scintillator Array
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

This legacy page describes a scintillator-bar array with `flux` digitization.
The current `gemc/src/examples` tree does not include this example, so the commands below should be treated as historical notes until the source example is restored.

<br/>

## Quickstart

No current quickstart is available in `gemc/src/examples` for this page.

<br/>

## Geometry

The legacy setup is an array of trapezoidal scintillator bars in a cylindrical configuration.
The bars were arranged to maximize active surface area around the beam line.

![scint_array]{:width="70%"}

<br/>

Another legacy rendering shows 1000 events with hits in the sensitive bars:

![scint_hits]{:width="70%"}

<br/>

## Physics List

No current YAML steering file is available in `gemc/src/examples` for this page, so the physics list cannot be verified from source.

<br/>

## Generator

No current YAML steering file is available in `gemc/src/examples` for this page, so the generated particles cannot be verified from source.

<br/>

## Digitization

The legacy page used `flux` digitization for the scintillator bars.
The output contained `trueInfo_flux` and `digitized_flux` ROOT trees.

<br/>

## Usage

The previous page referenced `scintillator_array.py` and `scintillator_array.jcard`, but those files are not present in the current `gemc/src/examples` tree.
Restore or update the source example before using this page as runnable documentation.

<br/>

## Output

The legacy ROOT output contained:

- `header`, the GEMC ROOT event header
- `trueInfo_flux`, the true-information tree
- `digitized_flux`, the digitized-data tree

Example ROOT expressions from the legacy page were:

```cpp
digitized_flux->Draw("eTot:bar_id>>(37, 0, 38, 100, 20.0, 20.6)", "eTot>20", "colz")
trueInfo_flux->Draw("avgy:avgx>>(400, -400, 400, 400, -400, 400)", "", "colz")
```

![eTot_vs_bar_id]{:width="70%"}

![avgy_vs_avgx]{:width="70%"}

<br/>

## Plotting with the GEMC Analyzer

When this example is restored and configured to write CSV or ROOT output with `gstreamer`, run GEMC with 1,000 events first:

```shell
gemc scintillator_array.yaml -n=1000
```

Plot the digitized energy deposited:

```shell
python3 -m analyzer scintillator_array_t0_digitized.csv eTot --kind csv
```

![scintillator array energy deposited plot](/home/assets/images/examples/scintillator_array/analyzer_eTot.png){:width="70%"}

Plot the true hit-position quantity:

```shell
python3 -m analyzer scintillator_array_t0_true_info.csv avgx --kind csv --data true_info
```

![scintillator array true x-position plot](/home/assets/images/examples/scintillator_array/analyzer_avgx.png){:width="70%"}

For ROOT output, select the detector tree name:

```shell
python3 -m analyzer scintillator_array_t0.root eTot --kind root --detector flux
```

![scintillator array ROOT energy deposited plot](/home/assets/images/examples/scintillator_array/analyzer_root_eTot.png){:width="70%"}

[scint_array]: /home/assets/images/examples/scintillator_array/geometry.png
[scint_hits]: /home/assets/images/examples/scintillator_array/geometry_and_hits.png
[eTot_vs_bar_id]: /home/assets/images/examples/scintillator_array/eTot_vs_bar_id.png
[avgy_vs_avgx]: /home/assets/images/examples/scintillator_array/avgy_vs_avgx.png
