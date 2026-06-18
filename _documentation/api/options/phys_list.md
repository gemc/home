---
layout: default
title: 'GEMC option: phys_list'
---

# `phys_list`

Type: `option`

Description: Select Physics List

Generated from:

```sh
gemc help phys_list
```

```text
-phys_list=<value> .........: Select Physics List


   Geant4 Version $Name: geant4-11-04-patch-02 $ Physics List: it contains a Geant4 physics module, optional e.m. replacement, and optional physics constructors
   The available geant4 modules are:
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
   The default e.m. physics can be replaced by appending one of these string to the module above:
   - _EM0 to use G4EmStandardPhysics
   - _EMV to use G4EmStandardPhysics_option1
   - _EMX to use G4EmStandardPhysics_option2
   - _EMY to use G4EmStandardPhysics_option3
   - _EMZ to use G4EmStandardPhysics_option4
   - _GS to use G4EmStandardPhysicsGS
   - _LE to use G4EmLowEPPhysics
   - _LIV to use G4EmLivermorePhysics
   - _PEN to use G4EmPenelopePhysics
   - _SS to use G4EmStandardPhysicsSS
   - _WVI to use G4EmStandardPhysicsWVI
   For example, FTFP_BERT_LIV would replace the default e.m. physics with the Livermore model
   Additional physics can be loaded by adding its constructor name to the list using the + sign
   For example: FTFP_BERT + G4OpticalPhysics. The available constructors are:
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
   Command-line examples:
   -phys_list=FTFP_BERT
   -phys_list="FTFP_BERT_EMZ + G4OpticalPhysics"
```
