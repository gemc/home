---
layout: default
title: "CLAS12 EC"
permalink: /examples/clas12/ec.html
lang: it
human_reviewed: false
---

# Esempio del calorimetro elettromagnetico di CLAS12
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

Questo esempio mostra la geometria del calorimetro elettromagnetico (EC) di CLAS12 tratta da `clas12-systems`.

{% assign example = site.data.examples | where: "title", "EC" | first %}

<br/>

## Avvio rapido

Dal repository `clas12-systems`, costruisci il database della geometria ed esegui una breve simulazione:

```shell
cd $GEMC_HOME/../clas12-systems/geometry_src/ec
./ec.py
gemc ec.yaml -n=1
```

<br/>

## Geometria

La geometria, mostrata di seguito, è definita in `geometry_src/ec/ec.py` e `geometry_src/ec/geometry.py`.
Il generatore della geometria dell'EC legge la factory locale della geometria di coatjava, converte i settori
del calorimetro di CLAS12, i coperchi, gli assorbitori in piombo e le strisce scintillanti in volumi GEMC
e li memorizza in `gemc.db`.

Il volume mondo (una scatola denominata %%root%%) contiene:

- sei volumi madre dei settori denominati da %%ec_s1%% a %%ec_s6%%
- tre strati dei coperchi per settore (da %%eclid1%% a %%eclid3%%): due rivestimenti in acciaio inossidabile e un nucleo in Last-a-Foam
- strati assorbitori in piombo denominati %%lead_<layer>_s<sector>_view_<view>_stack_<stack>%%
- strisce scintillanti U, V e W denominate %%U_strip_...%%, %%V_strip_...%% e %%W_strip_...%%

L'EC ha una geometria di grandi dimensioni, quindi l'esempio imposta `pyvista-fast: true` in `_data/examples.yml`
per usare la modalità di rendering veloce di PyVista durante l'esportazione della vista interattiva sottostante.

Visualizzatore interattivo:

{% assign ec_vtksz = "/home/assets/images/examples/ec/ec.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ ec_vtksz }}"
  title="Interactive VTK.js view of the CLAS12 EC geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## Lista di fisica

Per impostazione predefinita viene usata `FTFP_BERT`, selezionata nel file YAML con `phys_list: FTFP_BERT`.

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
    phi: 60*deg
    delta_phi: 180*deg
```

Vedi anche la [Documentazione del generatore interno]( /home/documentation/generator/internal ) per maggiori
informazioni.

<br/>

## Digitizzazione

Le strisce scintillanti usano il plugin di digitizzazione %%ec%% specifico di CLAS12. Gli identificatori
registrano i numeri di settore, strato e striscia:

```python
gvolume.digitization = "ec"
gvolume.set_identifier("sector", sector, "layer", hipo_layer, "strip", strip)
```

<br/>

## Utilizzo

### Costruzione del rivelatore

Usa `geometry_src/ec/ec.py` per costruire il rivelatore. Per impostazione predefinita, la configurazione viene
memorizzata in un file SQLite denominato `gemc.db`.

Vedi anche [Costruzione della geometria]( /home/documentation/geometry/geometry_building ) per maggiori informazioni.

<br/>

### Esecuzione di GEMC

Il file `ec.yaml` può essere usato per eseguire la simulazione con questa configurazione. Aggiungi `-gui` per
l'esecuzione interattiva:

```shell
gemc ec.yaml -gui
```

Modifica `ec.yaml` secondo necessità, in particolare per aggiungere particelle, controllare il numero di thread
o cambiare l'output.

<br/>

## Esecuzione degli eventi

{% include figure.html
src="/assets/images/examples/ec/gemc_view.png"
caption="CLAS12 EC simulation: generated electrons showering in the electromagnetic calorimeter geometry."
%}

<br/>

## Output

L'opzione %%gstreamer%% seleziona i nomi dei file e i formati di output:

```yaml
gstreamer:
  - format: csv
    filename: ec
  - format: hipo
    filename: ec
```

Vedi anche la [Documentazione sull'output]( /home/documentation/output ) per maggiori informazioni.


## Grafici con l'analizzatore GEMC

Esegui prima GEMC con 2.000 eventi. Il file YAML predefinito scrive i flussi CSV dell'analizzatore.

```shell
gemc ec.yaml -n=2000 -no_field=all -plugin_path=/opt/projects/gemc/clas12-systems/build
```

Traccia l'energia totale depositata per hit:

```shell
gemc-analyzer ec_t0_true_info.csv totalEDeposited --kind csv --data true_info
```

![Energia totale depositata per hit nell'EC][ec-analyzer_totEdep]{:width="70%"}

[ec-analyzer_totEdep]: /home/assets/images/examples/ec/analyzer_totEdep.png

Traccia le posizioni degli hit, y in funzione di x:

```shell
gemc-analyzer ec_t0_true_info.csv --kind csv --data true_info --plot yvsx --bins 80
```

![Posizioni degli hit nell'EC, y in funzione di x][ec-analyzer_yvsx]{:width="70%"}

[ec-analyzer_yvsx]: /home/assets/images/examples/ec/analyzer_yvsx.png
