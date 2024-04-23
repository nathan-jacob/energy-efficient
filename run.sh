#!/bin/bash
files=(
    "008.espresso.din"
    "013.spice2g6.din"
    "015.doduc.din"
    "022.li.din"
    "023.eqntott.din"
    "026.compress.din"
    "034.mdljdp2.din"
    "039.wave5.din"
    "047.tomcatv.din"
    "048.ora.din"
    "085.gcc.din"
    "089.su2cor.din"
    "090.hydro2d.din"
    "093.nasa7.din"
    "094.fpppp.din"
)
for file in "${files[@]}"; do
    python CacheSimulator.py "$file"
done
