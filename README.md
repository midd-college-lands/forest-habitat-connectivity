# Forest habitat connectivity 

![habitat connectivity model](images/hc-model.png)  

## Introduction

A model to identify a connected system of habitat blocks and connectors (Act 171) in Addison County, Vermont. It consists of the following routines.  

| STEP | SCRIPT | SOURCE | DESCRIPTION |
| :--:  | :---   | :---:   | :---        | 
| 1 | dem_10m | [ee repo][ee-repo] | Load and export USGS 3DEP 10m for study region. |   
| 2 | lowlands.py | [github][ll] | Classify landforms, isolate valley bottoms, and remove developed regions from valley bottoms. This represents potential locations to maintain connectedness of habitat fragments. |  
| 3 | clearings.js | [ee repo][ee-repo] | Identify clearings maintained by human activity from landcover and e911 footprints; export as geoTiff.  |  
| 4 | rarity.js | [ee repo][ee-repo] | Identify rare natural communities and rare plant locations from ANR natural heritage datasets. This contributes to the block qualities assessment (along with core area of blocks). |   
| 5 | blocks.py | [github][hb] | Identify blocks of habitat with qualities that make them conservation priorities. Invert clearings to represent contiguous blocks of reforesting habitat, isolate core habitat at least 200 meters from edge, isolate cores that are greater than five acres. Combine recovering blocks that include either rare natural communities or rare plant species. |  
| 6 | connectors.py | [github][hc] | Select valley bottoms that connect two or more priority blocks. Check that connectors and blocks create continuous habitat for study region. | 


[ee-repo]: https://code.earthengine.google.com/?accept_repo=users/jhowarth/college-lands   

[ll]: lowlands.py

[hb]: blocks.py  

[hc]: connectors.py