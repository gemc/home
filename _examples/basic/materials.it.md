---
layout: default
title: "Materials"
permalink: /examples/basic/materials.html
lang: it
human_reviewed: false
---

# Esempio sui materiali
<hr style="height:4px;border:0;background:#4a90e2;">

<br/>

Questo esempio illustra i quattro modi per definire un materiale in GEMC: utilizzando un materiale predefinito
di Geant4, componendo un materiale a partire da elementi in base al numero di atomi, componendo un materiale a
partire da materiali esistenti in base alle frazioni di massa e aggiungendo proprietà ottiche per la
scintillazione o la radiazione Cherenkov.

<br/>

{% assign example = site.data.examples | where: "title", "Materials" | first %}
Puoi eseguire questo esempio nel tuo browser: [![{{ example.title }}]({{ example.badge }})]({{ example.binder }}){:target="_blank" rel="noopener noreferrer"} 

## Avvio rapido

Copia l'esempio nella directory corrente.
Per creare la geometria ed eseguire 10 eventi:

```shell
cp -r $GEMC_HOME/examples/basic/material .
cd material
./materials.py
gemc materials.yaml -n=10
```

<br/>

## Geometria

La geometria è definita in `materials.py`.

Il mondo (un parallelepipedo chiamato %%root%%) contiene cinque tubi identici posizionati lungo l'asse z.
Tutti i tubi hanno la stessa forma: 10 cm di diametro, 1 cm di spessore, a partire da z = 0, con una distanza
di 3 cm tra l'uno e l'altro.
Differiscono solo per colore e definizione del materiale:

| Tubo | Nome del volume | Materiale | Metodo di definizione |
|------|-------------|----------|-------------------|
| 1 | %%tube_carbon%% | %%G4_C%% | Predefinito in Geant4 (grafite) |
| 2 | %%tube_water%% | %%custom_water%% | Composizione molecolare (H2O) |
| 3 | %%tube_mixture%% | %%air_water_mixture%% | Frazioni di massa (80% aria, 20% acqua) |
| 4 | %%tube_scintillator%% | %%my_scintillator%% | Simile al NaI, con proprietà di scintillazione |
| 5 | %%tube_optical%% | %%optical_glass%% | SiO2 con indice di rifrazione |


Visualizzatore interattivo:

<iframe
  src="{{ site.baseurl }}/assets/vtkjs-viewer.html?fileURL={{ site.baseurl }}/assets/images/examples/materials/material.vtksz"
  title="Interactive VTK.js view of the materials geometry"
  width="100%"
  height="620"
  style="border:1px solid #d0d7de; border-radius:1px;"
  loading="lazy">
</iframe>

<br/>


## Definizioni dei materiali

### Tubo 1 — Materiale predefinito in Geant4

Il caso più semplice: assegna un nome dal
[Database dei materiali di Geant4](https://geant4.web.cern.ch/documentation/dev/bfad_html/ForApplicationDevelopers/Appendix/materialNames.html)
direttamente a `gvolume.material`:

```python
tube1.material = "G4_C"
```

Non è necessario alcun oggetto `GMaterial`; GEMC risolve il nome in fase di esecuzione.

<br/>

### Tubo 2 — Composizione molecolare

Usa `GMaterial` e `addNAtoms` per specificare gli atomi e il loro numero nella formula chimica:

```python
water = GMaterial("custom_water")
water.description = "Water defined by molecular composition (H2O)"
water.density = 1.0          # g/cm3
water.addNAtoms("H", 2)
water.addNAtoms("O", 1)
water.publish(cfg)
```

Il numero totale di atomi deve essere maggiore di 1.

<br/>

### Tubo 3 — Frazioni di massa

Usa `addMaterialWithFractionalMass` per miscelare materiali esistenti in base alle frazioni di massa.
La somma delle frazioni deve essere esattamente 1:

```python
mixture = GMaterial("air_water_mixture")
mixture.description = "80% air / 20% water mixture"
mixture.density = 0.9601     # g/cm3
mixture.addMaterialWithFractionalMass("G4_AIR",   0.80)
mixture.addMaterialWithFractionalMass("G4_WATER", 0.20)
mixture.publish(cfg)
```

<br/>

### Tubo 4 — Proprietà di scintillazione

Imposta `photonEnergy` e i campi di scintillazione per abilitare l'emissione di fotoni ottici.
Tutte le grandezze dipendenti dall'energia devono avere lo stesso numero di valori di `photonEnergy`:

```python
scintillator = GMaterial("my_scintillator")
scintillator.density = 3.67   # g/cm3
scintillator.addNAtoms("Na", 1)
scintillator.addNAtoms("I",  1)
scintillator.photonEnergy       = "2.0*eV 2.5*eV 3.0*eV 3.5*eV 4.0*eV"
scintillator.fastcomponent      = "1.0 0.9 0.8 0.7 0.6"
scintillator.slowcomponent      = "0.5 0.4 0.3 0.2 0.1"
scintillator.scintillationyield = 38000   # photons/MeV
scintillator.resolutionscale    = 1.0
scintillator.fasttimeconstant   = 6       # ns
scintillator.slowtimeconstant   = 88      # ns
scintillator.yieldratio         = 0.8
scintillator.birksConstant      = 0.00152
scintillator.publish(cfg)
```


<br/>

### Tubo 5 — Indice di rifrazione (Cherenkov)

Imposta `photonEnergy`, `indexOfRefraction` e, facoltativamente, `absorptionLength` per abilitare
la radiazione Cherenkov nel materiale. Si segue lo stesso approccio utilizzato nel seguente
[esempio Cherenkov](/home/examples/optical/cherenkov):

```python
optical_glass = GMaterial("optical_glass")
optical_glass.density = 2.5   # g/cm3
optical_glass.addNAtoms("Si", 1)
optical_glass.addNAtoms("O",  2)
optical_glass.photonEnergy      = "2.0*eV 3.0*eV 4.0*eV 5.0*eV"
optical_glass.indexOfRefraction = "1.458 1.466 1.476 1.490"
optical_glass.absorptionLength  = "3*m 3*m 3*m 3*m"
optical_glass.publish(cfg)
```

<br/>

## Lista di fisica

Nel file YAML è selezionata la lista `FTFP_BERT + G4OpticalPhysics` in modo che i fotoni ottici prodotti dalla
scintillazione e dalla radiazione Cherenkov vengano tracciati.

```yaml
phys_list: FTFP_BERT + G4OpticalPhysics
```

{% include notes/physics-list-note.md %}

<br/>

## Generatore

La cinematica delle particelle è definita nel file YAML:

```yaml
gparticle:
  - name: proton
    p: 2000*MeV
    vz: -2*cm
    delta_vx: 0.1*cm
    delta_vy: 0.1*cm
    multiplicity: 1
```

Vedi anche la [documentazione del generatore interno]( /home/documentation/generator/internal ) per ulteriori
informazioni.

<br/>

## Utilizzo

### Costruzione del rivelatore

```shell
./materials.py
```

Vedi anche la [costruzione della geometria]( /home/documentation/geometry/geometry_building ) per ulteriori
informazioni.

<br/>

### Esecuzione di GEMC

```shell
gemc materials.yaml -n=10
```

Le annotazioni e le decorazioni della scena sono salvate in `annotations.yaml`. Esegui solo il file YAML principale
per una vista essenziale, oppure passa entrambi i file YAML per includere le etichette e la scala di riferimento:

```shell
gemc materials.yaml -n=10
gemc materials.yaml annotations.yaml -n=10
```

Aggiungi `-gui` per l'esecuzione interattiva.

<br/>

## Esecuzione degli eventi

{% include figure.html
src="/assets/images/examples/materials/gemc_view.png"
caption="Materials simulation: particles traversing the material samples."
%}

<br/>

## Output

Nel file YAML sono configurati due flussi di output:

```yaml
gstreamer:
  - format: csv
    filename: material
```

Vedi anche la [documentazione dell'output]( /home/documentation/output ) per maggiori informazioni.
