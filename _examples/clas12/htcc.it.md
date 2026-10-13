---
layout: default
title: "CLAS12 HTCC"
permalink: /examples/clas12/htcc.html
lang: it
human_reviewed: false
---

# Esempio del contatore Cherenkov ad alta soglia di CLAS12
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

Questo esempio mostra la geometria del contatore Cherenkov ad alta soglia (HTCC) di CLAS12 da `clas12-systems`.
Combina l'ottica nativa degli specchi di GEMC con mesh CAD caricate tramite la funzionalità `gcad`. Entrambi i
sistemi sono memorizzati in un unico database SQLite.

La geometria e la digitizzazione dell'HTCC sono disponibili in `clas12-systems` 0.3 con GEMC 0.5 e `pygemc` 0.5.0.

{% assign example = site.data.examples | where: "title", "HTCC" | first %}

<br/>

## Avvio rapido

Dal repository `clas12-systems`, costruisci il database della geometria ed esegui una breve simulazione:

```shell
cd $GEMC_HOME/../clas12-systems/geometry_src/htcc
./htcc.py
gemc htcc.yaml -n=1
```

<br/>

## Geometria

La geometria, mostrata di seguito, è definita in `geometry_src/htcc/geometry.py` e la sua costruzione è coordinata da
`geometry_src/htcc/htcc.py`. Le procedure di costruzione native adattano gli script Perl originali di clas12Tags
(volume del gas, finestre, 48 specchi ellittici e 48 tubi fotomoltiplicatori), mentre i tre coni della linea del
fascio sono importati come mesh CAD. Le righe dei volumi nativi usano il sistema SQLite %%htcc%% e quelle delle mesh
usano il sistema CAD separato %%htcc_cad%%. Entrambi condividono lo stesso database, la stessa variazione e lo stesso
run, quindi un unico `gemc.db` carica il rivelatore completo.

Il volume mondo (un parallelepipedo chiamato %%root%%) contiene:

- il volume del gas %%htcc%% costruito mediante operazioni booleane su policoni, più %%htccEntryWindow%% e
  %%htccExitWindow%%
- 48 segmenti di specchi ellittici ricavati da un corpo policonico e registrati con la superficie ottica
  %%htcc_AlMgF2%%
- tubi fotomoltiplicatori chiamati %%pmt_<ring>_sector<sector>_<half>%%, con lettura in due semisettori per settore
- gusci paraboloidali dei coni di Winston che condividono la superficie ottica di rivestimento %%htcc_AlMgF2%%
- coni CAD della linea del fascio (%%htccCone%%, %%htccMollerCone%%, %%htccMollerConeExt%%) collocati sotto %%root%%

Visualizzatore interattivo:

{% assign htcc_vtksz = "/home/assets/images/examples/htcc/htcc.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ htcc_vtksz }}"
  title="Interactive VTK.js view of the CLAS12 HTCC geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## Lista di fisica

L'HTCC è un rivelatore Cherenkov, quindi i fotoni ottici devono essere prodotti e tracciati. Il file YAML seleziona
`FTFP_BERT + G4OpticalPhysics` con `phys_list: FTFP_BERT + G4OpticalPhysics`.

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

I tubi fotomoltiplicatori usano il plugin di digitizzazione %%htcc%% specifico di CLAS12. Gli identificatori
registrano il settore, l'anello degli specchi e il semisettore da cui il tubo legge il segnale:

```python
pmt.digitization = "htcc"
pmt.set_identifier("sector", sector, "ring", ring, "half", hindex)
```

<br/>

## Utilizzo

### Costruzione del rivelatore

Usa `geometry_src/htcc/htcc.py` per costruire il rivelatore. Lo script definisce i materiali e le superfici degli
specchi, pubblica i volumi nativi %%htcc%% e pubblica i tre coni della linea del fascio come mesh CAD per il sistema
%%htcc_cad%%. Per impostazione predefinita, entrambi i sistemi sono memorizzati in un file SQLite chiamato `gemc.db`.

Vedi anche la [Costruzione della geometria]( /home/documentation/geometry/geometry_building ) per maggiori
informazioni.

<br/>

### Esecuzione di GEMC

Il file `htcc.yaml` può essere usato per eseguire la simulazione con questa configurazione. Aggiungi `-gui` per
eseguirla in modalità interattiva:

```shell
gemc htcc.yaml -gui
```

Modifica `htcc.yaml` secondo necessità, in particolare per aggiungere particelle, controllare il numero di thread
o cambiare l'output.

<br/>

## Esecuzione degli eventi

{% include figure.html
src="/assets/images/examples/htcc/gemc_view.png"
caption="CLAS12 HTCC simulation: generated electrons crossing the high-threshold Cherenkov counter geometry."
%}

<br/>

## Output

L'opzione %%gstreamer%% seleziona i nomi e i formati dei file di output:

```yaml
gstreamer:
  - format: csv
    filename: htcc
  - format: hipo
    filename: htcc
```

Vedi anche la [Documentazione dell'output]( /home/documentation/output ) per maggiori informazioni.


## Grafici con il GEMC Analyzer

Esegui prima GEMC con 2.000 eventi. Il file YAML predefinito scrive i flussi CSV dell'analizzatore.

```shell
gemc htcc.yaml -n=2000 -no_field=all -plugin_path=/opt/projects/gemc/clas12-systems/build
```

Traccia l'energia totale depositata per hit:

```shell
gemc-analyzer htcc_t0_true_info.csv totalEDeposited --kind csv --data true_info
```

![energia totale depositata per hit nell'htcc][htcc-analyzer_totEdep]{:width="70%"}

[htcc-analyzer_totEdep]: /home/assets/images/examples/htcc/analyzer_totEdep.png

Traccia le posizioni degli hit, y in funzione di x:

```shell
gemc-analyzer htcc_t0_true_info.csv --kind csv --data true_info --plot yvsx --bins 80
```

![posizioni degli hit nell'htcc, y in funzione di x][htcc-analyzer_yvsx]{:width="70%"}

[htcc-analyzer_yvsx]: /home/assets/images/examples/htcc/analyzer_yvsx.png
