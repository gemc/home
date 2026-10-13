---
layout: default
title: "Boolean Solids"
permalink: /examples/basic/boolean_solids.html
lang: it
human_reviewed: false
---

# Esempio di solidi booleani
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

Questo esempio illustra le operazioni sui solidi booleani di GEMC. Costruisce tre solidi posizionati a
partire da volumi componenti non posizionati: una piastra con un foro ottenuto per sottrazione, una croce
ottenuta da un'unione e una lente ottenuta dall'intersezione di due sfere.

<br/>

## Avvio rapido

Copia l'esempio nella tua directory corrente.
Per creare la geometria ed eseguire 10 eventi:

```shell
cp -r $GEMC_HOME/examples/basic/boolean_solids .
cd boolean_solids
./boolean_solids.py
gemc boolean_solids.yaml -n=10
```

<br/>

## Geometria

La geometria è definita in `boolean_solids.py`.

Il mondo (una scatola chiamata %%root%%) contiene tre volumi booleani visibili:

| Volume | Operazione | Componenti |
|--------|-----------|------------|
| %%plate_with_hole%% | sottrazione | %%plate_box - plate_hole%% |
| %%cross%% | unione | %%bar + bar_rotated%% |
| %%lens%% | intersezione | %%sphere_one * sphere_two%% |

I volumi componenti usano il materiale speciale %%Component%%. Definiscono gli operandi dell'espressione
booleana ma non vengono posizionati come volumi visibili del rivelatore. I volumi booleani risultanti sono
posizionati come qualsiasi altro `GVolume`, con materiale, colore, posizione e rotazione propri.

Visualizzatore interattivo:

{% assign boolean_solids_vtksz = "/assets/images/examples/boolean_solids/boolean_solids.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}{{ boolean_solids_vtksz }}"
  title="Interactive VTK.js view of the boolean solids geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## Espressioni booleane

Un solido booleano viene selezionato assegnando %%solidsOpr%%:

```python
plate.solidsOpr = 'plate_box - plate_hole'
cross.solidsOpr = 'bar + bar_rotated'
lens.solidsOpr = 'sphere_one * sphere_two'
```

Il primo operando viene valutato con la propria origine come riferimento. Il secondo operando usa la propria
posizione e rotazione relative al primo operando. Ad esempio, %%plate_hole%% viene spostato di 30 mm prima di
essere sottratto da %%plate_box%%, quindi il foro è decentrato.

<br/>

## Generatore

La cinematica delle particelle è definita nel file YAML:

```yaml
gparticle:
  - name: e-
    p: 500*MeV
    theta: 90*deg
    vx: -40*cm
    delta_vx: 12*cm
    randomVertexModel: uniform
```

Consulta anche la [Documentazione del generatore interno]( /home/documentation/generator/internal ) per
maggiori informazioni.

<br/>

## Utilizzo

### Costruzione del rivelatore

Usa lo script Python `boolean_solids.py` per costruire il rivelatore. Per impostazione predefinita, la
configurazione viene salvata in un file SQLite chiamato `gemc.db`.

```shell
./boolean_solids.py
```

Consulta anche la [Costruzione della geometria]( /home/documentation/geometry/geometry_building ) per
maggiori informazioni.

<br/>

### Esecuzione di GEMC

Il file `boolean_solids.yaml` può essere usato per eseguire la configurazione. Aggiungi `-gui` per eseguire
in modo interattivo:

```shell
gemc boolean_solids.yaml -gui
```

<br/>

## Esecuzione degli eventi

{% include figure.html
src="/assets/images/examples/boolean_solids/gemc_view.png"
caption="Boolean solids simulation: electrons crossing the subtraction, union, and intersection volumes."
%}
