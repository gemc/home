---
layout: default
title: "Torus ASCII Field Map"
permalink: /examples/fields/torus.html
lang: it
human_reviewed: false
---

# Esempio di Mappa di Campo ASCII Torus
<hr style="height:4px;border:0;background:#4a90e2;">

Questo esempio di campo mostra una mappa di campo ASCII segmentata in phi caricata tramite il plugin
di campo `asciimap`. Utilizza un volume trasparente a forma di toro per rendere facilmente
riconoscibile la regione del campo.

{% assign example = site.data.examples | where: "title", "Torus ASCII Field Map" | first %}

<br/>

## Avvio rapido

Copia l'esempio nella tua directory corrente, costruisci il database della geometria e apri la
visualizzazione del campo:

```shell
cp -r $GEMC_HOME/examples/fields/torus .
cd torus
./torus.py
gemc torus.yaml -gui
```

<br/>

## Geometria

La geometria è definita in `torus.py`. Il volume world %%root%% contiene un toro trasparente,
%%torus_field_volume%%, con la sua proprietà %%mfield%% impostata su %%torus%%.

<br/>

## Definizione del campo

Il file YAML carica `torus_map.txt` come mappa ASCII segmentata in phi:

```yaml
gfields:
  - name: torus
    type: asciimap
    symmetry: phi-segmented
    map: torus_map.txt
    field_unit: kilogauss
    interpolation: none
    integration_stepper: G4ClassicalRK4
    minimum_step: 1*mm
    coordinate1: "azimuthal,    4, 0*deg,  30*deg"
    coordinate2: "transverse,   6, 0*cm,   500*cm"
    coordinate3: "longitudinal, 6, 100*cm, 600*cm"
```

Le prime tre colonne della mappa sono %%azimuthal%%, %%transverse%% e %%longitudinal%%. Le tre
colonne successive sono %%Bx%%, %%By%% e %%Bz%% in kilogauss.

<br/>

## Visualizzazione del campo

{% include figure.html
src="/assets/images/examples/torus/gemc_view.png"
caption="Torus ASCII-map display: a transparent torus with field lines from a phi-segmented map."
%}

<br/>

## Utilizzo

Il file `torus.yaml` imposta `n: 0`, quindi per questa scena di visualizzazione non è necessario alcun
`/run/beamOn`. Aggiungi `-fieldAt` per ispezionare il campo configurato in un punto:

```shell
gemc torus.yaml -fieldAt="250*cm 0*cm 350*cm"
```
