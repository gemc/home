---
layout: default
title: 'GEMC Options Reference'
---

# GEMC Options Reference

This page is generated from `gemc -h`. Click each item for help.<br/><br/>

## Switches

| Name | Description |
| --- | --- |
| [`gui`](/home/documentation/api/options/gui)<br/> | run with the graphical user interface (Qt window) |
| [`i`](/home/documentation/api/options/i)<br/> | drop into the interactive Geant4 terminal session (non-GUI mode) |
| [`printSystemsMaterials`](/home/documentation/api/options/printsystemsmaterials)<br/> | print the materials used in this simulation |
| [`print_summary`](/home/documentation/api/options/print_summary)<br/> | print a timing summary at the end of the simulation (total wall-clock time, total time since beamOn, and the average event rate). On by default; disable with -print_summary=false. |
| [`recordZeroEdep`](/home/documentation/api/options/recordzeroedep)<br/> | Record particle even if they do not deposit energy in the sensitive volumes |
| [`showPhysics`](/home/documentation/api/options/showphysics)<br/> | Log Geant4 Physics Available Modules that can be used with the "phys_list" option and exit |
| [`showPredefinedMaterials`](/home/documentation/api/options/showpredefinedmaterials)<br/> | log GEMC Predefined Materials |
| [`useDawn`](/home/documentation/api/options/usedawn)<br/> | Take a dawn screenshot |

## Options

| Name | Shape | Description |
| --- | --- | --- |
| [`nthreads`](/home/documentation/api/options/nthreads) | `<value>` | sets number of threads. |
| [`randomEngine`](/home/documentation/api/options/randomengine) | `<value>` | randomEngine |
| [`seed`](/home/documentation/api/options/seed) | `<value>` | seed |
| [`plugin_path`](/home/documentation/api/options/plugin_path) | `<value>` | colon-separated list of directories to search for .gplugin files |
| [`gsystem`](/home/documentation/api/options/gsystem) | `<sequence>` | defines the group of volumes in a system |
| [`gmodifier`](/home/documentation/api/options/gmodifier) | `<sequence>` | modify volume existence or placement |
| [`root`](/home/documentation/api/options/root) | `<value>` | root volume definition |
| [`sql`](/home/documentation/api/options/sql) | `<value>` | sql host or sqlite file |
| [`ascii_db`](/home/documentation/api/options/ascii_db) | `<value>` | ascii factory search path |
| [`experiment`](/home/documentation/api/options/experiment) | `<value>` | experiment selection |
| [`runno`](/home/documentation/api/options/runno) | `<value>` | geometry/conditions run number |
| [`useBackupMaterial`](/home/documentation/api/options/usebackupmaterial) | `<value>` | Backup material |
| [`check_overlaps`](/home/documentation/api/options/check_overlaps) | `<value>` | check overlaps |
| [`gmultipoles`](/home/documentation/api/options/gmultipoles) | `<sequence>` | define the e.m. gmultipoles |
| [`gfields`](/home/documentation/api/options/gfields) | `<sequence>` | define a generic plugin-backed e.m. field |
| [`global_field`](/home/documentation/api/options/global_field) | `<value>` | associate a field with the ROOT world volume |
| [`no_field`](/home/documentation/api/options/no_field) | `<value>` | reset the field of one or more volumes |
| [`fieldAt`](/home/documentation/api/options/fieldat) | `<value>` | query all configured fields at x y z |
| [`fieldMapPoints`](/home/documentation/api/options/fieldmappoints) | `<value>` | ASCII file of x y z points for field queries |
| [`ebuffer`](/home/documentation/api/options/ebuffer) | `<value>` | number of events kept in memory before flushing them to the filestream |
| [`gstreamer`](/home/documentation/api/options/gstreamer) | `<sequence>` | define a gstreamer output |
| [`splash_time`](/home/documentation/api/options/splash_time) | `<value>` | splash display time in seconds |
| [`splash_scale`](/home/documentation/api/options/splash_scale) | `<value>` | splash image scale factor |
| [`phys_list`](/home/documentation/api/options/phys_list) | `<value>` | Select Physics List |
| [`log_every`](/home/documentation/api/options/log_every) | `<value>` | log module: print event progress and average rate every N events per thread |
| [`gparticle`](/home/documentation/api/options/gparticle) | `<sequence>` | define the generator particle(s) |
| [`gparticlefile`](/home/documentation/api/options/gparticlefile) | `<sequence>` | define generator particles from file(s) |
| [`n`](/home/documentation/api/options/n) | `<value>` | number of events to process |
| [`run`](/home/documentation/api/options/run) | `<value>` | event run number |
| [`run_weights`](/home/documentation/api/options/run_weights) | `<value>` | File with run number and weights |
| [`g4view`](/home/documentation/api/options/g4view) | `<sequence>` | Defines the geant4 viewer properties |
| [`g4camera`](/home/documentation/api/options/g4camera) | `<sequence>` | Defines the geant4 camera view point |
| [`g4light`](/home/documentation/api/options/g4light) | `<sequence>` | Defines the geant4 light source direction |
| [`dawn`](/home/documentation/api/options/dawn) | `<sequence>` | Defines the dawn view point |
| [`g4decoration`](/home/documentation/api/options/g4decoration) | `<sequence>` | Adds optional Geant4 scene decorations |
| [`g4text`](/home/documentation/api/options/g4text) | `<sequence>` | Insert texts in the current scene |
| [`conf_yaml`](/home/documentation/api/options/conf_yaml) | `<value>` | infix for the YAML file that records the resolved options |
| [`tt`](/home/documentation/api/options/tt) | `<value>` | GUI test timeout (ms) |
| [`verbosity`](/home/documentation/api/options/verbosity) | `<sequence>` | Sets the log verbosity for various classes |
| [`debug`](/home/documentation/api/options/debug) | `<sequence>` | Sets the debug level for various classes |

