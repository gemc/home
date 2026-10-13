---
layout: default
title: "CLAS12 FT"
permalink: /examples/clas12/ft.html
lang: it
human_reviewed: false
---

# Esempio del Forward Tagger di CLAS12
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

Questo esempio mostra la geometria del Forward Tagger (FT) di CLAS12 disponibile in `clas12-systems`. Il FT si trova a
piccoli angoli polari ed è costituito da tre sottosistemi: un calorimetro elettromagnetico, un odoscopio a
scintillatore e un tracciatore Micromegas.

La geometria e la digitizzazione del FT sono disponibili in `clas12-systems` 0.3 con GEMC 0.5 e `pygemc` 0.5.0.

{% assign example = site.data.examples | where: "title", "FT" | first %}

<br/>

## Avvio rapido

Dal repository `clas12-systems`, genera il database della geometria ed esegui una breve simulazione:

```shell
cd $GEMC_HOME/../clas12-systems/geometry_src/ft
./ft.py
gemc ft.yaml -n=1
```

<br/>

## Geometria

La geometria, mostrata di seguito, è definita in `geometry_src/ft/geometry.py` e generata da
`geometry_src/ft/ft.py`. Lo script di costruzione del FT assembla i tre sottosistemi in un unico `gemc.db`:

- il **calorimetro**, una matrice di cristalli di PbWO4, ciascuno rivestito e accoppiato a un APD, denominati
  %%ft_cal_cr_h<ih>_v<iv>%%, più i volumi dell'alloggiamento in rame, della scheda madre e della schermatura
- l'**odoscopio**, piastrelle di scintillatore denominate in base a settore, strato e componente
- il **tracciatore**, dischi Micromegas con volumi di kapton, fotoresist e anelli su ciascuno strato e lato

Il volume mondo (una scatola denominata %%root%%) contiene tutti e tre i sottosistemi. Al calorimetro e al
tracciatore vengono aggiunti rivelatori di flusso per registrare il flusso delle particelle incidenti.

Visualizzatore interattivo:

{% assign ft_vtksz = "/home/assets/images/examples/ft/ft.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ ft_vtksz }}"
  title="Interactive VTK.js view of the CLAS12 FT geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## Lista dei processi fisici

`FTFP_BERT` è utilizzata per impostazione predefinita e selezionata nel file YAML con `phys_list: FTFP_BERT`.

{% include notes/physics-list-note.md %}

<br/>

## Generatore

La cinematica delle particelle è definita nel file YAML:

```yaml
gparticle:
  - name: e-
    p: 2000*MeV
    theta: 3*deg
    phi: 10*deg
    delta_phi: 180*deg
```

Vedi anche la [Documentazione del generatore interno]( /home/documentation/generator/internal ) per maggiori
informazioni.

<br/>

## Digitizzazione

Ogni sottosistema del FT utilizza il proprio plugin di digitizzazione specifico per CLAS12. I cristalli del
calorimetro usano %%ft_cal%%, le piastrelle dell'odoscopio usano %%ft_hodo%% e i dischi del tracciatore usano
%%ft_trk%%. Gli identificatori indicano il componente da cui viene acquisito il segnale, ad esempio la riga e
la colonna del cristallo del calorimetro:

```python
digitization="ft_cal",
identifiers=("ih", ix, "iv", iy),
```

<br/>

## Utilizzo

### Costruzione del rivelatore

Usa `geometry_src/ft/ft.py` per costruire il rivelatore. Per impostazione predefinita, la configurazione viene
memorizzata in un file SQLite denominato `gemc.db`.

Vedi anche la [Costruzione della geometria]( /home/documentation/geometry/geometry_building ) per maggiori
informazioni.

<br/>

### Esecuzione di GEMC

Il file `ft.yaml` può essere usato per simulare la configurazione. Aggiungi `-gui` per eseguire in modalità
interattiva:

```shell
gemc ft.yaml -gui
```

Modifica `ft.yaml` secondo necessità, in particolare per aggiungere particelle, controllare il numero di
thread o cambiare l'output.

<br/>

## Esecuzione degli eventi

{% include figure.html
src="/assets/images/examples/ft/gemc_view.png"
caption="CLAS12 FT simulation: generated electrons crossing the forward tagger geometry."
%}

<br/>

## Output

L'opzione %%gstreamer%% seleziona i nomi dei file e i formati di output:

```yaml
gstreamer:
  - format: csv
    filename: ft
  - format: hipo
    filename: ft
```

Vedi anche la [Documentazione dell'output]( /home/documentation/output ) per maggiori informazioni.

Il forward tagger acquisisce i segnali di tre rivelatori (%%ft_cal%%, %%ft_hodo%% e %%ft_trk%%) con strutture
degli identificatori diverse. L'esempio di analisi qui sotto disabilita l'output delle informazioni di verità
(true-information) e dei dati digitizzati per i rivelatori di flusso, dell'odoscopio e del tracciatore, in modo
che il CSV contenga lo schema uniforme di %%ft_cal%%.


## Grafici con il GEMC Analyzer

Esegui prima GEMC con 2.000 eventi. Il file YAML predefinito scrive i flussi CSV dell'analizzatore.

```shell
gemc ft.yaml -n=2000 -no_field=all -plugin_path=/opt/projects/gemc/clas12-systems/build \
  -no_true_info="flux ft_hodo ft_trk" -no_digitized="flux ft_hodo ft_trk"
```

Traccia l'energia totale depositata per hit:

```shell
gemc-analyzer ft_t0_true_info.csv totalEDeposited --kind csv --data true_info
```

![energia totale depositata per hit nel FT][ft-analyzer_totEdep]{:width="70%"}

[ft-analyzer_totEdep]: /home/assets/images/examples/ft/analyzer_totEdep.png

Traccia le posizioni degli hit, y in funzione di x:

```shell
gemc-analyzer ft_t0_true_info.csv --kind csv --data true_info --plot yvsx --bins 80
```

![posizioni degli hit nel FT, y in funzione di x][ft-analyzer_yvsx]{:width="70%"}

[ft-analyzer_yvsx]: /home/assets/images/examples/ft/analyzer_yvsx.png
