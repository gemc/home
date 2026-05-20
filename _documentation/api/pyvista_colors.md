---
layout: default
title: "PyVista Color Reference"
---
{% include directory.html data=site.data.documentation columns=4 section_breaks=3 %}

# PyVista Color Reference
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

Colors are specified as CSS/HTML color names or as 6-digit hex strings (without `#`).
A metallic sheen can be added with the prefix `"metallic, <color>"`.

```python
volume.color = "steelblue"          # named color
volume.color = "4682B4"             # same as steelblue, hex form
volume.color = "metallic, steelblue"  # steelblue with metallic sheen
```

The default color (when none is specified) is `lightslategray` (`778899`).

<br/>

## Basics

| Name | Hex | &nbsp; | Name | Hex | &nbsp; | Name | Hex |
|------|-----|--------|------|-----|--------|------|-----|
| `black` | `000000` | <span style="display:inline-block;width:20px;height:14px;background:#000000;border:1px solid #ccc"></span> | `white` | `FFFFFF` | <span style="display:inline-block;width:20px;height:14px;background:#FFFFFF;border:1px solid #ccc"></span> | `red` | `FF0000` | <span style="display:inline-block;width:20px;height:14px;background:#FF0000;border:1px solid #ccc"></span> |
| `green` | `008000` | <span style="display:inline-block;width:20px;height:14px;background:#008000;border:1px solid #ccc"></span> | `blue` | `0000FF` | <span style="display:inline-block;width:20px;height:14px;background:#0000FF;border:1px solid #ccc"></span> | `yellow` | `FFFF00` | <span style="display:inline-block;width:20px;height:14px;background:#FFFF00;border:1px solid #ccc"></span> |
| `cyan` | `00FFFF` | <span style="display:inline-block;width:20px;height:14px;background:#00FFFF;border:1px solid #ccc"></span> | `magenta` | `FF00FF` | <span style="display:inline-block;width:20px;height:14px;background:#FF00FF;border:1px solid #ccc"></span> | `gray` | `808080` | <span style="display:inline-block;width:20px;height:14px;background:#808080;border:1px solid #ccc"></span> |
| `silver` | `C0C0C0` | <span style="display:inline-block;width:20px;height:14px;background:#C0C0C0;border:1px solid #ccc"></span> | `maroon` | `800000` | <span style="display:inline-block;width:20px;height:14px;background:#800000;border:1px solid #ccc"></span> | `olive` | `808000` | <span style="display:inline-block;width:20px;height:14px;background:#808000;border:1px solid #ccc"></span> |
| `navy` | `000080` | <span style="display:inline-block;width:20px;height:14px;background:#000080;border:1px solid #ccc"></span> | `teal` | `008080` | <span style="display:inline-block;width:20px;height:14px;background:#008080;border:1px solid #ccc"></span> | `purple` | `800080` | <span style="display:inline-block;width:20px;height:14px;background:#800080;border:1px solid #ccc"></span> |

## Grays

| Name | Hex | &nbsp; | Name | Hex | &nbsp; | Name | Hex |
|------|-----|--------|------|-----|--------|------|-----|
| `whitesmoke` | `F5F5F5` | <span style="display:inline-block;width:20px;height:14px;background:#F5F5F5;border:1px solid #ccc"></span> | `gainsboro` | `DCDCDC` | <span style="display:inline-block;width:20px;height:14px;background:#DCDCDC;border:1px solid #ccc"></span> | `lightgray` | `D3D3D3` | <span style="display:inline-block;width:20px;height:14px;background:#D3D3D3;border:1px solid #ccc"></span> |
| `darkgray` | `A9A9A9` | <span style="display:inline-block;width:20px;height:14px;background:#A9A9A9;border:1px solid #ccc"></span> | `slategray` | `708090` | <span style="display:inline-block;width:20px;height:14px;background:#708090;border:1px solid #ccc"></span> | `dimgray` | `696969` | <span style="display:inline-block;width:20px;height:14px;background:#696969;border:1px solid #ccc"></span> |
| `lightslategray` | `778899` | <span style="display:inline-block;width:20px;height:14px;background:#778899;border:1px solid #ccc"></span> | `darkslategray` | `2F4F4F` | <span style="display:inline-block;width:20px;height:14px;background:#2F4F4F;border:1px solid #ccc"></span> | | | |

## Blues

| Name | Hex | &nbsp; | Name | Hex | &nbsp; | Name | Hex |
|------|-----|--------|------|-----|--------|------|-----|
| `aliceblue` | `F0F8FF` | <span style="display:inline-block;width:20px;height:14px;background:#F0F8FF;border:1px solid #ccc"></span> | `ghostwhite` | `F8F8FF` | <span style="display:inline-block;width:20px;height:14px;background:#F8F8FF;border:1px solid #ccc"></span> | `lavender` | `E6E6FA` | <span style="display:inline-block;width:20px;height:14px;background:#E6E6FA;border:1px solid #ccc"></span> |
| `powderblue` | `B0E0E6` | <span style="display:inline-block;width:20px;height:14px;background:#B0E0E6;border:1px solid #ccc"></span> | `lightblue` | `ADD8E6` | <span style="display:inline-block;width:20px;height:14px;background:#ADD8E6;border:1px solid #ccc"></span> | `lightskyblue` | `87CEFA` | <span style="display:inline-block;width:20px;height:14px;background:#87CEFA;border:1px solid #ccc"></span> |
| `skyblue` | `87CEEB` | <span style="display:inline-block;width:20px;height:14px;background:#87CEEB;border:1px solid #ccc"></span> | `deepskyblue` | `00BFFF` | <span style="display:inline-block;width:20px;height:14px;background:#00BFFF;border:1px solid #ccc"></span> | `dodgerblue` | `1E90FF` | <span style="display:inline-block;width:20px;height:14px;background:#1E90FF;border:1px solid #ccc"></span> |
| `cornflowerblue` | `6495ED` | <span style="display:inline-block;width:20px;height:14px;background:#6495ED;border:1px solid #ccc"></span> | `steelblue` | `4682B4` | <span style="display:inline-block;width:20px;height:14px;background:#4682B4;border:1px solid #ccc"></span> | `lightsteelblue` | `B0C4DE` | <span style="display:inline-block;width:20px;height:14px;background:#B0C4DE;border:1px solid #ccc"></span> |
| `royalblue` | `4169E1` | <span style="display:inline-block;width:20px;height:14px;background:#4169E1;border:1px solid #ccc"></span> | `mediumblue` | `0000CD` | <span style="display:inline-block;width:20px;height:14px;background:#0000CD;border:1px solid #ccc"></span> | `darkblue` | `00008B` | <span style="display:inline-block;width:20px;height:14px;background:#00008B;border:1px solid #ccc"></span> |
| `midnightblue` | `191970` | <span style="display:inline-block;width:20px;height:14px;background:#191970;border:1px solid #ccc"></span> | `slateblue` | `6A5ACD` | <span style="display:inline-block;width:20px;height:14px;background:#6A5ACD;border:1px solid #ccc"></span> | `blueviolet` | `8A2BE2` | <span style="display:inline-block;width:20px;height:14px;background:#8A2BE2;border:1px solid #ccc"></span> |
| `indigo` | `4B0082` | <span style="display:inline-block;width:20px;height:14px;background:#4B0082;border:1px solid #ccc"></span> | | | | | | |

## Cyans & Teals

| Name | Hex | &nbsp; | Name | Hex | &nbsp; | Name | Hex |
|------|-----|--------|------|-----|--------|------|-----|
| `cadetblue` | `5F9EA0` | <span style="display:inline-block;width:20px;height:14px;background:#5F9EA0;border:1px solid #ccc"></span> | `lightseagreen` | `20B2AA` | <span style="display:inline-block;width:20px;height:14px;background:#20B2AA;border:1px solid #ccc"></span> | `turquoise` | `40E0D0` | <span style="display:inline-block;width:20px;height:14px;background:#40E0D0;border:1px solid #ccc"></span> |
| `mediumturquoise` | `48D1CC` | <span style="display:inline-block;width:20px;height:14px;background:#48D1CC;border:1px solid #ccc"></span> | `darkturquoise` | `00CED1` | <span style="display:inline-block;width:20px;height:14px;background:#00CED1;border:1px solid #ccc"></span> | `paleturquoise` | `AFEEEE` | <span style="display:inline-block;width:20px;height:14px;background:#AFEEEE;border:1px solid #ccc"></span> |
| `aquamarine` | `7FFFD4` | <span style="display:inline-block;width:20px;height:14px;background:#7FFFD4;border:1px solid #ccc"></span> | `mediumaquamarine` | `66CDAA` | <span style="display:inline-block;width:20px;height:14px;background:#66CDAA;border:1px solid #ccc"></span> | `darkcyan` | `008B8B` | <span style="display:inline-block;width:20px;height:14px;background:#008B8B;border:1px solid #ccc"></span> |

## Greens

| Name | Hex | &nbsp; | Name | Hex | &nbsp; | Name | Hex |
|------|-----|--------|------|-----|--------|------|-----|
| `honeydew` | `F0FFF0` | <span style="display:inline-block;width:20px;height:14px;background:#F0FFF0;border:1px solid #ccc"></span> | `palegreen` | `98FB98` | <span style="display:inline-block;width:20px;height:14px;background:#98FB98;border:1px solid #ccc"></span> | `lightgreen` | `90EE90` | <span style="display:inline-block;width:20px;height:14px;background:#90EE90;border:1px solid #ccc"></span> |
| `springgreen` | `00FF7F` | <span style="display:inline-block;width:20px;height:14px;background:#00FF7F;border:1px solid #ccc"></span> | `lime` | `00FF00` | <span style="display:inline-block;width:20px;height:14px;background:#00FF00;border:1px solid #ccc"></span> | `limegreen` | `32CD32` | <span style="display:inline-block;width:20px;height:14px;background:#32CD32;border:1px solid #ccc"></span> |
| `lawngreen` | `7CFC00` | <span style="display:inline-block;width:20px;height:14px;background:#7CFC00;border:1px solid #ccc"></span> | `chartreuse` | `7FFF00` | <span style="display:inline-block;width:20px;height:14px;background:#7FFF00;border:1px solid #ccc"></span> | `greenyellow` | `ADFF2F` | <span style="display:inline-block;width:20px;height:14px;background:#ADFF2F;border:1px solid #ccc"></span> |
| `yellowgreen` | `9ACD32` | <span style="display:inline-block;width:20px;height:14px;background:#9ACD32;border:1px solid #ccc"></span> | `darkseagreen` | `8FBC8F` | <span style="display:inline-block;width:20px;height:14px;background:#8FBC8F;border:1px solid #ccc"></span> | `seagreen` | `2E8B57` | <span style="display:inline-block;width:20px;height:14px;background:#2E8B57;border:1px solid #ccc"></span> |
| `forestgreen` | `228B22` | <span style="display:inline-block;width:20px;height:14px;background:#228B22;border:1px solid #ccc"></span> | `mediumseagreen` | `3CB371` | <span style="display:inline-block;width:20px;height:14px;background:#3CB371;border:1px solid #ccc"></span> | `darkgreen` | `006400` | <span style="display:inline-block;width:20px;height:14px;background:#006400;border:1px solid #ccc"></span> |
| `olivedrab` | `6B8E23` | <span style="display:inline-block;width:20px;height:14px;background:#6B8E23;border:1px solid #ccc"></span> | `darkolivegreen` | `556B2F` | <span style="display:inline-block;width:20px;height:14px;background:#556B2F;border:1px solid #ccc"></span> | | | |

## Yellows & Oranges

| Name | Hex | &nbsp; | Name | Hex | &nbsp; | Name | Hex |
|------|-----|--------|------|-----|--------|------|-----|
| `lightyellow` | `FFFFE0` | <span style="display:inline-block;width:20px;height:14px;background:#FFFFE0;border:1px solid #ccc"></span> | `lemonchiffon` | `FFFACD` | <span style="display:inline-block;width:20px;height:14px;background:#FFFACD;border:1px solid #ccc"></span> | `ivory` | `FFFFF0` | <span style="display:inline-block;width:20px;height:14px;background:#FFFFF0;border:1px solid #ccc"></span> |
| `beige` | `F5F5DC` | <span style="display:inline-block;width:20px;height:14px;background:#F5F5DC;border:1px solid #ccc"></span> | `wheat` | `F5DEB3` | <span style="display:inline-block;width:20px;height:14px;background:#F5DEB3;border:1px solid #ccc"></span> | `tan` | `D2B48C` | <span style="display:inline-block;width:20px;height:14px;background:#D2B48C;border:1px solid #ccc"></span> |
| `khaki` | `F0E68C` | <span style="display:inline-block;width:20px;height:14px;background:#F0E68C;border:1px solid #ccc"></span> | `gold` | `FFD700` | <span style="display:inline-block;width:20px;height:14px;background:#FFD700;border:1px solid #ccc"></span> | `goldenrod` | `DAA520` | <span style="display:inline-block;width:20px;height:14px;background:#DAA520;border:1px solid #ccc"></span> |
| `darkgoldenrod` | `B8860B` | <span style="display:inline-block;width:20px;height:14px;background:#B8860B;border:1px solid #ccc"></span> | `orange` | `FFA500` | <span style="display:inline-block;width:20px;height:14px;background:#FFA500;border:1px solid #ccc"></span> | `darkorange` | `FF8C00` | <span style="display:inline-block;width:20px;height:14px;background:#FF8C00;border:1px solid #ccc"></span> |

## Browns

| Name | Hex | &nbsp; | Name | Hex | &nbsp; | Name | Hex |
|------|-----|--------|------|-----|--------|------|-----|
| `burlywood` | `DEB887` | <span style="display:inline-block;width:20px;height:14px;background:#DEB887;border:1px solid #ccc"></span> | `peru` | `CD853F` | <span style="display:inline-block;width:20px;height:14px;background:#CD853F;border:1px solid #ccc"></span> | `chocolate` | `D2691E` | <span style="display:inline-block;width:20px;height:14px;background:#D2691E;border:1px solid #ccc"></span> |
| `sienna` | `A0522D` | <span style="display:inline-block;width:20px;height:14px;background:#A0522D;border:1px solid #ccc"></span> | `saddlebrown` | `8B4513` | <span style="display:inline-block;width:20px;height:14px;background:#8B4513;border:1px solid #ccc"></span> | `rosybrown` | `BC8F8F` | <span style="display:inline-block;width:20px;height:14px;background:#BC8F8F;border:1px solid #ccc"></span> |
| `brown` | `A52A2A` | <span style="display:inline-block;width:20px;height:14px;background:#A52A2A;border:1px solid #ccc"></span> | | | | | | |

## Reds & Corals

| Name | Hex | &nbsp; | Name | Hex | &nbsp; | Name | Hex |
|------|-----|--------|------|-----|--------|------|-----|
| `mistyrose` | `FFE4E1` | <span style="display:inline-block;width:20px;height:14px;background:#FFE4E1;border:1px solid #ccc"></span> | `peachpuff` | `FFDAB9` | <span style="display:inline-block;width:20px;height:14px;background:#FFDAB9;border:1px solid #ccc"></span> | `lightcoral` | `F08080` | <span style="display:inline-block;width:20px;height:14px;background:#F08080;border:1px solid #ccc"></span> |
| `salmon` | `FA8072` | <span style="display:inline-block;width:20px;height:14px;background:#FA8072;border:1px solid #ccc"></span> | `darksalmon` | `E9967A` | <span style="display:inline-block;width:20px;height:14px;background:#E9967A;border:1px solid #ccc"></span> | `lightsalmon` | `FFA07A` | <span style="display:inline-block;width:20px;height:14px;background:#FFA07A;border:1px solid #ccc"></span> |
| `coral` | `FF7F50` | <span style="display:inline-block;width:20px;height:14px;background:#FF7F50;border:1px solid #ccc"></span> | `tomato` | `FF6347` | <span style="display:inline-block;width:20px;height:14px;background:#FF6347;border:1px solid #ccc"></span> | `orangered` | `FF4500` | <span style="display:inline-block;width:20px;height:14px;background:#FF4500;border:1px solid #ccc"></span> |
| `firebrick` | `B22222` | <span style="display:inline-block;width:20px;height:14px;background:#B22222;border:1px solid #ccc"></span> | `darkred` | `8B0000` | <span style="display:inline-block;width:20px;height:14px;background:#8B0000;border:1px solid #ccc"></span> | `crimson` | `DC143C` | <span style="display:inline-block;width:20px;height:14px;background:#DC143C;border:1px solid #ccc"></span> |

## Pinks & Purples

| Name | Hex | &nbsp; | Name | Hex | &nbsp; | Name | Hex |
|------|-----|--------|------|-----|--------|------|-----|
| `pink` | `FFC0CB` | <span style="display:inline-block;width:20px;height:14px;background:#FFC0CB;border:1px solid #ccc"></span> | `lightpink` | `FFB6C1` | <span style="display:inline-block;width:20px;height:14px;background:#FFB6C1;border:1px solid #ccc"></span> | `hotpink` | `FF69B4` | <span style="display:inline-block;width:20px;height:14px;background:#FF69B4;border:1px solid #ccc"></span> |
| `deeppink` | `FF1493` | <span style="display:inline-block;width:20px;height:14px;background:#FF1493;border:1px solid #ccc"></span> | `palevioletred` | `DB7093` | <span style="display:inline-block;width:20px;height:14px;background:#DB7093;border:1px solid #ccc"></span> | `orchid` | `DA70D6` | <span style="display:inline-block;width:20px;height:14px;background:#DA70D6;border:1px solid #ccc"></span> |
| `mediumorchid` | `BA55D3` | <span style="display:inline-block;width:20px;height:14px;background:#BA55D3;border:1px solid #ccc"></span> | `darkorchid` | `9932CC` | <span style="display:inline-block;width:20px;height:14px;background:#9932CC;border:1px solid #ccc"></span> | `thistle` | `D8BFD8` | <span style="display:inline-block;width:20px;height:14px;background:#D8BFD8;border:1px solid #ccc"></span> |
| `plum` | `DDA0DD` | <span style="display:inline-block;width:20px;height:14px;background:#DDA0DD;border:1px solid #ccc"></span> | `violet` | `EE82EE` | <span style="display:inline-block;width:20px;height:14px;background:#EE82EE;border:1px solid #ccc"></span> | `mediumpurple` | `9370DB` | <span style="display:inline-block;width:20px;height:14px;background:#9370DB;border:1px solid #ccc"></span> |
| `rebeccapurple` | `663399` | <span style="display:inline-block;width:20px;height:14px;background:#663399;border:1px solid #ccc"></span> | `darkviolet` | `9400D3` | <span style="display:inline-block;width:20px;height:14px;background:#9400D3;border:1px solid #ccc"></span> | `mediumvioletred` | `C71585` | <span style="display:inline-block;width:20px;height:14px;background:#C71585;border:1px solid #ccc"></span> |
