---
layout: default
title: "Cherenkov"
permalink: /examples/optical/cherenkov.html
lang: it
human_reviewed: false
---

[low-img]: /home/assets/images/examples/cherenkov/low_index_radiator.png
[medium-img]: /home/assets/images/examples/cherenkov/medium_index_radiator.png
[high-img]: /home/assets/images/examples/cherenkov/high_index_radiator.png
[lowy-img]: /home/assets/images/examples/cherenkov/low_index_radiator_y_vs_x.png
[mediumy-img]: /home/assets/images/examples/cherenkov/medium_index_radiator_y_vs_x.png
[highy-img]: /home/assets/images/examples/cherenkov/high_index_radiator_y_vs_x.png


# Esempio Cherenkov
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

Questo esempio mostra come attivare la radiazione Cherenkov in un rivelatore GEMC.
I tre nomi dei radiatori sono etichette dimostrative neutre. Le loro costanti ottiche potrebbero non essere
fisicamente realistiche e non vanno interpretate come definizioni di materiali reali.

{% assign example = site.data.examples | where: "title", "Cherenkov" | first %}

Puoi eseguire questo esempio nel tuo browser: [![{{ example.title }}]({{ example.badge }})]({{ example.binder }}){:target="_blank" rel="noopener noreferrer"} 

<br/>

## Avvio rapido

Copia l'esempio nella tua directory corrente.
Per creare la geometria, eseguire 1 evento e produrre i file di output ROOT e CSV:

```shell
cp -r $GEMC_HOME/examples/optical/cherenkov .
cd cherenkov
./cherenkov.py
gemc cherenkov.yaml -n=1
```

<br/>

## Geometria

La geometria, mostrata di seguito, è definita in `cherenkov.py`. Viene prodotta in tre varianti:
%%default%%, %%mediumIndexRadiator%% e %%highIndexRadiator%%.

Il mondo (un box chiamato %%root%%) contiene un box %%radiator%%. Il materiale del radiatore dipende dalla variante selezionata:

{:.zebra .compact-table}

| variante | materiale | colore | intervallo dell'indice di rifrazione |
|-----------|----------|-------|------------------------|
| %%default%% | %%lowIndexRadiator%% | rosso | 1.0010-1.0013 |
| %%mediumIndexRadiator%% | %%mediumIndexRadiator%% | blu | 1.0110-1.0150 |
| %%highIndexRadiator%% | %%highIndexRadiator%% | verde | 1.0500-1.0530 |


- un rivelatore %%gPhotonDetector%% composto da quattro box (%%detector_left%%, %%detector_right%%, %%detector_top%% e %%detector_bottom%%). Questo lascia un piccolo foro al centro per il fascio.

Visualizzatore interattivo:

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}/assets/images/examples/cherenkov/cherenkov.vtksz"
  title="Interactive VTK.js view of the Cherenkov geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

{% include figure.html
src="/assets/images/examples/cherenkov/high_index_radiator.png"
caption="Cherenkov geometry with 1 generated electron. The highIndexRadiator volume (green, style = 2 renders it as a cloud) is the medium generating Cherenkov radiation."
%}


<br/>

## Lista della fisica

Per impostazione predefinita, nel file YAML viene usato `FTFP_BERT + G4OpticalPhysics`. Il componente di fisica ottica è necessario per produrre fotoni ottici.

{% include notes/physics-list-note.md %}

<br/>

## Generatore

La cinematica delle particelle è definita nel file YAML:

```yaml
gparticle:
  - name: e-
    p: 1000*MeV
    vz: -50*cm
```

Vedi anche la [Documentazione del generatore interno]( /home/documentation/generator/internal ) per maggiori informazioni.


<br/>


## Digitalizzazione

Le sensibilità dei volumi del rivelatore sono specificate con la digitalizzazione %%gPhotonDetector%% (una delle routine GEMC predefinite disponibili)
in `cherenkov.py`.

L'%%identifier%% è usato per distinguere i diversi box del rivelatore:

```python
backplate.digitization = "gPhotonDetector"
backplate.set_identifier("detector", panel_id)
```

Vedi la [Documentazione sul flusso]( /home/documentation/sensitivity/gPhotonDetector ) per maggiori informazioni.


<br/>

## Utilizzo

### Costruzione del rivelatore

Usa lo script Python `cherenkov.py` per costruire il rivelatore. Per impostazione predefinita, la configurazione è salvata in un file SQLite
chiamato `gemc.db`. Le opzioni da riga di comando possono definire il tipo di database, le varianti e il numero di run.

Vedi anche [Costruzione della geometria]( /home/documentation/geometry/geometry_building ) per maggiori informazioni.

<br/>

### Esecuzione di GEMC

Il file `cherenkov.yaml` può essere usato per eseguire la configurazione. Aggiungi `-gui` per eseguire in modo interattivo:

```shell
gemc cherenkov.yaml -gui
```

Il file YAML imposta `g4view.cloudPoints: 60000` in modo che i volumi in stile nuvola siano abbastanza densi per gli screenshot della geometria renderizzata.

Modifica `cherenkov.yaml` secondo necessità, in particolare per aggiungere particelle, controllare il numero di thread o cambiare l'output.
La digitalizzazione %%gPhotonDetector%% registra i fotoni ottici anche quando depositano energia nulla, quindi %%recordZeroEdep%%
non è necessario per questo esempio.

<br/>

### Varianti

All'interno del file YAML, la variante è impostata su %%mediumIndexRadiator%%. Puoi sostituirla con %%default%% o %%highIndexRadiator%%
per cambiare il materiale. Ad esempio:

```yaml
gsystem:
  - name: cherenkov
    variation: highIndexRadiator
```

Materiali del radiatore diversi producono rese e angoli fotonici diversi, come mostrato di seguito.
Le loro costanti ottiche sono valori dimostrativi e potrebbero non essere fisicamente realistici.
Usa il nome della variante nel nome del file %%gstreamer%% quando vuoi file di output separati per ogni variante.


<br/>

|:---:|:---:|:---:|
| ![low index radiator](/home/assets/images/examples/cherenkov/low_index_radiator.png) | ![medium index radiator](/home/assets/images/examples/cherenkov/medium_index_radiator.png) | ![high index radiator](/home/assets/images/examples/cherenkov/high_index_radiator.png) |
| ![low index radiator y vs x](/home/assets/images/examples/cherenkov/low_index_radiator_y_vs_x.png) | ![medium index radiator y vs x](/home/assets/images/examples/cherenkov/medium_index_radiator_y_vs_x.png) | ![high index radiator y vs x](/home/assets/images/examples/cherenkov/high_index_radiator_y_vs_x.png) |

<p class="image-caption">
  Sinistra: <span class="gstring">lowIndexRadiator</span>, Centro: <span class="gstring">mediumIndexRadiator</span>, Destra: <span class="gstring">highIndexRadiator</span>.
</p>

<br/>

## Esecuzione degli eventi

{% include figure.html
src="/assets/images/examples/cherenkov/gemc_view.png"
caption="Cherenkov simulation: electron beam entering the radiator volume."
%}

<br/>

## Output

L'opzione %%gstreamer%% seleziona i nomi dei file di output e il formato:


```yaml
gstreamer:
  - format: csv
    filename: cherenkov
```

Poiché %%gPhotonDetector%% è una digitalizzazione per evento, GEMC produrrà un file di output per thread.
Per i file ROOT, puoi usare `hadd` per unire i file.

Vedi anche la [Documentazione sull'output]( /home/documentation/output ) per maggiori informazioni.

<br/>

## Creazione di grafici con l'Analizzatore GEMC

Esegui prima GEMC con 1 evento. Il file YAML predefinito scrive i flussi CSV dell'analizzatore.

```shell
gemc cherenkov.yaml -n=1
```

Traccia l'energia totale depositata per hit:

```shell
gemc-analyzer cherenkov_t0_digitized.csv totEdep --kind csv
```

![cherenkov total energy deposited per hit][cherenkov-analyzer_totEdep]{:width="70%"}

[cherenkov-analyzer_totEdep]: /home/assets/images/examples/cherenkov/analyzer_totEdep.png

Traccia le posizioni degli hit y vs x:

```shell
gemc-analyzer cherenkov_t0_true_info.csv --kind csv --data true_info --plot yvsx --bins 80
```

![cherenkov y vs x hit positions][cherenkov-analyzer_yvsx]{:width="70%"}

[cherenkov-analyzer_yvsx]: /home/assets/images/examples/cherenkov/analyzer_yvsx.png
