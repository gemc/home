---
layout: default
title: LUND Format
order: 32
description: LUND particle file format for the GEMC generator
---

GEMC can load event particle definitions from LUND files with:

```bash
gemc -gparticlefile="[{format: lund, filename: events.lund}]"
```

The `format` value is case-insensitive, so `lund`, `Lund`, and `LUND` are equivalent.

## Event Structure

A LUND file contains one or more events. Each event has:

1. one header line;
2. a blank line separating the header from particle data;
3. `N` particle lines, where `N` is the first value in the header.

GEMC reads the whole file as event records. In single-threaded mode, event 0 in the
file is used for GEMC event 0, event 1 for GEMC event 1, and so on.
In multi-threaded mode, Geant4 distributes event IDs to worker threads, and GEMC uses
the event ID to select the LUND event record. This means LUND events are distributed
to threads; each worker does not replay the full file.

If `gparticle` is also present, each GEMC event receives the `gparticle` particles
plus the matching LUND event record.

## Header Line

The header must contain at least 10 numeric variables. Up to 100 variables are allowed.
Quantities shown in bold are used by GEMC. Other variables are user-defined values
kept by the LUND convention but not used to create primaries.

{:.zebra .compact-table}

| Column | Quantity |
| --- | --- |
| 1 | **Number of particles in this event.** |
| 2 | Mass number of the target. User-defined. |
| 3 | Atomic number of the target. User-defined. |
| 4 | Target polarization. User-defined. |
| 5 | **First particle z component of spin.** |
| 6 | Beam type, for example electron = 11, photon = 22. User-defined. |
| 7 | Beam energy in GeV. User-defined. |
| 8 | Interacted nucleon ID, for example 2212 or 2112. User-defined. |
| 9 | Process ID. User-defined. |
| 10 | Event weight. User-defined. |
| 11-100 | Optional numeric values. |

Header column 1 must be a non-negative integer.

Example header for an event with two particles:

```text
2 1 1 0 0 0 0 0 0 1
```

## Particle Lines

After the header and blank separator, the event must contain exactly `N` particle lines.
Each particle line must contain at least 14 numeric columns. Up to 100 columns are allowed.
Quantities shown in bold are used by GEMC. Other variables are user-defined values.

{:.zebra .compact-table}

| Column | Quantity |
| --- | --- |
| 1 | **Particle index. Indices start from 1 and must follow the particle order.** |
| 2 | Lifetime in ns. User-defined. |
| 3 | **Type. Only type `1` is propagated in Geant4.** |
| 4 | **PDG particle ID.** |
| 5 | Parent index. User-defined. |
| 6 | First daughter index. User-defined. |
| 7 | **Momentum x in GeV.** |
| 8 | **Momentum y in GeV.** |
| 9 | **Momentum z in GeV.** |
| 10 | Energy in GeV. User-defined. |
| 11 | Mass in GeV. User-defined. |
| 12 | **Vertex x in cm.** |
| 13 | **Vertex y in cm.** |
| 14 | **Vertex z in cm.** |
| 15-100 | Optional numeric values. |

Columns 1, 3, 4, 5, and 6 must be integer-valued. GEMC creates primaries only for
particle lines with type `1`.

## Minimal Example

```text
2 1 1 0 0 0 0 0 0 1

1 0 1 11 0 0 0.0 0.0 2.3 2.3 0.0005 0.0 0.0 0.0
2 0 1 2212 0 0 0.0 0.1 1.2 1.5 0.9383 0.0 0.0 0.0
```

This event creates:

- one electron with momentum `(0.0, 0.0, 2.3)` GeV at `(0.0, 0.0, 0.0)` cm;
- one proton with momentum `(0.0, 0.1, 1.2)` GeV at `(0.0, 0.0, 0.0)` cm.

## Multi-Event Example

The following example shows the first two deep inelastic scattering events from
`gparticle/examples/test_dis.dat`. A blank line separates consecutive event
records.

```text
22  1.  1.  0  1 0.331   0.616   9.392   4.211   6.778
1 -1.   21   11  0  0    0.0000    0.0000   11.0000   11.0000    0.0005      0.0000    0.0000    0.0000
2  1.   21 2212  0  0    0.0000    0.0000    0.0000    0.9383    0.9383      0.0000    0.0000    0.0000
3  0.   21   22  1  0    0.4304   -1.1806    6.9709    6.7795   -2.0521      0.0000    0.0000    0.0000
4 -1.    1   11  1  0   -0.4304    1.1806    4.0291    4.2205    0.0005      0.0000    0.0000    0.0000
5  0.   13    1  0  6    0.4449   -1.2501    5.2451    5.4104    0.0099      0.0000    0.0000    0.0000
6  1.   13 2203  2  0   -0.0209    0.0205    0.5730    0.9613    0.7713      0.0000    0.0000    0.0000
7  0.   11  223  2 10    0.0643   -0.1027    1.7762    1.9395    0.7697      0.0000    0.0000    0.0000
8  0.   12    1  5 13    0.4449   -1.2501    5.2451    5.4104    0.0099      0.0000    0.0000    0.0000
9  1.   11 2203  6 13   -0.0209    0.0205    0.5730    0.9613    0.7713      0.0000    0.0000    0.0000
10  1.    1  211  7  0    0.1259    0.1147    0.1596    0.2720    0.1396      0.0000    0.0000    0.0000
11 -1.    1 -211  7  0    0.0111   -0.0038    0.7083    0.7221    0.1396      0.0000    0.0000    0.0000
12  0.   11  111  7 17   -0.0728   -0.2136    0.9082    0.9455    0.1350      0.0000    0.0000    0.0000
13  0.   11   92  8 14    0.4240   -1.2296    5.8181    6.3717    2.2486      0.0000    0.0000    0.0000
14 -1.    1 -211 13  0   -0.1951    0.0573    0.1465    0.2869    0.1396      0.0000    0.0000    0.0000
15  2.   11 2224 13 19    0.7526   -0.8204    4.3391    4.6603    1.2848      0.0000    0.0000    0.0000
16  0.   11  111 13 21   -0.1336   -0.4665    1.3325    1.4245    0.1350      0.0000    0.0000    0.0000
17  0.    1   22 12  0   -0.0133   -0.0625    0.0844    0.1059    0.0000      0.0000    0.0000    0.0000
18  0.    1   22 12  0   -0.0595   -0.1511    0.8237    0.8396    0.0000      0.0000    0.0000    0.0000
19  1.    1 2212 15  0    0.8743   -0.7894    3.9728    4.2487    0.9383      0.0000    0.0000    0.0000
20  1.    1  211 15  0   -0.1216   -0.0310    0.3663    0.4116    0.1396      0.0000    0.0000    0.0000
21  0.    1   22 16  0   -0.1474   -0.4391    1.1554    1.2448    0.0000      0.0000    0.0000    0.0000
22  0.    1   22 16  0    0.0139   -0.0274    0.1770    0.1797    0.0000      0.0000    0.0000    0.0000

18  1.  1.  0  1 0.291   0.555   9.010   3.329   6.105
1 -1.   21   11  0  0    0.0000    0.0000   11.0000   11.0000    0.0005      0.0000    0.0000    0.0000
2  1.   21 2212  0  0    0.0000    0.0000    0.0000    0.9383    0.9383      0.0000    0.0000    0.0000
3  0.   21   22  1  0    1.0953    0.5086    6.2578    6.1065   -1.8247      0.0000    0.0000    0.0000
4 -1.    1   11  1  0   -1.0953   -0.5086    4.7422    4.8935    0.0005      0.0000    0.0000    0.0000
5  1.   13    2  0  6    1.2316    0.7953    5.9929    6.1696    0.0056      0.0000    0.0000    0.0000
6  0.   13 2103  2  0   -0.1364   -0.2867    0.2649    0.8752    0.7713      0.0000    0.0000    0.0000
7  1.   12    2  5  9    1.2316    0.7953    5.9929    6.1696    0.0056      0.0000    0.0000    0.0000
8  0.   11 2103  6  9   -0.1364   -0.2867    0.2649    0.8752    0.7713      0.0000    0.0000    0.0000
9  0.   11   92  7 10    1.0953    0.5086    6.2578    7.0448    3.0017      0.0000    0.0000    0.0000
10  0.   11  111  9 13    0.8210    0.9015    4.0458    4.2277    0.1350      0.0000    0.0000    0.0000
11  1.    1  211  9  0    0.1662   -0.3106    0.7357    0.8276    0.1396      0.0000    0.0000    0.0000
12  0.   11 2114  9 15    0.1081   -0.0823    1.4763    1.9895    1.3267      0.0000    0.0000    0.0000
13  0.    1   22 10  0    0.1194    0.2105    0.8070    0.8425    0.0000      0.0000    0.0000    0.0000
14  0.    1   22 10  0    0.7016    0.6909    3.2388    3.3852    0.0000      0.0000    0.0000    0.0000
15  0.    1 2112 12  0    0.0064    0.2212    1.2305    1.5639    0.9396      0.0000    0.0000    0.0000
16  0.   11  111 12 17    0.1017   -0.3035    0.2458    0.4255    0.1350      0.0000    0.0000    0.0000
17  0.    1   22 16  0    0.1299   -0.2575    0.1780    0.3389    0.0000      0.0000    0.0000    0.0000
18  0.    1   22 16  0   -0.0282   -0.0460    0.0678    0.0866    0.0000      0.0000    0.0000    0.0000
```

The first LUND record contributes to GEMC event 0 and the second record contributes
to GEMC event 1. With multiple Geant4 worker threads, those GEMC event IDs may be
processed by different workers, but each file event is still used once for its
matching event ID.
