#!/usr/bin/env bash

scigTemplate.py -s forward

cd forward
ls -l

# adds a box volume to geometry.py
scigTemplate.py -gv G4Box  -gvp '30 40 50 cm' >> geometry.py
cat geometry.py

./forward.py

gemc forward.jcard
