import arcpy
import os
import uuid

# Input WebMap json
Web_Map_as_JSON = arcpy.GetParameterAsText(0)

# The template location in the server data store
templateMxd = r"E:\ÖÇ»Û»ÝÖÝ\template\ExportWebMapTemplates\A3 Landscape.mxd"

# Convert the WebMap to a map document
result = arcpy.mapping.ConvertWebMapToMapDocument(Web_Map_as_JSON, templateMxd)
mxd = result.mapDocument

# Reference the data frame that contains the webmap
# Note: ConvertWebMapToMapDocument renames the active dataframe in the template_mxd to "Webmap"
df = arcpy.mapping.ListDataFrames(mxd, 'Webmap')[0]

# Remove the service layer
# This will just leave the vector layers from the template
for lyr in arcpy.mapping.ListLayers(mxd, data_frame=df):
    if lyr.isServiceLayer:
        arcpy.mapping.RemoveLayer(df, lyr)

# Use the uuid module to generate a GUID as part of the output name
# This will ensure a unique output name
output = 'WebMap1_{}.pdf'.format(str(uuid.uuid1()))
Output_File = os.path.join(arcpy.env.scratchFolder, output)

# Export the WebMap
arcpy.mapping.ExportToPDF(mxd, Output_File)

# Set the output parameter to be the output file of the server job
arcpy.SetParameterAsText(1, Output_File)

# Clean up - delete the map document reference
filePath = mxd.filePath
del mxd, result
os.remove(filePath)