---
layout: default
title: "CLAS12 FTOF"
permalink: /examples/clas12/ftof.html
lang: it
human_reviewed: false
---

# Esempio del Forward Time-of-Flight di CLAS12
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

Questo esempio mostra la geometria del Forward Time-of-Flight (FTOF) di CLAS12 dal repository `clas12-systems`.

{% assign example = site.data.examples | where: "title", "FTOF" | first %}

<br/>

## Avvio rapido

Dal repository `clas12-systems`, costruisci il database della geometria ed esegui una breve simulazione:

```shell
cd $GEMC_HOME/../clas12-systems/geometry_src/ftof
./ftof.py
gemc ftof.yaml -n=1
```

<br/>

## Geometria

La geometria, mostrata di seguito, è definita in `geometry_src/ftof/ftof.py` e `geometry_src/ftof/geometry.py`.
Il costruttore FTOF legge la factory locale della geometria coatjava, converte i pannelli del TOF in avanti di CLAS12
e le barre scintillatrici in volumi GEMC e li memorizza in `gemc.db`.

Il volume mondo (una scatola chiamata %%root%%) contiene, per ciascuno dei sei settori:

- tre volumi madre dei pannelli chiamati %%ftof_p1a_s<sector>%%, %%ftof_p1b_s<sector>%% e %%ftof_p2_s<sector>%%
- barre scintillatrici chiamate %%panel1a_sector<sector>_paddle_<n>%% (23 barre), %%panel1b_...%% (62) e
  %%panel2_...%% (5)
- una schermatura in piombo dietro i pannelli 1a e 2 chiamata %%ftof_shield_p1a_sector<sector>%% e
  %%ftof_shield_p2_sector<sector>%%

Visualizzatore interattivo:

{% assign ftof_vtksz = "/home/assets/images/examples/ftof/ftof.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ ftof_vtksz }}"
  title="Interactive VTK.js view of the CLAS12 FTOF geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## Lista di processi fisici

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
    delta_phi: 180*deg
```

Per approfondimenti, vedi la [documentazione del generatore interno]( /home/documentation/generator/internal ).

<br/>

## Digitizzazione

Le barre scintillatrici usano il plugin di digitizzazione %%ftof%% specifico di CLAS12. Ogni barra viene letta a
entrambe le estremità, quindi il plugin suddivide ogni hit in due canali PMT, sinistro (Left) e destro (Right).
Gli identificatori registrano settore, pannello, barra e lato del PMT:

```python
gvolume.digitization = "ftof"
gvolume.set_identifier("sector", sector, "panel", layer, "paddle", paddle, "side", 0)
```

<br/>

## Utilizzo

### Costruzione del rivelatore

Usa `geometry_src/ftof/ftof.py` per costruire il rivelatore. Per impostazione predefinita, la configurazione
viene memorizzata in un file SQLite chiamato `gemc.db`.

Per approfondimenti, vedi [Costruzione della geometria]( /home/documentation/geometry/geometry_building ).

<br/>

### Esecuzione di GEMC

Il file `ftof.yaml` può essere usato per simulare la configurazione. Aggiungi `-gui` per eseguire in modalità
interattiva:

```shell
gemc ftof.yaml -gui
```

Modifica `ftof.yaml` secondo necessità, in particolare per aggiungere particelle, controllare il numero di
thread o cambiare l'output.

<br/>

## Esecuzione degli eventi

{% include figure.html
src="/assets/images/examples/ftof/gemc_view.png"
caption="CLAS12 FTOF simulation: generated electrons crossing the forward time-of-flight geometry."
%}

<br/>

## Output

L'opzione %%gstreamer%% seleziona i nomi dei file di output e i formati:

```yaml
gstreamer:
  - format: csv
    filename: ftof
  - format: hipo
    filename: ftof
```

Vedi anche la [documentazione dell'output]( /home/documentation/output ) per ulteriori informazioni.


## Grafici con l'analizzatore GEMC

Esegui prima GEMC con 2.000 eventi. Il file YAML predefinito scrive i flussi CSV dell'analizzatore.

```shell
gemc ftof.yaml -n=2000 -no_field=all -plugin_path=/opt/projects/gemc/clas12-systems/build
```

Traccia l'energia totale depositata per hit:

```shell
gemc-analyzer ftof_t0_true_info.csv totalEDeposited --kind csv --data true_info
```

![Energia totale depositata per hit nel FTOF][ftof-analyzer_totEdep]{:width="70%"}

[ftof-analyzer_totEdep]: /home/assets/images/examples/ftof/analyzer_totEdep.png

Traccia le posizioni degli hit in y rispetto a x:

```shell
gemc-analyzer ftof_t0_true_info.csv --kind csv --data true_info --plot yvsx --bins 80
```

![Posizioni degli hit nel FTOF in y rispetto a x][ftof-analyzer_yvsx]{:width="70%"}

[ftof-analyzer_yvsx]: /home/assets/images/examples/ftof/analyzer_yvsx.png
