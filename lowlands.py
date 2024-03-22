# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# LOWLANDS
#   
# Map connected valley bottoms from a 10m DEM.
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

out = work + "jhowarth/outputs/lowlands/"

# Declare a name for our test data

dem = work + "data/elevation/DEM_10m_03192024.tif"
mama = dem
building_zone = work + "data/clearings/building_zone_03202024.tif"
# lowlands = work + "jhowarth/outputs/lowlands/_03_lowland_upland_binary_filtered.tif"


# ----------------------------------------------------------------------
#   Choose parameters for landform classification
# ----------------------------------------------------------------------

# Three bears approach for search radius: 100, 250, 500.

# # wbt.geomorphons(
# #     dem = dem, 
# #     output = out + "_01_geomorphons_100.tif", 
# #     search=100, 
# #     threshold=0.0, 
# #     # fdist=0, 
# #     # skip=0, 
# #     forms=True, 
# #     # residuals=False, 
# #     # callback=default_callback
# # )

# wbt.geomorphons(
#     dem = dem, 
#     output = out + "_01_geomorphons_250.tif", 
#     search=250, 
#     threshold=0.0, 
#     # fdist=0, 
#     # skip=0, 
#     forms=True, 
#     # residuals=False, 
#     # callback=default_callback
# )

# # wbt.geomorphons(
# #     dem = dem, 
# #     output = out + "_01_geomorphons_500.tif", 
# #     search=500, 
# #     threshold=0.0, 
# #     # fdist=0, 
# #     # skip=0, 
# #     forms=True, 
# #     # residuals=False, 
# #     # callback=default_callback
# # )

# ----------------------------------------------------------------------
#   Valley bottoms from landforms
# ----------------------------------------------------------------------

# Make binary of upland versus lowlands (where lowlands are valley or pits). 

wbt.greater_than(
    input1 = out + "_01_geomorphons_250.tif", 
    input2 = 9, 
    output = out + "_11_lowland_upland_binary.tif", 
    incl_equals=True, 
    # callback=default_callback
)

# Reduce noise with a majority filter. 

wbt.majority_filter(
    i = out + "_11_lowland_upland_binary.tif", 
    output = out + "_12_lowland_upland_binary_filtered.tif", 
    filterx=5, 
    filtery=5, 
    # callback=default_callback
)

wbt.clump(
    i =  out + "_12_lowland_upland_binary_filtered.tif", 
    output = out + "_13_lowland_objects.tif", 
    diag=True, 
    zero_back=True, 
    # callback=default_callback
)

# ----------------------------------------------------------------------
#   Assess impact of human development on connectedness of lowland network.
# ----------------------------------------------------------------------

# Resample built proximity layer to mama raster resolution and extent. 

wbt.resample(
    inputs = building_zone, 
    output = out + "_21_building_zone_mama.tif", 
    cell_size=None, 
    base = mama, 
    method = "nn", 
    # callback=default_callback
)

wbt.equal_to(
    input1 = out + "_21_building_zone_mama.tif", 
    input2 = 2, 
    output = out + "_22_building_zone_binary.tif", 
    # callback=default_callback
)

wbt.multiply(
    input1 = out + "_22_building_zone_binary.tif", 
    input2 = 10, 
    output = out + "_23_building_zone_binary_10.tif", 
    # callback=default_callback
)

wbt.add(
    input1 = out + "_23_building_zone_binary_10.tif", 
    input2 = out + "_12_lowland_upland_binary_filtered.tif", 
    output = out + "_24_lowlands_building_zones_combo.tif", 
    # callback=default_callback
)

wbt.equal_to(
    input1 = out + "_24_lowlands_building_zones_combo.tif", 
    input2 = 1, 
    output = out + "_25_lowlands_left_after_building_zones.tif", 
    # callback=default_callback
)

wbt.clump(
    i = out + "_25_lowlands_left_after_building_zones.tif", 
    output = out + "_26_lowland_objects_left_after_building_zones.tif", 
    diag=True, 
    zero_back=True, 
    # callback=default_callback
)