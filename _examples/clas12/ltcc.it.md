---
layout: default
title: "CLAS12 LTCC"
permalink: /examples/clas12/ltcc.html
lang: it
human_reviewed: false
---

# Esempio di contatore Cherenkov a bassa soglia di CLAS12
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

Questo esempio mostra la geometria del contatore Cherenkov a bassa soglia (LTCC) di CLAS12 disponibile in
`clas12-systems`. Combina l'ottica nativa degli specchi di GEMC con mesh CAD caricate tramite la funzionalità
`gcad`. Entrambi i sistemi sono memorizzati in un unico database SQLite.

La geometria e la digitizzazione dell'LTCC sono disponibili in `clas12-systems` 0.3 con GEMC 0.5 e `pygemc` 0.5.0.

{% assign example = site.data.examples | where: "title", "LTCC" | first %}

<br/>

## Avvio rapido

Dal repository `clas12-systems`, genera il database della geometria ed esegui una breve simulazione:

```shell
cd $GEMC_HOME/../clas12-systems/geometry_src/ltcc
./ltcc.py
gemc ltcc.yaml -n=1
```

<br/>

## Geometria

La geometria, mostrata di seguito, è definita in `geometry_src/ltcc/geometry.py` e orchestrata da
`geometry_src/ltcc/ltcc.py`. I costruttori nativi sono un porting degli script Perl originali di clas12Tags
(forme degli specchi, PMT e schermature in ferro), mentre i coni Winston riflettenti e il telaio meccanico
sono importati come mesh CAD. Le righe dei volumi nativi usano il sistema SQLite %%ltcc%% e le righe delle
mesh usano il sistema CAD separato %%ltcc_cad%%. Entrambi condividono lo stesso database, la stessa variante
e lo stesso run, quindi un unico `gemc.db` carica il rivelatore completo.

Il volume mondo (un parallelepipedo chiamato %%root%%) contiene, per ciascuno dei sei settori:

- un volume madre a cuneo riempito di gas chiamato %%ltccS<sector>%% che contiene l'ottica di quel settore
- segmenti di specchio cilindrici, iperbolici ed ellittici definiti con la superficie ottica %%ltcc_AlMgF2%%
- tubi fotomoltiplicatori chiamati %%pmt_s<sector><side>_<n>%%, con lettura a sinistra e a destra di ciascun segmento
- schermature in ferro da 5 mm che coprono la faccia esterna dei coni Winston
- coni Winston CAD (%%WC_S%%, %%WC_M%%, %%WC_L%%) e mesh del telaio riutilizzate come posizionamenti %%copyOf%%

Visualizzatore interattivo:

{% assign ltcc_vtksz = "/home/assets/images/examples/ltcc/ltcc.vtksz" %}

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ ltcc_vtksz }}"
  title="Interactive VTK.js view of the CLAS12 LTCC geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## Lista di fisica

L'LTCC è un rivelatore Cherenkov, quindi i fotoni ottici devono essere prodotti e tracciati. Il file YAML
seleziona `FTFP_BERT + G4OpticalPhysics` con `phys_list: FTFP_BERT + G4OpticalPhysics`.

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

Vedi anche la [Documentazione del generatore interno]( /home/documentation/generator/internal ) per altri dettagli.

<br/>

## Digitizzazione

I tubi fotomoltiplicatori usano il plugin di digitizzazione %%ltcc%% specifico di CLAS12. Gli identificatori
registrano il settore, il lato del PMT e il segmento di specchio da cui il tubo raccoglie il segnale:

```python
pmt.digitization = "ltcc"
pmt.set_identifier("sector", sector, "side", side_id, "segment", n)
```

<br/>

## Utilizzo

### Costruzione del rivelatore

Usa `geometry_src/ltcc/ltcc.py` per costruire il rivelatore. Lo script definisce i materiali e le superfici
degli specchi, pubblica i volumi nativi %%ltcc%%, carica le definizioni CAD per il sistema %%ltcc_cad%% da
`stls/cad__default.yaml` e aggiunge i posizionamenti CAD `copyOf`. Per impostazione predefinita, entrambi i
sistemi sono memorizzati in un file SQLite chiamato `gemc.db`.

Vedi anche la [Costruzione della geometria]( /home/documentation/geometry/geometry_building ) per altri dettagli.

<br/>

### Esecuzione di GEMC

Il file `ltcc.yaml` può essere usato per eseguire la simulazione con questa configurazione. Aggiungi `-gui`
per l'esecuzione interattiva:

```shell
gemc ltcc.yaml -gui
```

Modifica `ltcc.yaml` secondo necessità, in particolare per aggiungere particelle, controllare il numero di
thread o cambiare l'output.

<br/>

## Esecuzione degli eventi

{% include figure.html
src="/assets/images/examples/ltcc/gemc_view.png"
caption="CLAS12 LTCC simulation: generated electrons crossing the low-threshold Cherenkov counter geometry."
%}

<br/>

## Output

L'opzione %%gstreamer%% seleziona i nomi dei file di output e i formati:

```yaml
gstreamer:
  - format: csv
    filename: ltcc
  - format: hipo
    filename: ltcc
```

Vedi anche la [Documentazione dell'output]( /home/documentation/output ) per maggiori informazioni.


## Creazione di grafici con l'analizzatore GEMC

Esegui prima GEMC con 2.000 eventi. Il file YAML predefinito scrive i flussi CSV dell'analizzatore.

```shell
gemc ltcc.yaml -n=2000 -no_field=all -plugin_path=/opt/projects/gemc/clas12-systems/build
```

Traccia l'energia totale depositata per hit:

```shell
gemc-analyzer ltcc_t0_true_info.csv totalEDeposited --kind csv --data true_info
```

![Energia totale depositata per hit nell'LTCC][ltcc-analyzer_totEdep]{:width="70%"}

[ltcc-analyzer_totEdep]: /home/assets/images/examples/ltcc/analyzer_totEdep.png

Traccia le posizioni degli hit, y in funzione di x:

```shell
gemc-analyzer ltcc_t0_true_info.csv --kind csv --data true_info --plot yvsx --bins 80
```

![Posizioni degli hit nell'LTCC, y in funzione di x][ltcc-analyzer_yvsx]{:width="70%"}

[ltcc-analyzer_yvsx]: /home/assets/images/examples/ltcc/analyzer_yvsx.png
