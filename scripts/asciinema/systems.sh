#!/usr/bin/env bash

scigTemplate.py -s forward

cd forward
ls -l

./forward.py
ls -l

gemc forward.jcard

