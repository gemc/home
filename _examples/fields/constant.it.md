---
layout: default
title: "Constant Field"
permalink: /examples/fields/constant.html
lang: it
human_reviewed: false
---

# Esempio di Campo Costante
<hr style="height:4px;border:0;background:#4a90e2;">

Questo esempio di campo mostra un campo magnetico longitudinale uniforme utilizzando `gmultipoles`. È una
scena minimale per verificare la visualizzazione delle linee di campo senza eseguire eventi.

{% assign example = site.data.examples | where: "title", "Constant Field" | first %}

<br/>

## Avvio rapido

Copia l'esempio nella directory corrente, costruisci il database della geometria e apri la visualizzazione del campo:

```shell
cp -r $GEMC_HOME/examples/fields/constant .
cd constant
./constant.py
gemc constant.yaml -gui
```

<br/>

## Geometria

La geometria è definita in `constant.py`. Il volume world %%root%% contiene una scatola trasparente,
%%constant_field_box%%, con la sua proprietà %%mfield%% impostata su %%constant%%.

<br/>

## Definizione del Campo

Il file YAML definisce un campo uniforme longitudinale tramite `gmultipoles`:

```yaml
gmultipoles:
  - name: constant
    pole_number: 2
    strength: 1
    rotaxis: z
    longitudinal: true
```

Le opzioni di visualizzazione richiedono 30 linee di campo e i bordi geometrici ausiliari:

```yaml
show_field_lines: 30
show_auxiliary_edges: true
```

<br/>

## Visualizzazione del Campo

{% include figure.html
src="/assets/images/examples/constant/gemc_view.png"
caption="Visualizzazione del campo costante: una scatola trasparente con linee di campo uniformi."
%}

<br/>

## Utilizzo

Il file `constant.yaml` imposta `n: 0`, quindi non è necessario alcun `/run/beamOn` per questa scena di
visualizzazione. Aggiungi `-fieldAt` per ispezionare il campo configurato in un punto:

```shell
gemc constant.yaml -fieldAt="0*cm 0*cm 0*cm"
```
