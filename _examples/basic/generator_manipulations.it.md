---
layout: default
title: "Generator manipulations"
permalink: /examples/basic/generator_manipulations.html
lang: it
human_reviewed: false
---

# Manipolazioni del generatore
<hr style="height:4px;border:0;background:#4a90e2;">

Usa GEMC 0.5 o versioni successive per questi esempi.
Consulta la [guida all'installazione]({{ site.baseurl }}/installation/) per l'eseguibile e l'ambiente Python.

Undici steering card indipendenti isolano lo smearing del vertice, gli angoli fissi e il campionamento angolare.
Ciascuna genera un geantino da 1 GeV all'interno dello stesso piccolo bersaglio tubolare per rappresentare un
evento sul bersaglio. I grafici seguenti provengono da nuove simulazioni:
5.000 lanci per card, verificati confrontandoli con i record delle particelle generate prima di creare i grafici.
Ogni caso include inoltre una propria vista GEMC di 100 eventi.

{% assign source = "https://github.com/gemc/src/tree/main/examples/basic/generator_manipulations" %}
{% assign source_files = source | replace: "/tree/", "/blob/" %}
{% assign cases = site.data.generator_cases %}

[Esplora l'esempio sorgente]({{ source }}), inclusi la geometria, le card YAML complete e i controlli automatici.

## Avvio rapido

Copia l'esempio dalla tua installazione di GEMC e genera la sua geometria ASCII:

```shell
cp -r "$GEMC_HOME/examples/basic/generator_manipulations" .
cd generator_manipulations
python generator_manipulations.py -f ascii
gemc uniform_z.yaml -gui
```

Genera gli eventi con il controllo beam-on della GUI, poi apri l'Analyzer. Le card di smearing XY preparano un
unico grafico 2D di Y in funzione di X. Lo smearing Z e gli angoli fissi preparano tre istogrammi; le altre card
preparano quattro grafici.
Tutte le card abilitano l'accumulo tra le chiamate beam-on. Qt Charts è necessario per l'Analyzer della GUI.
Esegui una qualsiasi card senza %%-gui%% per produrre invece un campione CSV di 5.000 eventi con seed fissato:

```shell
gemc uniform_z.yaml
```

Ogni card ha il proprio prefisso di output. Per esempio, %%uniform_z%% produce i flussi CSV delle particelle
generate e delle informazioni di verità usati per verificare che il bersaglio registri esattamente i vertici
generati.

## Geometria e grandezze registrate

Il volume mondo in vuoto contiene un tubo di idrogeno liquido, centrato nell'origine, con raggio 25 mm e lunghezza
totale 40 mm, visualizzato con opacità del 20% per mantenere visibili le traiettorie attraverso il bersaglio.
La sua sensibilità %%flux%% registra le particelle che hanno origine al suo interno. Lo smearing rappresenta i
vertici di produzione degli eventi sul bersaglio.
I geantini non subiscono scattering né creano particelle secondarie; %%recordZeroEdep: true%% conserva i loro hit
sul bersaglio. Questo produce un hit per particella lanciata in queste configurazioni.

{% include figure.html
src="/assets/images/examples/generator_manipulations/gemc_view.png"
alt="Geantinos originating at smeared vertices inside the transparent cylindrical target"
caption="The shared tube target with 100 events from the uniform-Z card, rendered by GEMC."
%}

{% assign vtk = "/assets/images/examples/generator_manipulations/generator_manipulations.vtksz" %}
<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}{{ vtk }}"
  title="Interactive view of the tube target"
  width="100%" height="420" loading="lazy"
  style="border:1px solid #d0d7de;">
</iframe>

I grafici dei vertici usano %%vx%%, %%vy%% e %%vz%% dalle informazioni di verità del bersaglio, in mm. Questi sono i
vertici originali delle tracce. I campi %%avgx%%, %%avgy%% e %%avgz%% descrivono invece le posizioni all'interno del
bersaglio. I grafici angolari usano le componenti conservate della quantità di moto %%px%%, %%py%% e %%pz%%,
in MeV/c.

Le figure del sito web usano le funzioni di tracciamento dei grafici dell'Analyzer di `pygemc` con le variabili e
la disposizione definiti nel blocco %%ganalysis%% di ciascuna card. Sono grafici offline degli stessi campi di
dati mostrati nella GUI. Le figure di smearing Z del sito web dispongono X e Y sopra un istogramma Z che occupa
entrambe le colonne; la figura ad angoli fissi usa una riga di tre istogrammi. La GUI usa la propria disposizione
a pannello singolo o a quattro riquadri.

## Casi dei vertici

Le card di smearing usano il centro spostato (2, -3, 0) mm per mostrare che gli scostamenti casuali vengono
aggiunti alla posizione nominale. Lo smearing Z usa theta = 90 gradi; gli smearing XY e sferico usano
theta = 45 gradi.
Tutte le card di smearing del vertice usano phi = 90 gradi.
Gli smearing XY uniforme e gaussiano variano entrambe le coordinate trasversali in modo indipendente e
visualizzano mappe 2D di Y in funzione di X. Card separate per lo smearing Z uniforme e gaussiano isolano la
dispersione longitudinale.

- %%uniform%%: ogni %%delta_vx%%, %%delta_vy%% o %%delta_vz%% diverso da zero è una semiampiezza attorno al
  proprio centro.
- %%gaussian%%: ogni delta è una deviazione standard. Le finestre dei grafici monodimensionali mostrano cinque
  sigma; questi limiti di visualizzazione non troncano la generazione. Lo smearing Z gaussiano usa sigma = 3 mm,
  quindi la semilunghezza del bersaglio comprende più di sei sigma. Le code gaussiane sono illimitate; si verifica
  che i campioni con seed fissato siano contenuti nel bersaglio.
- %%sphere%%: i punti sono distribuiti uniformemente in tutto il volume di una sfera di raggio
  %%sqrt(delta_vx^2 + delta_vy^2 + delta_vz^2)%%. Dispersioni di (1, 2, 2) mm danno un raggio di 3 mm, anziché
  tre assi di un ellissoide. Le proiezioni sulle coordinate sono paraboliche e la CDF radiale è %%(r/R)^3%%.

{% assign vertex_cases = cases | where: "group", "Vertices" %}
{% for case in vertex_cases %}
### {{ case.title }}

{{ case.expected }}

[File completo {{ case.name }}.yaml]({{ source_files }}/{{ case.name }}.yaml)

<details markdown="1">
<summary>Impostazioni della particella</summary>

{% highlight yaml %}{{ case.particle }}{% endhighlight %}

</details>

{% capture event_caption %}GEMC: {{ case.view_events }} eventi per {{ case.title }}.{% endcapture %}
{% include figure.html src=case.event_image alt=case.title caption=event_caption link=case.event_image %}
{% include figure.html src=case.image alt=case.title caption=case.expected link=case.image %}
{% endfor %}

## Casi angolari

Le card angolari fissano il vertice al centro del bersaglio, (0, 0, 0) mm. %%randomThetaModel%% supporta %%uniform%%,
%%gaussian%% e %%cosine%%.
Per %%uniform%%, %%delta_theta%% è una semiampiezza; per %%gaussian%% è una deviazione standard.
Il modello %%cosine%% è uniforme in cos(theta) nell'intervallo theta +/- delta_theta, con una densità proporzionale
a sin(theta), limitata a [0, 180] gradi.
Le card di smearing di theta usano %%delta_theta: 20*deg%% e theta nominale = 2 gradi. Il campionamento uniforme
copre [-18, 22] gradi; il campionamento gaussiano ha media 2 gradi e sigma 20 gradi. Un theta negativo inverte la
quantità di moto trasversale: l'angolo polare ricostruito è non negativo, con l'azimut spostato di 180 gradi.
Il campionamento secondo il modello coseno copre [0, 22] gradi perché le estrazioni sono limitate agli angoli
polari fisici.
Phi usa sempre il campionamento uniforme con semiampiezza %%delta_phi%%; non esiste un %%randomPhiModel%%.

Per una quantità di moto p, le componenti attese sono:

```text
px = p sin(theta) cos(phi)
py = p sin(theta) sin(phi)
pz = p cos(theta)
```

La card con theta e phi fissi imposta i due angoli rispettivamente a 3 e 45 gradi e mostra solo i tre
istogrammi della quantità di moto. I casi con theta uniforme, gaussiano e secondo il modello coseno mostrano
%%px%% sull'asse verticale e %%pz%% sull'asse orizzontale nei grafici 2D. Il caso con theta secondo il modello
coseno produce anche una distribuzione uniforme di %%pz%%. Theta fisso con una dispersione di phi traccia un arco
nella proiezione %%px%%/%%py%%. Il caso di wraparound attraversa 360 gradi senza discontinuità nella quantità di moto.
Gli angoli del banco delle particelle generate sono memorizzati in radianti; le steering card usano gradi espliciti.

{% assign angular_cases = cases | where: "group", "Angles" %}
{% for case in angular_cases %}
### {{ case.title }}

{{ case.expected }}

[File completo {{ case.name }}.yaml]({{ source_files }}/{{ case.name }}.yaml)

<details markdown="1">
<summary>Impostazioni della particella</summary>

{% highlight yaml %}{{ case.particle }}{% endhighlight %}

</details>

{% capture event_caption %}GEMC: {{ case.view_events }} eventi per {{ case.title }}.{% endcapture %}
{% include figure.html src=case.event_image alt=case.title caption=event_caption link=case.event_image %}
{% include figure.html src=case.image alt=case.title caption=case.expected link=case.image %}
{% endfor %}

## Verifica e riproduzione

Da un albero dei sorgenti GEMC configurato, esegui tutti gli 11 controlli:

```shell
meson test -C build --suite generator_manipulations --print-errorlogs
```

I controlli richiedono che ogni vertice sia all'interno del bersaglio e che ci sia un hit sul bersaglio per lancio.
Verificano la corrispondenza degli ID degli eventi e dei vertici, confrontano le componenti della quantità di moto,
ricostruiscono theta e phi modulo 360 gradi e verificano le distribuzioni di probabilità attese.
I controlli XY verificano anche che i campioni trasversali siano non correlati. I test generano nuovi dati di
geometria e output in directory temporanee, quindi ogni caso funziona anche singolarmente.

Per rigenerare le immagini e le impostazioni delle particelle di questa pagina dal repository del sito web:

```shell
python3 scripts/generate_example_assets.py generator_manipulations
```

La [guida agli asset]({{ site.baseurl }}/assets/assets.md) del sito web documenta gli ambienti locali richiesti.
Vedi anche la [guida al generatore interno]({{ site.baseurl }}/documentation/generator/internal).
