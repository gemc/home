---
layout: default
title: "Mirrors"
permalink: /examples/optical/mirrors.html
lang: it
human_reviewed: false
---

# Esempio Mirrors
<hr style="height:4px;border:0;background:#4a90e2;">

Questo esempio illustra le superfici ottiche ("mirrors", specchi) di GEMC. Tre elettroni identici da 1 GeV
attraversano un radiatore gassoso a basso indice di rifrazione, ciascuno puntato al centro di una piastra
riflettente. I fotoni Cherenkov restano in un cono stretto in avanti attorno a ciascun elettrone e si
depositano sulla piastra di quell'elettrone. Ogni piastra illustra una diversa definizione di specchio:

* %%polished_metal%% - superficie di tipo skin `dielectric_metal` / `polished` / `unified` con una
  tabella di riflettività esplicita: un tipico specchio rivestito di metallo;
* %%rough_metal%% - la stessa superficie skin con finitura `ground`: la riflessione si distribuisce in un
  lobo speculare (%%specularlobe%% = 1) la cui sfocatura è impostata da %%sigmaAlpha%%;
* %%semi_transparent%% - uno specchio semiargentato definito come **superficie di bordo** tra il
  radiatore e la sua piastra: il 60% dei fotoni viene riflesso, il 30% viene trasmesso attraverso la
  piastra (%%transmittance%%) e il 10% viene assorbito.

Ogni piastra riflette i propri fotoni di nuovo sul proprio pannello rivelatore di fotoni a monte (usando la
digitalizzazione %%gPhotonDetector%% e disegnato nel colore del suo specchio), così che i pannelli vedano
condizioni identiche e differisca solo la riflessione. Un quarto pannello conta i fotoni trasmessi dopo che
hanno attraversato un ampio spazio dietro la piastra semitrasparente. Conteggi relativi tipici di fotoni
(pannello piatto = 1):

| Pannello | Superficie | Conteggio relativo |
|---|---|---|
| piatto (oro) | polished, R = 0.90 | 1.00 |
| ruvido (tomato) | lobo speculare, sigmaAlpha = 0.03 | circa 0.99 (immagine sfocata, lieve dispersione) |
| semi (blu) | riflesso, R = 0.60 | circa 0.69 (= 0.60 / 0.90) |
| dietro (blu) | trasmesso, T = 0.30 | circa 0.37 (= 0.30 / 0.90) |

<br/>

## Quickstart

Copia l'esempio nella tua directory corrente.
Per creare la geometria, eseguire 10 eventi e produrre file di output CSV:

```shell
cp -r $GEMC_HOME/examples/optical/mirrors .
cd mirrors
./mirrors.py
gemc mirrors.yaml -n=10
```

<br/>

## Geometria

La geometria è definita in `mirrors.py`. Il volume world %%root%% contiene un radiatore gassoso da 1 m^3
(%%radiatorGas%%, un gas dimostrativo con indice di rifrazione circa 1.001). All'interno del radiatore:

* tre piastre sottili a metà del radiatore: due piastre di alluminio che portano gli specchi skin e la
  piastra semitrasparente - fatta di gas radiatore così che i fotoni trasmessi proseguano
  indisturbati - bersaglio della superficie di bordo %%semi_transparent%%;
* tre pannelli rivelatori di fotoni a monte, ciascuno allineato con una piastra e disegnato nel colore del
  suo specchio, che raccolgono i fotoni riflessi da quella piastra;
* un lungo spazio di trasmissione dietro la piastra semitrasparente, riempito con un vuoto ottico
  (indice di rifrazione 1) così che l'elettrone non irradi luce Cherenkov nello spazio e i fotoni
  trasmessi possano essere visti mentre lo attraversano;
* un quarto pannello alla fine dello spazio, che raccoglie i fotoni trasmessi.

Visualizzatore interattivo:

{% assign mirrors_vtk = "/assets/images/examples/mirrors/mirrors.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}{{ mirrors_vtk }}"
  title="Interactive VTK.js view of the mirrors geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

{% include figure.html
src="/assets/images/examples/mirrors/gemc_view.png"
caption="Mirrors simulation with 1 generated event."
%}

<br/>

## Definizioni degli specchi

Ogni specchio è un `GMirror` pubblicato insieme alla geometria:

```python
polished = GMirror("polished_metal")
polished.type = "dielectric_metal"
polished.finish = "polished"
polished.model = "unified"
polished.border = "SkinSurface"
polished.photonEnergy = "2.0*eV 3.0*eV 4.0*eV 5.0*eV 6.0*eV"
polished.reflectivity = "0.90 0.90 0.89 0.88 0.87"
polished.publish(cfg)
```

e i volumi vi fanno riferimento per nome:

```python
plate.mirror = "polished_metal"
```

Consulta la [documentazione sugli specchi](/home/documentation/optical/mirrors) per il riferimento completo
dei campi.

<br/>

## Fisica

La steering card abilita la fisica ottica:

```yaml
phys_list: FTFP_BERT + G4OpticalPhysics
```

L'esecuzione dell'esempio stampa le superfici create da GEMC:

```text
G4World: created optical surface <mirrors/polished_metal> type <dielectric_metal>,
finish <polished>, model <unified>
G4World: created 3 optical surfaces, attached to 2 skin and 1 border logical surfaces
```


## Grafici con il GEMC Analyzer

Esegui prima GEMC con 10 eventi. Il file YAML predefinito scrive i flussi CSV dell'analyzer.

```shell
gemc mirrors.yaml -n=10
```

### y vs x per pannello

I grafici seguenti suddividono le posizioni dei colpi dei fotoni ottici per %%panel%%. Il pannello di
trasmissione posteriore è mostrato come grafico a sé, non fuso nel grafico del pannello riflesso
semitrasparente. Il conteggio mostrato su ciascuna immagine è il numero di righe selezionate dal flusso di
informazioni true.

| | |
|:---:|:---:|
| ![flat panel y vs x][mirrors-flat-panel-yvsx] | ![rough panel y vs x][mirrors-rough-panel-yvsx] |
| pannello riflesso piatto<br>conteggi = 2,445 | pannello riflesso ruvido<br>conteggi = 2,269 |
| ![semi panel y vs x][mirrors-semi-panel-yvsx] | ![back panel y vs x][mirrors-back-panel-yvsx] |
| pannello riflesso semitrasparente<br>conteggi = 1,681 | pannello trasmesso posteriore<br>conteggi = 918 |

[mirrors-flat-panel-yvsx]: /home/assets/images/examples/mirrors/flat_panel_y_vs_x.png
[mirrors-rough-panel-yvsx]: /home/assets/images/examples/mirrors/rough_panel_y_vs_x.png
[mirrors-semi-panel-yvsx]: /home/assets/images/examples/mirrors/semi_panel_y_vs_x.png
[mirrors-back-panel-yvsx]: /home/assets/images/examples/mirrors/back_panel_y_vs_x.png
