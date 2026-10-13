---
layout: default
title: "PyVista Geometry Visualization"
permalink: /examples/basic/pyvista.html
lang: it
human_reviewed: false
---

# Visualizzazione della geometria con PyVista
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

GEMC utilizza [PyVista](https://docs.pyvista.org/) per visualizzare la geometria del rivelatore
direttamente da Python. La geometria può essere visualizzata in modo interattivo, esportata come file `.vtksz`
per la visualizzazione sul web o renderizzata come screenshot.
Consulta la [documentazione dell'API PyVista](/home/documentation/api/pyvista_api)
per la documentazione di riferimento completa dell'API.

<br/>

## Avvio rapido

Copia l'esempio nella directory corrente:

```shell
cp -r $GEMC_HOME/examples/basic/pyvista .
cd pyvista
./gemc_pyvista.py
```

Per visualizzare un'anteprima interattiva della geometria (apre una finestra PyVista):

```shell
./gemc_pyvista.py -pv
```

<br/>

## Geometria

L'esempio definisce quattro volumi in `pyvista_basic_shapes.py`: un contenitore a forma di scatola trasparente,
un cilindro pieno, una sfera e una piccola scatola ruotata all'interno del contenitore.

Visualizzatore interattivo:

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}/assets/images/examples/pyvista/pyvista.vtksz"
  title="Interactive VTK.js view of the pyvista geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## Utilizzo

### Costruzione della geometria

```shell
./gemc_pyvista.py
```

{% include notes/python-api-note.md %}

<br/>

### Esecuzione di GEMC

```shell
gemc pyvista.yaml -n=10
```

Aggiungi `-gui` per eseguire in modo interattivo.
