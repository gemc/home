---
layout: default
title: System
order: 1
description: How to create a system, a hierarchical collection of volumes.
---

A detector in gemc is composed by one or more *systems*, each a hierarchical collection of volumes.
In the example below, the forward and central detector systems are defined, each composed by a set of volumes.

<ul style='list-style-type: square'>
    <li>Forward detector System
        <ul style='list-style-type: " ⌙ "'>
            <li>calorimeter
                <ul style='list-style-type: " ⌙ ︎"'>
                    <li>paddle 1</li>
                    <li>paddle 2</li>
                    <li>...</li>
                </ul>
            </li>
        </ul>
    </li>
    <li>Central Detector
        <ul style='list-style-type: " ⌙ ︎"'>
			<li>Time Of Flight
                <ul style='list-style-type: " ⌙ ︎"'>
                    <li>scintillator 1</li>
                    <li>...</li>
                </ul>
			</li>
			<li>Cerenkov
                <ul style='list-style-type: " ⌙ ︎"'>
                    <li>mirror 1</li>
                    <li>...	</li>
                </ul>
			</li>
		</ul>
    </li>
</ul>

The volumes can be geant4 objects built using the [sci-g](https://github.com/gemc/sci-g) python api or imported from
CAD / GDML.

<br/>

