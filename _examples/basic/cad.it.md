---
layout: default
title: "CAD example"
permalink: /examples/basic/cad.html
lang: it
human_reviewed: false
---

# Esempio CAD
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

Questo esempio importa tre mesh STL di organi con la factory CAD di GEMC e modella un trattamento medico
di brachiterapia: una sorgente di **iridio-192** ad alto rateo di dose (HDR) viene collocata *nel fegato*
ed emette fotoni in modo isotropo. Ogni organo è un rivelatore sensibile di tipo %%flux%%, quindi l'energia
depositata viene registrata per organo; `plot_dose.py` la converte in dose assorbita e nel tempo di
irraggiamento equivalente dell'Ir-192.

<br/>

## Avvio rapido

Copia l'esempio nella directory corrente. Per caricare le definizioni CAD, eseguire 200 eventi con
output CSV e rappresentare graficamente la dose in ciascun organo:

```shell
cp -r $GEMC_HOME/examples/basic/cad .
cd cad
./cad.py
gemc cad.yaml -n=200
./plot_dose.py
```

<br/>

## Geometria

La geometria è definita in modo dichiarativo in `stls/cad__default.yaml` e caricata in `gemc.db` da
`cad.py`.

Il sistema CAD denominato %%stls%% contiene:

- %%heart_NIH3D%%, una mesh del cuore a cui è assegnato il materiale sangue.
- %%respiratory_NIH3D%%, una mesh semitrasparente dei polmoni realizzata con %%G4_LUNG_ICRP%%.
- %%liver_NIH3D%%, una mesh del fegato a cui è assegnato il materiale tessuto molle.

Ogni voce in `stls/cad__default.yaml` imposta il file della mesh, il materiale, il colore, la scala, la
posizione e l'identificatore. Il valore %%system%% deve corrispondere sia al nome `gsystem` in `cad.yaml`
sia alla directory che contiene i file STL. I tre organi sono centrati sull'asse y (ogni centroide ha
`x = z = 0`) e disposti uno sopra l'altro lungo y; la mesh dei polmoni — creata con la trachea rivolta
verso il basso — ha una `rotation` di 180° attorno a z che la porta nell'orientamento corretto.

Vedi anche la [documentazione sulle importazioni CAD](/home/documentation/geometry/cad_imports) per
maggiori informazioni.

Visualizzatore interattivo:

<iframe
  src="/home/assets/vtkjs-viewer.html?fileURL=/home/assets/images/examples/cad/cad.vtksz"
  title="Interactive VTK.js view of the CAD organ geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## Lista di fisica

Per impostazione predefinita viene usata `FTFP_BERT`, selezionata nel file YAML con
`phys_list: FTFP_BERT`.

{% include notes/physics-list-note.md %}

<br/>

## Generatore

La cinematica delle particelle è definita nel file YAML:

```yaml
gparticle:
  - name: gamma
    p: 380*keV
    delta_p: 120*keV
    multiplicity: 300
    theta: 90*deg
    delta_theta: 90*deg
    randomThetaModel: cosine
    phi: 180*deg
    delta_phi: 180*deg
    vx: 0*mm
    vy: -140*mm
    vz: 0*mm
    delta_vx: 20*mm
    delta_vy: 20*mm
    delta_vz: 20*mm
    randomVertexModel: sphere
```

Questa configurazione modella una **sorgente clinica di brachiterapia HDR all'iridio-192** inserita nel fegato:

- **Energia** — l'Ir-192 emette uno spettro a righe (righe dominanti a 0,30–0,61 MeV). Qui è approssimato
  da fotoni con energia media di ~0,38 MeV, distribuita mediante `delta_p` per coprire lo spettro.
- **Posizione** — il vertice coincide con il centroide del fegato nelle coordinate globali, `(0, -140, 0) mm`,
  con una distribuzione uniforme all'interno di una sfera di ~35 mm (`randomVertexModel: sphere` usa
  `|delta_v|` come raggio) per simulare la regione di sosta della sorgente. Gli organi sono disposti lungo
  l'asse y (`x = z = 0`) con il cuore all'origine, il fegato appena sotto e i polmoni sopra.
- **Direzione** — emissione isotropa su 4π: campionamento `cosine` di θ nell'intervallo 0–180° combinato
  con una distribuzione uniforme di φ nell'intervallo 0–360°.

Vedi anche la [documentazione sul generatore interno](/home/documentation/generator/internal) per
maggiori informazioni.

<br/>

## Digitalizzazione

Ogni organo è configurato come rivelatore sensibile di tipo %%flux%% in `stls/cad__default.yaml`:

```yaml
defaults:
  digitization: flux

volumes:
  - name: heart_NIH3D
    identifier: "organ: 1"
```

La digitalizzazione %%flux%% corrisponde a un rivelatore in **modalità evento**: scrive una riga di output
per ogni hit, contenente l'%%identifier%% dell'organo e l'energia depositata %%totEdep%%. Questo consente
a una singola esecuzione di distinguere i tre organi.

> La digitalizzazione integrata %%dosimeter%% calcolerebbe anch'essa la dose, ma corrisponde a un rivelatore
> in **modalità run** che accumula tutti gli hit con lo stesso nome di rivelatore sensibile in un unico
> record contenente la somma. Poiché tutti e tre gli organi condividono il nome `dosimeter`, i loro dati
> verrebbero aggregati in un unico valore. L'uso di %%flux%% mantiene l'identità
> dell'organo per ogni hit.

### Dose assorbita

`plot_dose.py` somma l'energia depositata per organo e la divide per la massa dell'organo per ottenere
la dose assorbita:

$$
D_{\text{organ}} = \frac{\sum_i \mathrm{totEdep}_i}{m_{\text{organ}}},
\qquad
m_{\text{organ}} = \rho \, V_{\text{mesh}}
$$

dove la somma è estesa agli hit dell'organo, \\(\rho\\) è la densità del materiale assegnato
(`gemc cad.yaml -printSystemsMaterials` riporta 1,06, 1,04 e 1,03 g/cm³ per i materiali sangue, polmone e
tessuto molle) e \\(V_{\text{mesh}}\\) è il volume della mesh CAD (volume con segno originale × il cubo
del fattore di scala uniforme `scale`). Un gray è un joule per chilogrammo, \\(1\,\mathrm{Gy} = 1\,\mathrm{J/kg}\\).

### Tempo di irraggiamento

La simulazione emette un numero fisso di fotoni; il corrispondente **tempo di irraggiamento reale** è il
tempo che una sorgente Ir-192 di attività \\(A\\) impiega per emettere quel numero di fotoni. Con una
resa fotonica \\(Y\\) (fotoni per decadimento), la sorgente emette \\(R = A\,Y\\) fotoni al secondo, quindi per
\\(N_\gamma = N_{\text{events}} \times m\\) fotoni simulati (molteplicità \\(m\\)):

$$
R = A \, Y,
\qquad
t_{\text{rad}} = \frac{N_\gamma}{A \, Y}
$$

`plot_dose.py` usa per impostazione predefinita una sorgente HDR nominale, \\(A = 10\ \mathrm{Ci} = 3.7\times10^{11}\\)
Bq, e \\(Y = 2.3\\) fotoni per decadimento dell'Ir-192 (la somma delle intensità delle righe gamma);
entrambi i valori sono regolabili con `--activity` e `--yield`. Poiché la dose e \\(t_{\text{rad}}\\) variano
entrambi linearmente con \\(N_\gamma\\), la dose assorbita per unità di tempo di trattamento (il rateo di dose)
è \\(D_{\text{organ}} / t_{\text{rad}}\\), e una dose terapeutica completa si raggiunge aumentando il
numero di fotoni (equivalentemente, il tempo di sosta della sorgente).

Vedi la [documentazione sul dosimetro](/home/documentation/sensitivity/dosimeter) per maggiori informazioni.

<br/>

## Utilizzo

### Costruzione del rivelatore

Usa lo script Python `cad.py` per caricare le definizioni CAD. Lo script legge
`stls/cad__default.yaml` e salva la configurazione in un file SQLite denominato `gemc.db`.

```shell
./cad.py
```

{% include notes/python-api-note.md %}

Vedi anche la [documentazione sulla costruzione della geometria](/home/documentation/geometry/geometry_building) per
maggiori informazioni.

<br/>

### Esecuzione di GEMC

Il file `cad.yaml` può essere usato per eseguire la configurazione. Aggiungi `-gui` per eseguire in
modalità interattiva:

```shell
gemc cad.yaml -gui
```

Modifica `cad.yaml` secondo necessità, in particolare per aggiungere particelle, controllare il numero
di thread o cambiare l'output.

<br/>

## Esecuzione degli eventi

{% include figure.html
src="/assets/images/examples/cad/gemc_view.png"
caption="CAD simulation: an Iridium-192 brachytherapy source inside the liver emits photons
isotropically, depositing dose in the imported liver, heart, and lung meshes."
%}

<br/>

## Output

L'opzione %%gstreamer%% seleziona il nome e il formato del file di output:

```yaml
gstreamer:
  - format: csv
    filename: organs
```

{% include notes/output-note.md %}

Vedi anche la [documentazione sull'output](/home/documentation/output) per maggiori informazioni.

<br/>

## Grafico della dose in ciascun organo

Esegui prima GEMC in modo che vengano scritti i flussi CSV di flux (più eventi migliorano la precisione
statistica per gli organi a rischio):

```shell
gemc cad.yaml -n=200
```

Poi rappresenta graficamente la dose per organo con `plot_dose.py`. Lo script legge `organs_t0_digitized.csv`,
stampa l'energia depositata, la massa e la dose per organo e disegna il grafico a barre:

```shell
./plot_dose.py                       # nominal 10 Ci Ir-192 source
./plot_dose.py --activity 5          # a weaker 5 Ci source (rescales the irradiation time)
./plot_dose.py --save organs_dose.png
```

![Dose CAD per organo][cad-dose_per_organ]{:width="70%"}

Il fegato, che ospita la sorgente, assorbe di gran lunga la dose maggiore; il cuore appena sopra e i
polmoni in cima ricevono una dose molto inferiore dovuta alla radiazione diffusa — una localizzazione
che rende vantaggiosa la brachiterapia. Il titolo riporta il tempo di irraggiamento dell'Ir-192
rappresentato dal numero di fotoni simulati (vedi [Tempo di irraggiamento](#irradiation-time) sopra).

[cad-dose_per_organ]: /home/assets/images/examples/cad/dose_per_organ.png


## Grafici con l'Analyzer di GEMC

Esegui prima GEMC con 200 eventi. Il file YAML predefinito scrive i flussi CSV per l'analyzer.

```shell
gemc cad.yaml -n=200
```

Rappresenta graficamente l'energia totale depositata per hit:

```shell
gemc-analyzer organs_t0_digitized.csv totEdep --kind csv
```

![Energia totale depositata per hit nel CAD][cad-analyzer_totEdep]{:width="70%"}

[cad-analyzer_totEdep]: /home/assets/images/examples/cad/analyzer_totEdep.png
