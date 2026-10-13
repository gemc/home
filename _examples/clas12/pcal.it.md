---
layout: default
title: "CLAS12 PCAL"
permalink: /examples/clas12/pcal.html
lang: it
human_reviewed: false
---

# Esempio del Calorimetro Preshower di CLAS12
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

Questo esempio mostra la geometria del Calorimetro Preshower (PCAL) di CLAS12 da `clas12-systems`.

{% assign example = site.data.examples | where: "title", "PCAL" | first %}

<br/>

## Avvio rapido

Dal repository `clas12-systems`, costruisci il database della geometria ed esegui una breve simulazione:

```shell
cd $GEMC_HOME/../clas12-systems/geometry_src/pcal
./pcal.py
gemc pcal.yaml -n=1
```

<br/>

## Geometria

La geometria, mostrata di seguito, è definita in `geometry_src/pcal/pcal.py` e `geometry_src/pcal/geometry.py`.
Il builder del PCAL legge la factory di geometria locale di coatjava, converte i settori del calorimetro
preshower di CLAS12, le finestre, gli strati di piombo, gli strati di scintillatore e i volumi delle strip U, V
e W in volumi GEMC e li memorizza in `gemc.db`.

Il mondo (un box chiamato %%root%%) contiene, per ciascuno dei sei settori:

- i volumi madre dei settori chiamati %%pcal_s1%% fino a %%pcal_s6%%
- finestre in acciaio inossidabile anteriori e posteriori chiamate %%Stainless_Steel_Front_...%% e
  %%Stainless_Steel_Back_...%%
- finestre in Last-a-Foam anteriori e posteriori chiamate %%Last-a-Foam_Front_...%% e %%Last-a-Foam_Back_...%%
- strati di piombo chiamati %%PCAL_Lead_Layer_<layer>_s<sector>%%
- i volumi madre degli strati di scintillatore U, V e W e i volumi delle strip singole/doppie

Il PCAL è una geometria di grandi dimensioni, quindi l'esempio imposta `pyvista-fast: true` in
`_data/examples.yml` per usare il percorso di rendering rapido di PyVista durante l'esportazione della vista
interattiva qui sotto.

Visualizzatore interattivo:

{% assign pcal_vtksz = "/home/assets/images/examples/pcal/pcal.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ pcal_vtksz }}"
  title="Interactive VTK.js view of the CLAS12 PCAL geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## Lista fisica

`FTFP_BERT` è usata per impostazione predefinita, selezionata nel file YAML con `phys_list: FTFP_BERT`.

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

Vedi anche la [Documentazione del Generatore Interno]( /home/documentation/generator/internal ) per maggiori
informazioni.

<br/>

## Digitalizzazione

Le strip di scintillatore usano il plugin di digitalizzazione %%ecal%% condiviso di CLAS12. Il PCAL scrive
negli stessi banchi ECAL del sistema EC, usando i layer hipo da 1 a 3. Gli identificatori registrano i numeri
di settore, layer e strip:

```python
gvolume.digitization = "ecal"
gvolume.set_identifier("sector", sector, "layer", layer, "strip", pcal_strip_id(uvw, kind, strip))
```

<br/>

## Utilizzo

### Costruzione del rivelatore

Usa `geometry_src/pcal/pcal.py` per costruire il rivelatore. Per impostazione predefinita, la configurazione
viene memorizzata in un file SQLite chiamato `gemc.db`.

Vedi anche [Costruzione della Geometria]( /home/documentation/geometry/geometry_building ) per maggiori
informazioni.

<br/>

### Esecuzione di GEMC

Il file `pcal.yaml` può essere usato per eseguire la configurazione. Aggiungi `-gui` per eseguire in modalità
interattiva:

```shell
gemc pcal.yaml -gui
```

Modifica `pcal.yaml` secondo necessità, in particolare per aggiungere particelle, controllare il numero di
thread o cambiare l'output.

<br/>

## Esecuzione degli eventi

{% include figure.html
src="/assets/images/examples/pcal/gemc_view.png"
caption="CLAS12 PCAL simulation: generated electrons crossing the preshower calorimeter geometry."
%}

<br/>

## Output

L'opzione %%gstreamer%% seleziona i nomi dei file e i formati di output:

```yaml
gstreamer:
  - format: csv
    filename: pcal
  - format: hipo
    filename: pcal
```

Vedi anche la [Documentazione dell'Output]( /home/documentation/output ) per maggiori informazioni.


## Grafici con il GEMC Analyzer

Esegui prima GEMC con 2.000 eventi. Il file YAML predefinito scrive gli stream CSV dell'analyzer.

```shell
gemc pcal.yaml -n=2000 -no_field=all -plugin_path=/opt/projects/gemc/clas12-systems/build
```

Traccia l'energia totale depositata per hit:

```shell
gemc-analyzer pcal_t0_true_info.csv totalEDeposited --kind csv --data true_info
```

![pcal total energy deposited per hit][pcal-analyzer_totEdep]{:width="70%"}

[pcal-analyzer_totEdep]: /home/assets/images/examples/pcal/analyzer_totEdep.png

Traccia le posizioni degli hit y vs x:

```shell
gemc-analyzer pcal_t0_true_info.csv --kind csv --data true_info --plot yvsx --bins 80
```

![pcal y vs x hit positions][pcal-analyzer_yvsx]{:width="70%"}

[pcal-analyzer_yvsx]: /home/assets/images/examples/pcal/analyzer_yvsx.png
