---
layout: default
title: Gemc options
order: 2
description: How to use the command line and / or jcards to setup a gemc session

---



gemc can be configured using: 

- command line options
- steering cards 

For example:

```
gemc -gui example.jcard
```

will launch gemc using its graphical user interface and the directives specified in the file 'example.jcard'

## JCards

<br/>
The gemc steering cards are called **jcard**s and have the extention **.jcard**. These are JSON files but comments can be added using the # sign.
An example of jcard:
```
{

	# verbosities
	"verbosity": 1,
	"edistv": 2,

	# the pim_absorbtion system
	"+gsystem": [
		{
			"system":   "./pim_absorbtion",
			"factory": "text",
			"variation": "default"
		}
	],

	# the output
	"+goutput": [
		{
			"format": "ROOT",
			"name": "events.root",
			"type": "event"
		}
	],

	# number of events
	"n": 10000,
	
	# Generator: an 11 GeV electron on the z axis placed at z = -10cm
	"+gparticle": [
		{ "pname": "e-", "p": 11000, "vz": -10.0}
	]
}
```




<!--## JCards and command lines-->
<!---->
<!--The directives on the steering card are equivalent to the one in the command lines, -->
<!---->
<!--- For non-cumulative options the command line options overwrites the jcard options. -->
<!--- On the other hand, all instances of cumulative options will be compounded.-->
<!---->
<!---->



<!---->
<!--## Cumulative Options-->
<!---->
<!---->
<!--## Importing Jcards-->


## Complete List of gemc options

The following is the output of gemc -h. Soon this help will be better formatted to be displayed online.

```
Usage:

 ➤ -dawn .....................takes a screenshot of the loaded scene using the dawn driver
 ➤ -gui ......................use Graphical User Interface
 ➤ -logG4Materials ...........Log Geant4 Predefined Materials
 ➤ -printSystemsMaterials ....Print the materials used in this simulation
 ➤ -recordZeroEdep ...........Record particle even if they do not deposit energy in the sensitive volumes
 ➤ -showAvailablePhysics .....Log Geant4 Physics Modules that can be used with the "physicsList" option
 ➤ -showAvailablePhysicsX ....Log Geant4 Physics Modules that can be used with the "physicsList" option and exit
 ➤ -sndf .....................Shows non default options
 ➤ -stream ...................Activate Streaming ReadOut
 ➤ -useDefaultMaterial .......use material defined by "defaultMaterial" option if a volume's material is not defined
 ➤ -nthreads=<value> .........set number of threads
 ➤ -verbosity=<value> ........Possible values: 0: shush; 1: summary; 2: details; 3: everything
 ➤ -grunv=<value> ............Possible values: 0: shush; 1: summary; 2: details; 3: everything
 ➤ -gsensitivityv=<value> ....Possible values: 0: shush; 1: summary; 2: details; 3: everything
 ➤ -elog=<value> .............Log every N events
 ➤ -gpluginsPath=<value> .....Directory containing the plugins
 ➤ -tlog=<value> .............Log only thread # given. 0 (default) means log all
 ➤ -dVariation=<value> .......Digitization Variation
 ➤ -eventTimeSize=<value> ....event duration with unit. Examples: 4*ns, 2*ms
 ➤ +gsystem=<jsonvalue> ......defines a group of detectors

                              A system definition includes the geometry location, factory and variation

                              Example: +gsystem={detector: "experiments/clas12/targets", factory: "TEXT", variation: "bonus"}

                              <jsonvalue>:

                               • system: system name (mandatory). For TEXT factories, it may include the path to the file
                               • factory: factory name (mandatory). Possible choices: TEXT, CAD, GDML
                               • variation: geometry variation (optional, default is default)
                               • runno: runno (optional, default is 1)

 ➤ +gmodifier=<jsonvalue> ....modify volume existance or placement

                              The volume modifer can shift, tilt, or delete a volume from the gworld

                              Example: +gmodifier={volume: "targetCell", tilt: "0*deg, 0*deg, -10*deg" }

                              <jsonvalue>:

                               • volume: volume name (optional)
                               • shift: volume shift added to existing position
                               • tilt: volume tilt added to existing rotation
                               • isPresent: remove volume from world if set to false

 ➤ -gsystemv=<value> .........verbosity for gsystem. Possible values: 0: shush; 1: summary; 2: details; 3: everything
 ➤ -worldVolume=<value> ......geant4 definition for the world volume <root>. Default is G4Box, 15*m, 15*m, 15*m, G4_Air
 ➤ -g4systemv=<value> ........Possible values: 0: shush; 1: summary; 2: details; 3: everything
 ➤ -logVolume=<value> ........log all information for volume
 ➤ -defaultMaterial=<value> ..default material to be used if the switch "useDefaultMaterial" is activated
 ➤ -checkOverlaps=<value> ....Check for volumes overlaps.
                              Possibles values are:
                               - 0 (default): no check.
                               - 1: check for overlaps at physical volume construction.
                               - 2: use the geant4 overlap validator with 10,000 points on the surface
                               - Any number greater than 100 : use the geant4 overlap validator with this number of points on the surface
 ➤ -geventstreamv=<value> ....Possible values: 0: shush; 1: summary; 2: details; 3: everything
 ➤ -gframestreamv=<value> ....Possible values: 0: shush; 1: summary; 2: details; 3: everything
 ➤ +goutput=<jsonvalue> ......Output format and name

                              Define a Output format and name

                              Example: +output={format: "TEXT", name: "output.txt", type: "event" }

                              Current available formats:

                               - TEXT

                              Output types

                               - event: write events
                               - stream: write frame stream

                              <jsonvalue>:

                               • format: Output file format
                               • name: Output file name
                               • type: Output type

 ➤ -g4view=<jsonvalue> .......geant4 viewer properties

                              Defines the geant4 viewer properties:
                               - screen dimensions
                               - screen position
                               - resolution in terms of segments per circle

                              Example: -g4view={viewer: "OGL", dimension: "1100x800", position: "+200+100", segsPerCircle: 100}

                              <jsonvalue>:

                               • viewer: g4 viewer. Available choices:

				- OpenGLImmediateQt
				- OGLIQt
				- OGLI
				- OpenGLStoredQt
				- OGLSQt
				- OGL
				- OGLS

                               • dimension: g4 viewer dimension
                               • position: g4 viewer position
                               • segsPerCircle: Number of segments per circle

 ➤ -g4camera=<jsonvalue> .....geant4 camera

                              Defines the geant4 camera view point

                              Example: -g4camera={phi: "20*deg"; theta: "15*deg";}

                              <jsonvalue>:

                               • phi: geant4 camera phi
                               • theta: geant4 camera theta

 ➤ -g4displayv=<value> .......Possible values: 0: shush; 1: summary; 2: details; 3: everything
 ➤ +scenetext=<jsonvalue> ....adds text to the scene

                              Adds a scene text. The text does not move with the detector.

                              Example: +scenetext={text: "lhc experiment", color: "green", x: 0.5, y: 0.5}

                              <jsonvalue>:

                               • text: scene text (mandatory).
                               • color: scene text color (optional). Possible values are color names such as green, red, etc. Default is white.
                               • x: scene text x position (optional). Possible values: between -1 and 1. Default is 0.
                               • y: scene text y position (optional). Possible values: between -1 and 1. Default is 0.
                               • size: scene text size (optional). Default is 24

 ➤ +viewtext=<jsonvalue> .....adds text to the view

                              Adds a view text.

                              Example: +viewtext={text: "lhc experiment", color: "green", x: 5, y: 5, z: 30}

                              <jsonvalue>:

                               • text: view text (mandatory).
                               • color: view text color (optional). Possible values are color names such as green, red, etc. Default is white.
                               • x: view text x position in cm. Default is 0.
                               • y: view text y position in cm. Default is 0.
                               • z: view text z position in cm. Default is 0.
                               • size: view text size (optional). Default is 24

 ➤ -edistv=<value> ...........Possible values: 0: shush; 1: summary; 2: details; 3: everything
 ➤ -runWeightsFile=<value> ...Text file with run number and their weights
   The text file must have two columns, run# and weight.
   For example a "weights.txt" file that contains:
   11 0.1
   12 0.7
   13 0.2
   will simulate 10% of events with run number 11 conditions, 70% for run 12 and 20% for run 13.

 ➤ -n=<value> ................Number of events to process
 ➤ -userRunno=<value> ........User Run Number
 ➤ -maxebuffer=<value> .......Max number of events to keep in memory before writing out the output.
 ➤ +gparticle=<jsonvalue> ....adds a particle to the event generator


                              Examples

                              • 5 GeV electron along z:
                                +gparticle={"pname": "e-"; "p": 5000;}

                              • a 500 MeV neutron at theta=20 deg and uniform distribution in phi:
                                +gparticle={"pname": "neutron"; "p": 500; "theta": 20; "delta_phi": 180}

                              • 150 2.1 GeV electrons at theta=3deg, uniform in phi, at z=-2mm
                                +gparticle={ "pname": "e-", "multiplicity": 150, "p": 2100, "theta": 3.0, "delta_phi": 180.0, "vz": -2.0}

                              • 250 3 GeV pions+ at theta between 5 and 15 deg (uniform in cos(theta)), phi = 180
                                +gparticle={ "pname": "pi+", "multiplicity": 250, "p": 3000, "theta": 10.0, "delta_theta": 5.0, "phi": 180}

                              • 250 3 GeV pions+ at theta between 5 and 15 deg (uniform in theta), phi = 180
                                +gparticle={ "pname": "pi+", "multiplicity": 250, "p": 3000, "theta": 10.0, "delta_theta": 5.0, "phi": 180, "thetaModel": "flat"}

                              • 400 MeV protons at theta=90deg, uniform in phi, v on a sphere of radius 0.5mm at vz=-4mm
                                +gparticle={ "pname": "proton", "multiplicity": 400, "p": 150, "theta": 90.0, "delta_phi": 180.0, "delta_VR": 0.5, "vz": -4.0}

                              <jsonvalue>:

                               • pname: Particle name, for example proton
                               • multiplicity: How many copies of this particle will be generated in each event
                               • p: Particle momentum
                               • theta: Particle polar angle. Default: 0
                               • phi: Particle azimuthal angle. Default: 0
                               • delta_p: Particle momentum range, centered on p. Default: 0
                               • delta_theta: Particle polar angle range, centered on theta. Default: 0
                               • delta_phi: Particle azimuthal angle range, centered on phi. Default: 0
                               • randomMomentumModel: Momentum randomization. Default: uniform distribution. 'gaussian': use deltas as sigmas
                               • thetaModel: Distribute cos(theta) or theta. 'ct' (default): cosTheta is uniform. 'flat': theta is uniform
                               • punit: Unit for the particle momentum. Default: MeV
                               • aunit: Unit for the particle angles. Default: deg
                               • vx: Particle vertex x component. Default: 0
                               • vy: Particle vertex y component. Default: 0
                               • vz: Particle vertex z component. Default: 0
                               • delta_vx: Particle vertex range of the x component. Default: 0
                               • delta_vy: Particle vertex range of the y component. Default: 0
                               • delta_vz: Particle vertex range of the z component. Default: 0
                               • delta_VR: Particle vertex is generated within a sphere of radius delta_R. Default: 0
                               • randomVertexModel: Vertex randomization. Default: uniform distribution. 'gaussian': use deltas as sigmas
                               • vunit: Unit for the particle vertex. Default: mm

 ➤ -gphysv=<value> ...........Possible values: 0: shush; 1: summary; 2: details; 3: everything
 ➤ -physicsList=<value> ......Geant4 Version $Name: geant4-11-00-patch-03 $ Physics List: it contains a Geant4 physics module, optional e.m. replacement, and optional physics constructors
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

                              For example, FTFP_BERT_LIV would replace the default e.m. physics with the Livermode model


                              Additional physics can be loaded by adding its constructor name to the list using the  sign

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

```






