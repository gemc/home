---
layout: default
title: "Scintillator Barrel"
permalink: /examples/basic/scintillator_barrel.html
lang: it
human_reviewed: false
---

# Barile di scintillatori
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

Questo esempio costruisce un rivelatore cilindrico a barile composto da 48 barre di scintillatore
trapezoidali disposte in un anello completo. Illustra l'API `distribute_on_circle` per replicare un
volume a intervalli angolari uniformi lungo una circonferenza e mostra come dimensionare le barre affinché
le facce adiacenti siano quasi contigue.


{% assign example = site.data.examples | where: "title", "Scintillator Barrel" | first %}
Puoi eseguire questo esempio nel browser: [![{{ example.title }}]({{ example.badge }})]({{ example.binder }}){:target="_blank" rel="noopener noreferrer"} 

<br/>

## Avvio rapido

Copia l'esempio nella directory corrente.
Per creare la geometria ed eseguire 3 eventi:

```shell
cp -r $GEMC_HOME/examples/basic/scintillator_barrel .
cd scintillator_barrel
./scintillator_barrel.py
gemc scintillator_barrel.yaml
```

<br/>

## Geometria

La geometria è definita in `scintillator_barrel.py`. Il volume mondo (una scatola chiamata %%root%%) contiene
48 volumi %%paddle%% identici disposti in un anello:

- Ogni %%paddle%% è un trapezoide generale `G4Trap` (%%G4_PLASTIC_SC_VINYLTOLUENE%%) con la
  faccia più larga rivolta radialmente verso l'esterno e quella più stretta verso l'asse del fascio.
- Le barre sono dimensionate con la formula della corda affinché le facce esterne adiacenti siano contigue:
  - semilarghezza esterna: `pX  = (radius + pY) × sin(π/n)`
  - semilarghezza interna: `pLTX = (radius − pY) × sin(π/n)`
- `distribute_on_circle(n=48, radius=400 mm, align=True, axis='z')` posiziona e ruota ogni
  copia attorno all'asse z a intervalli uniformi di 7,5°.

Consulta la documentazione [Funzioni di supporto per le strutture](/home/documentation/geometry/structure)
per il riferimento completo dell'API `distribute_on_circle` e la geometria usata per il dimensionamento.

Visualizzatore interattivo (barile completo con 48 barre):

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}/assets/images/examples/scintillator_barrel/scintillator_barrel.vtksz"
  title="Interactive VTK.js view of the scintillator_barrel geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>

## Lista di fisica

`QBBC` è usata per impostazione predefinita ed è selezionata nel file YAML con `phys_list: QBBC`.

{% include notes/physics-list-note.md %}

<br/>

## Generatore

La cinematica delle particelle è definita nel file YAML:

```yaml
gparticle:
  - name: proton
    p: 500*MeV
    theta: 90*deg
    delta_phi: 360*deg
    multiplicity: 3
```

Consulta anche la [Documentazione del generatore interno]( /home/documentation/generator/internal )
per maggiori informazioni.

<br/>

## Digitizzazione

A ogni %%paddle%% è assegnata la digitizzazione %%flux%% con un identificatore univoco della barra:

```python
paddle.digitization = "flux"
# ...
v.set_identifier("paddle", i)
```

Consulta la [Documentazione di Flux]( /home/documentation/sensitivity/flux ) per maggiori informazioni.

<br/>

## L'API `distribute_on_circle`

Il metodo `distribute_on_circle` di `GVolume` replica il volume modello `n` volte
lungo una circonferenza di raggio `radius`. Con `align=True`, ogni copia viene inoltre ruotata
attorno all'asse scelto di un angolo pari alla sua posizione angolare φᵢ, mantenendo il sistema di riferimento
locale di ogni barra allineato radialmente:

```python
for i, v in enumerate(paddle.distribute_on_circle(n, radius, align=True, axis='z')):
    v.set_identifier("paddle", i)
    v.publish(cfg)
```

Il metodo restituisce una lista di copie indipendenti di `GVolume`, una per ogni passo angolare, ciascuna chiamata
`<name>_i` e posizionata in `(radius·cos φᵢ, radius·sin φᵢ, 0)`.
Il riferimento completo dell'API è nella documentazione
[Funzioni di supporto per le strutture](/home/documentation/geometry/structure).

<br/>

## Utilizzo

### Costruzione del rivelatore

Usa lo script Python `scintillator_barrel.py` per costruire il rivelatore. Per impostazione predefinita,
la configurazione è memorizzata in un file SQLite chiamato `gemc.db`. Le opzioni da riga di comando permettono
di definire il tipo di database, le varianti e il numero di run.

Consulta anche [Costruzione della geometria]( /home/documentation/geometry/geometry_building )
per maggiori informazioni.

<br/>

### Esecuzione di GEMC

Il file `scintillator_barrel.yaml` esegue la simulazione. Aggiungi `-gui` per eseguirla in modo interattivo:

```shell
gemc scintillator_barrel.yaml -gui
```

Modifica `scintillator_barrel.yaml` secondo necessità, in particolare per cambiare il numero di eventi,
aggiungere thread o selezionare i formati di output.

<br/>

## Esecuzione degli eventi

La vista qui sotto mostra il barile lungo il suo asse dopo un evento, con 3 protoni emessi radialmente
verso l'esterno a θ = 90°. Ogni protone attraversa una barra di scintillatore.

{% include figure.html
src="/assets/images/examples/scintillator_barrel/gemc_view.png"
caption="Scintillator barrel viewed end-on along the beam axis. Three protons at θ = 90°
travel radially outward, each depositing energy in one paddle."
%}

<br/>

## Output

L'opzione %%gstreamer%% seleziona i nomi dei file di output e il formato:

```yaml
gstreamer:
  - format: csv
    filename: barrel
```

Consulta anche la [Documentazione dell'output]( /home/documentation/output ) per maggiori informazioni.

<br/>

## Grafici con l'analizzatore GEMC

Esegui prima GEMC con 1.000 eventi. Il file YAML predefinito scrive i flussi CSV per l'analizzatore.

```shell
gemc scintillator_barrel.yaml -n=1000
```

Traccia il grafico dell'energia totale depositata per hit:

```shell
gemc-analyzer barrel_t0_digitized.csv totEdep --kind csv
```

![scintillator_barrel: energia totale depositata per hit][scintillator_barrel-analyzer_totEdep]{:width="70%"}

[scintillator_barrel-analyzer_totEdep]: /home/assets/images/examples/scintillator_barrel/analyzer_totEdep.png

Traccia il grafico dell'energia vera della traccia della particella:

```shell
gemc-analyzer barrel_t0_true_info.csv E --kind csv --data true_info
```

![scintillator_barrel: energia vera della traccia della particella][scintillator_barrel-analyzer_true_energy]{:width="70%"}

[scintillator_barrel-analyzer_true_energy]: /home/assets/images/examples/scintillator_barrel/analyzer_true_energy.png
