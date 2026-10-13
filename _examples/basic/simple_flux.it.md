---
layout: default
title: "Simple flux"
permalink: /examples/basic/simple_flux.html
lang: it
human_reviewed: false
---

# Rivelatore di flusso semplice
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

Questo esempio usa la digitizzazione %%flux%% per salvare nell'output le informazioni di verità e quelle digitizzate.

{% assign example = site.data.examples | where: "title", "Simple Flux" | first %}

Puoi eseguire questo esempio nel tuo browser: [![{{ example.title }}]({{ example.badge }})]({{ example.binder }}){:target="_blank" rel="noopener noreferrer"} 

<br/>

## Avvio rapido

Copia l'esempio nella directory corrente.
Per creare la geometria, simulare 10 eventi e produrre i file di output ROOT e CSV:

```shell
cp -r $GEMC_HOME/examples/basic/simple_flux .
cd simple_flux
./simple_flux.py
gemc simple_flux.yaml -n=10
```

<br/>

## Geometria

La geometria, mostrata di seguito, è definita in `simple_flux.py`.

Il volume mondo (un parallelepipedo chiamato %%root%%) contiene:

- %%target%%, un bersaglio cilindrico di idrogeno liquido (%%G4_lH2%%)
- %%FluxPlane%%, un parallelepipedo di aria (%%G4_AIR%%) a cui è assegnata la digitizzazione %%flux%%


Visualizzatore interattivo:

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}/assets/images/examples/simple_flux/simple_flux.vtksz"
  title="Interactive VTK.js view of the simple_flux geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>


<br/>

## Lista di fisica

Per impostazione predefinita viene usata `QBBC`, selezionata nel file YAML con `phys_list: QBBC`.

{% include notes/physics-list-note.md %}

<br/>


## Generatore

La cinematica delle particelle è definita nel file YAML:

```yaml
gparticle:
  - name: proton
    p: 2000*MeV
    vz: -3*cm
    delta_vx: 0.1*cm
    delta_vy: 0.1*cm
    multiplicity: 10
```

Consulta anche la [documentazione del generatore interno]( /home/documentation/generator/internal ) per ulteriori
informazioni.

<br/>


## Digitizzazione

La sensibilità di %%FluxPlane%% è specificata in `simple_flux.py` tramite la digitizzazione %%flux%%
(una delle routine predefinite disponibili in GEMC), con identificatore %%flux_plane = 1%%.

```python
gvolume.digitization = "flux"
gvolume.set_identifier("flux_plane", 1)
```

In questo caso, l'%%identifier%% contiene un solo nome: %%flux_plane%%.

Consulta la [documentazione di Flux]( /home/documentation/sensitivity/flux ) per ulteriori informazioni.


Oltre alle variabili digitizzate, le informazioni di verità vengono salvate nel flusso di output.

{% include notes/true_info-note.md %}


<br/>

## Utilizzo

### Costruzione del rivelatore

Usa lo script Python `simple_flux.py` per costruire il rivelatore. Per impostazione predefinita, la configurazione
è memorizzata in un file SQLite chiamato `gemc.db`. Le opzioni da riga di comando consentono di definire il tipo
di database, le varianti e il numero di run.

Consulta anche [Costruzione della geometria]( /home/documentation/geometry/geometry_building ) per ulteriori
informazioni.


<br/>

### Esecuzione di GEMC

Il file `simple_flux.yaml` può essere usato per eseguire la configurazione. Aggiungi `-gui` per avviare
l'esecuzione in modalità interattiva:

```shell
gemc simple_flux.yaml -gui
```

Modifica `simple_flux.yaml` secondo necessità, in particolare per aggiungere particelle, controllare il numero
di thread o cambiare l'output.

<br/>

## Simulazione degli eventi

{% include figure.html
src="/assets/images/examples/simple_flux/gemc_view.png"
caption="Simple flux simulation: proton tracks traversing the flux detector volumes."
%}

<br/>

## Output

L'opzione %%gstreamer%% seleziona i nomi dei file di output e il formato:

```yaml
gstreamer:
  - format: csv
    filename: simple_flux
```

Poiché %%flux%% è una digitizzazione per evento, GEMC produrrà un file di output per ciascun thread.
Per i file ROOT, puoi usare `hadd` per unire i file.


Consulta anche la [documentazione dell'output]( /home/documentation/output ) per ulteriori informazioni.


<br/>

## Creazione di grafici con GEMC Analyzer

Esegui prima GEMC con 10.000 eventi. Il file YAML predefinito scrive i flussi CSV per l'analizzatore.

```shell
gemc simple_flux.yaml -n=10000
```

Genera il grafico dell'energia totale depositata per hit:

```shell
gemc-analyzer simple_flux_t0_digitized.csv totEdep --kind csv
```

![Energia totale depositata per hit in simple_flux][simple_flux-analyzer_totEdep]{:width="70%"}

[simple_flux-analyzer_totEdep]: /home/assets/images/examples/simple_flux/analyzer_totEdep.png

Genera il grafico dell'energia vera della particella lungo la traccia:

```shell
gemc-analyzer simple_flux_t0_true_info.csv E --kind csv --data true_info
```

![Energia vera della particella lungo la traccia in simple_flux][simple_flux-analyzer_true_energy]{:width="70%"}

[simple_flux-analyzer_true_energy]: /home/assets/images/examples/simple_flux/analyzer_true_energy.png
