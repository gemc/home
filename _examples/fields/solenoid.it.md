---
layout: default
title: "Solenoid ASCII Field Map"
permalink: /examples/fields/solenoid.html
lang: it
human_reviewed: false
---

# Esempio di Mappa di Campo ASCII per Solenoide
<hr style="height:4px;border:0;background:#4a90e2;">

Questo esempio di campo mostra una mappa di campo ASCII cilindrica caricata tramite il plugin di campo `asciimap`.
Il file della mappa è volutamente piccolo, in modo che l'esempio sia facile da ispezionare e modificare.

{% assign example = site.data.examples | where: "title", "Solenoid ASCII Field Map" | first %}

<br/>

## Avvio rapido

Copia l'esempio nella tua directory corrente, costruisci il database della geometria e apri la visualizzazione del campo:

```shell
cp -r $GEMC_HOME/examples/fields/solenoid .
cd solenoid
./solenoid.py
gemc solenoid.yaml -gui
```

<br/>

## Geometria

La geometria è definita in `solenoid.py`. Il volume world %%root%% contiene un tubo trasparente,
%%solenoid_field_tube%%, con la sua proprietà %%mfield%% impostata a %%solenoid%%.

<br/>

## Definizione del campo

Il file YAML carica `solenoid_map.txt` come mappa ASCII cilindrica-z:

```yaml
gfields:
  - name: solenoid
    type: asciimap
    symmetry: cylindrical-z
    map: solenoid_map.txt
    field_unit: T
    interpolation: linear
    coordinate1: "transverse,   4, 0*m, 3*m"
    coordinate2: "longitudinal, 7, -3*m, 3*m"
```

Le prime due colonne della mappa sono %%transverse%% e %%longitudinal%%. Le due colonne successive sono le
componenti trasversale e longitudinale del campo in tesla.

<br/>

## Visualizzazione del campo

{% include figure.html
src="/assets/images/examples/solenoid/gemc_view.png"
caption="Visualizzazione della mappa ASCII del solenoide: un tubo trasparente con linee di campo da una mappa cilindrica."
%}

<br/>

## Utilizzo

Il file `solenoid.yaml` imposta `n: 0`, quindi non è necessario alcun `/run/beamOn` per questa scena di
visualizzazione. Aggiungi `-fieldAt` per ispezionare il campo configurato in un punto:

```shell
gemc solenoid.yaml -fieldAt="1*m 0*m 0*m"
```
