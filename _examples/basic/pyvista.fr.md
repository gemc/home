---
layout: default
title: "PyVista Geometry Visualization"
permalink: /examples/basic/pyvista.html
lang: fr
human_reviewed: false
---

# Visualisation de la géométrie avec PyVista
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

GEMC utilise [PyVista](https://docs.pyvista.org/) pour visualiser la géométrie du détecteur directement
depuis Python. La géométrie peut être affichée de façon interactive, exportée dans un fichier `.vtksz`
pour un affichage web, ou rendue sous forme de capture d'écran. Consultez la
[documentation de l'API PyVista](/home/documentation/api/pyvista_api) pour la référence complète de l'API.

<br/>

## Démarrage rapide

Copiez l'exemple dans votre répertoire courant :

```shell
cp -r $GEMC_HOME/examples/basic/pyvista .
cd pyvista
./gemc_pyvista.py
```

Pour prévisualiser la géométrie de façon interactive (ouvre une fenêtre PyVista) :

```shell
./gemc_pyvista.py -pv
```

<br/>

## Géométrie

L'exemple définit quatre volumes dans `pyvista_basic_shapes.py` : une boîte conteneur transparente,
un cylindre plein, une sphère, et une petite boîte pivotée à l'intérieur du conteneur.

Visualiseur interactif :

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}/assets/images/examples/pyvista/pyvista.vtksz"
  title="Interactive VTK.js view of the pyvista geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## Utilisation

### Construction de la géométrie

```shell
./gemc_pyvista.py
```

{% include notes/python-api-note.md %}

<br/>

### Exécution de GEMC

```shell
gemc pyvista.yaml -n=10
```

Ajoutez `-gui` pour une exécution interactive.
