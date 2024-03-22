# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   CONNECTORS FOR BLOCKS
#
#   Where are contiguous regions of forest connected by lowland regions? 
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

out = work + "jhowarth/outputs/connectors/"

# Declare named for test data.

blocks = work + "jhowarth/outputs/blocks/_25_recovering_clumps_with_qualities_binary.tif"
lowlands = work + "jhowarth/outputs/lowlands/_25_lowlands_left_after_building_zones.tif"

# ------------------------------------------------------------------------------
# Step 0. Erase valleys where they overlap blocks. 
# ------------------------------------------------------------------------------

# Convert blocks into an inverse binary. 

wbt.equal_to(
    input1 = blocks, 
    input2 = 0, 
    output = out + "_01_inverse_binary.tif", 
)

# Erase blocks from valley bottoms.  

wbt.multiply(
    input1 = out + "_01_inverse_binary.tif", 
    input2 = lowlands, 
    output = out + "_02_valleys_not_blocks.tif", 
)

# Re-clump valley bottoms to identify individual objects. 

wbt.clump(
    i = out + "_02_valleys_not_blocks.tif", 
    output = out + "_03_valleys_not_blocks_objects.tif", 
    diag=True, 
    zero_back=True
)

# Mask background.

wbt.set_nodata_value(
    i = out + "_03_valleys_not_blocks_objects.tif", 
    output = out + "_04_valleys_not_blocks_objects_bg_nd.tif", 
    back_value=0.0,
)

# ------------------------------------------------------------------------------
# Step 1. Identify and remove islands. 
# ------------------------------------------------------------------------------

# Grow forest blocks edge by one pixel.

wbt.maximum_filter(
    i = blocks, 
    output =  out +"_11_blocks_extra_edge.tif", 
    filterx=3, 
    filtery=3
)

# Test for overlap between valley bottoms and habitat blocks.

wbt.zonal_statistics(
    i = out + "_11_blocks_extra_edge.tif", 
    features = out + "_04_valleys_not_blocks_objects_bg_nd.tif", 
    output = out + "_12_island_test_overlap.tif", 
    stat = "max", 
    out_table = None
)

# Mask islands.  

wbt.set_nodata_value(
    i = out + "_12_island_test_overlap.tif", 
    output = out +"_13_not_islands.tif", 
    back_value=0.0, 
)

# Re-clump valley bottoms without islands to identify individual objects. 

wbt.clump(
    i = out +"_13_not_islands.tif", 
    output = out + "_14_not_island_clumps.tif", 
    diag=True, 
    zero_back=True
)

# ------------------------------------------------------------------------------
# Step 2. Select corridors. 
# ------------------------------------------------------------------------------

# Set background of blocks to no data. 

wbt.set_nodata_value(
    i = out + "_11_blocks_extra_edge.tif", 
    output = out + "_21_blocks_extra_edge_masked.tif", 
    back_value=0.0, 
)

# Identify unique blocks. 

wbt.clump(
    i = out + "_21_blocks_extra_edge_masked.tif", 
    output = out + "_22_blocks_extra_edge_objects.tif", 
    diag=True, 
    zero_back=True
)

# Test for min of overlap.

wbt.zonal_statistics(
    i = out + "_22_blocks_extra_edge_objects.tif", 
    features = out + "_14_not_island_clumps.tif", 
    output= out + "_23_valley_blocks_overlap_min.tif", 
    stat="min", 
    out_table=None, 
)

# Test for max of overlap.

wbt.zonal_statistics(
    i = out + "_22_blocks_extra_edge_objects.tif", 
    features = out + "_14_not_island_clumps.tif", 
    output= out + "_24_valley_blocks_overlap_max.tif", 
    stat="max", 
    out_table=None, 
)

# Corridors (tombolos) will have unequal min and max values, 
# Dead ends (spits) will have equal min and max values. 

wbt.not_equal_to(
    input1 = out + "_24_valley_blocks_overlap_max.tif", 
    input2 = out + "_23_valley_blocks_overlap_min.tif", 
    output = out + "_25_valley_corridors_test.tif", 
)

# Unmask background values. 

wbt.convert_nodata_to_zero(
    i = out + "_25_valley_corridors_test.tif", 
    output = out + "_26_valley_corridors_test_bg_0.tif"
)

# Select valley bottom corridors. 

wbt.zonal_statistics(
    i = out + "_26_valley_corridors_test_bg_0.tif", 
    features = out + "_14_not_island_clumps.tif", 
    output =  out +"_27_valley_connectors.tif", 
    stat="max", 
    out_table=None
)

# Make binary without background mask.  

wbt.convert_nodata_to_zero(
    i = out + "_27_valley_connectors.tif", 
    output = out + "_28_valley_connectors_binary.tif", 
    # callback=default_callback
)

# ------------------------------------------------------------------------------
# Step 3. Check connectivity of the network.  
# ------------------------------------------------------------------------------

wbt.Or(
    input1 = out + "_28_valley_connectors_binary.tif", 
    input2 = blocks, 
    output = out + "_31_union_blocks_corridors.tif", 
    # callback=default_callback
)

wbt.clump(
    i = out + "_31_union_blocks_corridors.tif", 
    output = out + "_32_network_groups.tif", 
    diag=True, 
    zero_back=True
)