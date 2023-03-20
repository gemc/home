---
layout: default
title: Geant4 Physics
description: Explore and select Geant4 Physics modules
order: 40
---

The Geant4 Physics is determined with the option **physicsList**. By default, gemc uses **FTFP_BERT** .

<br/>
### Usage:

<br/>
In the jcard, add this line to select the desired physics:
 ```
"physicsList": "your choice of physics"
```  
 The option can be composed by: 

- The main geant4 module (mandatory field). For example: **QGSP_BIC** 
- Optional: a replacement for the default electro-magnetic physics list, specified by adding its code
- Optional: physics constructor(s) can be added using the **+** sign

<br/>
### Examples:
<br/>
 - "**QGSP_BIC_EMX**" will use the **QGSP_BIC** module but replace its e.m. physics with the **G4EmStandardPhysics_option2**
 - "**FTFP_BERT_HP + G4OpticalPhysics**" will use the **FTFP_BERT_HP** module and add **G4OpticalPhysics** on top of it
 - "**QGSP_BIC_PEN + G4OpticalPhysics + G4RadioactiveDecayPhysics**" will use the **QGSP_BIC** module,    replace its e.m. physics with the **G4EmPenelopePhysics**, and add G4OpticalPhysics and G4RadioactiveDecayPhysics

<br/>
### Geant4 Version Name: geant4-11-00-patch-03 [MT]  (16-September-2022)

<br/>
#### Modules:
 - FTFP_BERT
 - FTFP_BERT_ATL
 - FTFP_BERT_HP
 - FTFP_BERT_TRV
 - FTFP_INCLXX
 - FTFP_INCLXX_HP
 - FTFQGSP_BERT
 - FTF_BIC
 - G4GenericPhysicsList
 - LBE
 - NuBeam
 - QBBC
 - QGSP_BERT
 - QGSP_BERT_HP
 - QGSP_BIC
 - QGSP_BIC_AllHP
 - QGSP_BIC_HP
 - QGSP_FTFP_BERT
 - QGSP_INCLXX
 - QGSP_INCLXX_HP
 - QGS_BIC
 - Shielding
 - ShieldingLEND
 - ShieldingM

<br/>
##### E.m. replacement codes:
 - _EM0: G4EmStandardPhysics
 - _EMV: G4EmStandardPhysics_option1
 - _EMX: G4EmStandardPhysics_option2
 - _EMY: G4EmStandardPhysics_option3
 - _EMZ: G4EmStandardPhysics_option4
 - _GS: G4EmStandardPhysicsGS
 - _LE: G4EmLowEPPhysics
 - _LIV: G4EmLivermorePhysics
 - _PEN: G4EmPenelopePhysics
 - _SS: G4EmStandardPhysicsSS
 - _WVI: G4EmStandardPhysicsWVI

<br/><br/>
##### Physics Constructors:
 - G4ChargeExchangePhysics
 - G4DecayPhysics
 - G4EmDNAChemistry
 - G4EmDNAChemistry_option1
 - G4EmDNAChemistry_option2
 - G4EmDNAChemistry_option3
 - G4EmDNAPhysics
 - G4EmDNAPhysics_option1
 - G4EmDNAPhysics_option2
 - G4EmDNAPhysics_option3
 - G4EmDNAPhysics_option4
 - G4EmDNAPhysics_option5
 - G4EmDNAPhysics_option6
 - G4EmDNAPhysics_option7
 - G4EmDNAPhysics_option8
 - G4EmDNAPhysics_stationary
 - G4EmDNAPhysics_stationary_option2
 - G4EmDNAPhysics_stationary_option4
 - G4EmDNAPhysics_stationary_option6
 - G4EmExtraPhysics
 - G4EmLivermorePhysics
 - G4EmLivermorePolarizedPhysics
 - G4EmLowEPPhysics
 - G4EmPenelopePhysics
 - G4EmStandardPhysics
 - G4EmStandardPhysicsGS
 - G4EmStandardPhysicsSS
 - G4EmStandardPhysicsWVI
 - G4EmStandardPhysics_option1
 - G4EmStandardPhysics_option2
 - G4EmStandardPhysics_option3
 - G4EmStandardPhysics_option4
 - G4FastSimulationPhysics
 - G4GenericBiasingPhysics
 - G4HadronDElasticPhysics
 - G4HadronElasticPhysics
 - G4HadronElasticPhysicsHP
 - G4HadronElasticPhysicsLEND
 - G4HadronElasticPhysicsPHP
 - G4HadronElasticPhysicsXS
 - G4HadronHElasticPhysics
 - G4HadronInelasticQBBC
 - G4HadronPhysicsFTFP_BERT
 - G4HadronPhysicsFTFP_BERT_ATL
 - G4HadronPhysicsFTFP_BERT_HP
 - G4HadronPhysicsFTFP_BERT_TRV
 - G4HadronPhysicsFTFQGSP_BERT
 - G4HadronPhysicsFTF_BIC
 - G4HadronPhysicsINCLXX
 - G4HadronPhysicsNuBeam
 - G4HadronPhysicsQGSP_BERT
 - G4HadronPhysicsQGSP_BERT_HP
 - G4HadronPhysicsQGSP_BIC
 - G4HadronPhysicsQGSP_BIC_AllHP
 - G4HadronPhysicsQGSP_BIC_HP
 - G4HadronPhysicsQGSP_FTFP_BERT
 - G4HadronPhysicsQGS_BIC
 - G4HadronPhysicsShielding
 - G4HadronPhysicsShieldingLEND
 - G4ImportanceBiasing
 - G4IonBinaryCascadePhysics
 - G4IonElasticPhysics
 - G4IonINCLXXPhysics
 - G4IonPhysics
 - G4IonPhysicsPHP
 - G4IonPhysicsXS
 - G4IonQMDPhysics
 - G4MuonicAtomDecayPhysics
 - G4NeutronCrossSectionXS
 - G4NeutronTrackingCut
 - G4OpticalPhysics
 - G4ParallelWorldPhysics
 - G4RadioactiveDecayPhysics
 - G4SpinDecayPhysics
 - G4StepLimiterPhysics
 - G4StoppingPhysics
 - G4StoppingPhysicsFritiofWithBinaryCascade
 - G4UnknownDecayPhysics
 - G4WeightWindowBiasing

