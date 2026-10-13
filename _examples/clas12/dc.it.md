---
layout: default
title: "CLAS12 DC"
permalink: /examples/clas12/dc.html
lang: it
human_reviewed: false
---

# Esempio della camera a deriva di CLAS12
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

Questo esempio mostra la geometria della camera a deriva di CLAS12 proveniente da `clas12-systems`.

{% assign example = site.data.examples | where: "title", "DC" | first %}

<br/>

## Avvio rapido

Dal repository `clas12-systems`, genera il database della geometria ed esegui una breve simulazione:

```shell
cd $GEMC_HOME/../clas12-systems/geometry_src/dc
./dc.py
gemc dc.yaml -n=1
```

<br/>

## Geometria

La geometria, mostrata di seguito, è definita in `geometry_src/dc/dc.py` e `geometry_src/dc/geometry.py`.
Il costruttore della DC legge la factory di geometria locale di coatjava, converte le regioni e i superlayer della
camera a deriva di CLAS12 in volumi GEMC e li memorizza in `gemc.db`.

Il mondo (una scatola denominata %%root%%) contiene:

- sei settori di volumi madre delle regioni, denominati da %%region1_s1%% a %%region3_s6%%
- sei settori di volumi dei superlayer, denominati da %%sl1_s1%% a %%sl6_s6%%

Visualizzatore interattivo:

{% assign dc_vtksz = "/home/assets/images/examples/dc/dc.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ dc_vtksz }}"
  title="Interactive VTK.js view of the CLAS12 DC geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## Lista di fisica

Per impostazione predefinita viene utilizzata `FTFP_BERT`, selezionata nel file YAML con `phys_list: FTFP_BERT`.

{% include notes/physics-list-note.md %}

<br/>

## Generatore

La cinematica delle particelle è definita nel file YAML:

```yaml
gparticle:
  - name: e-
    p: 5000*MeV
    delta_p: 1*GeV
    theta: 25*deg
    delta_theta: 15*deg
    randomThetaModel: cosine
    delta_phi: 180*deg
```

Vedi anche la [Documentazione del generatore interno]( /home/documentation/generator/internal ) per maggiori
informazioni.

<br/>

## Digitizzazione

I volumi sensibili dei superlayer utilizzano il plugin di digitizzazione %%dc%% specifico di CLAS12.
Gli identificatori registrano i numeri di settore, superlayer, strato e filo:

```python
gvolume.digitization = "dc"
gvolume.set_identifier("sector", sector, "superlayer", superlayer, "layer", 1, "wire", 1)
```

<br/>

## Utilizzo

### Costruzione del rivelatore

Usa `geometry_src/dc/dc.py` per costruire il rivelatore. Per impostazione predefinita, la configurazione viene
memorizzata in un file SQLite denominato `gemc.db`.

Vedi anche la [Costruzione della geometria]( /home/documentation/geometry/geometry_building ) per maggiori
informazioni.

<br/>

### Esecuzione di GEMC

Il file `dc.yaml` può essere utilizzato per eseguire la simulazione con questa configurazione.
Aggiungi `-gui` per eseguirla in modo interattivo:

```shell
gemc dc.yaml -gui
```

Modifica `dc.yaml` secondo necessità, in particolare per aggiungere particelle, controllare il numero di thread
o cambiare l'output.

<br/>

## Esecuzione degli eventi

{% include figure.html
src="/assets/images/examples/dc/gemc_view.png"
caption="CLAS12 DC simulation: generated electrons crossing the drift chamber geometry."
%}

<br/>

## Output

L'opzione %%gstreamer%% seleziona i nomi dei file e i formati di output:

```yaml
gstreamer:
  - format: csv
    filename: dc
  - format: hipo
    filename: dc
```

Vedi anche la [Documentazione dell'output]( /home/documentation/output ) per maggiori informazioni.


## Creazione di grafici con l'analizzatore GEMC

Esegui prima GEMC con 2.000 eventi. Il file YAML predefinito scrive i flussi CSV dell'analizzatore.

```shell
gemc dc.yaml -n=2000 -no_field=all -plugin_path=/opt/projects/gemc/clas12-systems/build
```

Traccia l'energia totale depositata per hit:

```shell
gemc-analyzer dc_t0_true_info.csv totalEDeposited --kind csv --data true_info
```

![Energia totale depositata per hit nella DC][dc-analyzer_totEdep]{:width="70%"}

[dc-analyzer_totEdep]: /home/assets/images/examples/dc/analyzer_totEdep.png

Traccia le posizioni degli hit, y in funzione di x:

```shell
gemc-analyzer dc_t0_true_info.csv --kind csv --data true_info --plot yvsx --bins 80
```

![Posizioni degli hit nella DC, y in funzione di x][dc-analyzer_yvsx]{:width="70%"}

[dc-analyzer_yvsx]: /home/assets/images/examples/dc/analyzer_yvsx.png

Traccia il tempo TDC digitizzato:

```shell
gemc-analyzer dc_t0_digitized.csv TDC_TDC --kind csv
```

![Tempo TDC digitizzato della DC][dc-analyzer_tdc]{:width="70%"}

[dc-analyzer_tdc]: /home/assets/images/examples/dc/analyzer_tdc.png
