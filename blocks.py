# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   BLOCKS  
#
#   Where are large (>200 acres) blocks of recovering forest? 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  

# import tools from WBT module

from WBT.whitebox_tools import WhiteboxTools

# declare a name for the tools

wbt = WhiteboxTools()

# Set the Whitebox working directory
# You will need to change this to your local path name

# wbt.work_dir = "/Users/jhowarth/projects/wbt_starter/testData"

work =  "/Users/jhowarth/Library/CloudStorage/GoogleDrive-jhowarth@middlebury.edu/Shared drives/GEOG0352-S24/"

wbt.work_dir = work

# Declare a director for our outputs  

out = work + "jhowarth/outputs/blocks/"

# Declare a name for our test data

clearing = work + "DATA/clearings/Clearings_Addison_County_03192024.tif"  
rarity = work + "DATA/rarity/rarity_03212024.tif"

# ----------------------------------------------------------------------
#  0 Identify cores.
# ----------------------------------------------------------------------

# Make clearing binary.

wbt.equal_to(
    input1 = clearing, 
    input2 = 2, 
    output = out + "_01_clearings_binary.tif", 
    # callback=default_callback
)

wbt.euclidean_distance(
    i = out + "_01_clearings_binary.tif", 
    output = out + "_02_clearing_distance.tif", 
    # callback=default_callback
)

wbt.reclass(
    i = out + "_02_clearing_distance.tif", 
    output = out + "_03_forest_cores.tif", 
    reclass_vals = "0;0;200;1;200;max", 
    assign_mode=False, 
    # callback=default_callback
)

wbt.set_nodata_value(
    i = out + "_03_forest_cores.tif", 
    output = out + "_04_forest_cores_bg_nd.tif", 
    back_value=0.0, 
    # callback=default_callback
)

# Identify contiguous regions. 

wbt.clump(
    i = out + "_04_forest_cores_bg_nd.tif", 
    output = out + "_05_forest_core_clumps.tif", 
    diag=True, 
    zero_back=False, 
    # callback=default_callback
)

# wbt.set_nodata_value(
#     i = out + "_05_forest_core_clumps.tif", 
#     output = out + "_06_forest_core_clumps_bg_nd.tif", 
#     back_value=0.0, 
#     # callback=default_callback
# )

# Calculate area of objects. 

wbt.raster_area(
    i = out + "_05_forest_core_clumps.tif", 
    output= out + "_07_forest_core_clumps_area.tif", 
    out_text=False, 
    units="map units", 
    zero_back=True, 
    # callback=default_callback
)

# Convert to acres.

wbt.divide(
    input1 = out + "_07_forest_core_clumps_area.tif", 
    input2 = 4046.86, 
    output = out + "_08_forest_core_clumps_acres.tif", 
    # callback=default_callback
)

# reclassify

wbt.reclass(
    i = out + "_08_forest_core_clumps_acres.tif", 
    output = out + "_09_priority_clumps.tif", 
    reclass_vals = "0;0;5;1;5;999999999999999", 
    assign_mode=False, 
    # callback=default_callback
)

# ----------------------------------------------------------------------
#   1. Combine cores and rarity.
# ----------------------------------------------------------------------

wbt.convert_nodata_to_zero(
    i = out + "_09_priority_clumps.tif", 
    output = out + "_10_priority_clumps_bg0.tif", 
    # callback=default_callback
)

wbt.Or(
    input1 = rarity, 
    input2 = out + "_10_priority_clumps_bg0.tif", 
    output = out + "_11_habitat_qualities.tif", 
    # callback=default_callback
)

# ----------------------------------------------------------------------
#   2. Identify contiguous regions with qualities.
# ----------------------------------------------------------------------

# Make recovering binary.

wbt.equal_to(
    input1 = clearing, 
    input2 = 1, 
    output = out + "_21_recovering_binary.tif", 
    # callback=default_callback
)

wbt.set_nodata_value(
    i = out + "_21_recovering_binary.tif", 
    output = out + "_22_recovering_binary_bg_nd.tif", 
    back_value=0.0, 
    # callback=default_callback
)

# Identify contiguous regions. 

wbt.clump(
    i = out + "_22_recovering_binary_bg_nd.tif", 
    output = out + "_23_recovering_clumps.tif", 
    diag=True, 
    zero_back=False, 
    # callback=default_callback
)

wbt.zonal_statistics(
    i = out + "_11_habitat_qualities.tif", 
    features = out + "_23_recovering_clumps.tif", 
    output = out + "_24_recovering_clumps_with_qualities.tif", 
    stat="max", 
    out_table=None, 
    # callback=default_callback
)

wbt.convert_nodata_to_zero(
    i = out + "_24_recovering_clumps_with_qualities.tif", 
    output = out + "_25_recovering_clumps_with_qualities_binary.tif", 
    # callback=default_callback
)
