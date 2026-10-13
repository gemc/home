---
layout: default
title: "Dipole Field"
permalink: /examples/fields/dipole.html
lang: it
human_reviewed: false
---

# Esempio di Campo di Dipolo
<hr style="height:4px;border:0;background:#4a90e2;">

Questo esempio di campo mostra un campo di dipolo trasversale ideale generato da `gmultipoles`. È utile per
verificare l'associazione del campo su un singolo volume e le opzioni visive di avvio delle linee di campo.

{% assign example = site.data.examples | where: "title", "Dipole Field" | first %}

<br/>

## Avvio rapido

Copia l'esempio nella directory corrente, costruisci il database della geometria e apri la visualizzazione del campo:

```shell
cp -r $GEMC_HOME/examples/fields/dipole .
cd dipole
./dipole.py
gemc dipole.yaml -gui
```

<br/>

## Geometria

La geometria è definita in `dipole.py`. Il volume world %%root%% contiene una scatola trasparente,
%%dipole_field_box%%, con la sua proprietà %%mfield%% impostata a %%dipole%%.

<br/>

## Definizione del campo

Il file YAML definisce un dipolo da 2 T ruotato di 30 gradi attorno all'asse z:

```yaml
gmultipoles:
  - name: dipole
    pole_number: 2
    strength: 2
    rotaxis: z
    rotation_angle: "30*deg"
```

Le opzioni di visualizzazione richiedono 80 linee di campo e i bordi della geometria ausiliaria:

```yaml
show_field_lines: 80
show_auxiliary_edges: true
```

<br/>

## Visualizzazione del campo

{% include figure.html
src="/assets/images/examples/dipole/gemc_view.png"
caption="Dipole field display: a transparent field box with ideal transverse field lines."
%}

<br/>

## Utilizzo

Il file `dipole.yaml` imposta `n: 0`, quindi non è necessario alcun `/run/beamOn` per questa scena di
visualizzazione. Aggiungi `-fieldAt` per ispezionare il campo configurato in un punto:

```shell
gemc dipole.yaml -fieldAt="0*cm 0*cm 0*cm"
```
