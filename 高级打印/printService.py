#encoding=utf-8
import arcpy
import os
import uuid

# The template location in the registered folder (as UNC path)
templatePath = r'E:\zhhz_wks\template\USA'
# Input WebMap json
Web_Map_as_JSON ='{"mapOptions":{"showAttribution":true,"extent":{"xmin":12531164.393143252,"ymin":2551720.445752619,"xmax":13000793.49492715,"ymax":2757183.177783074,"spatialReference":{"wkid":102100}},"spatialReference":{"wkid":102100},"scale":740000},"operationalLayers":[{"id":"baseMap_2","title":"baseMap_2","opacity":1,"minScale":0,"maxScale":0,"type":"WebTiledLayer","urlTemplate":"http://t0.tianditu.gov.cn/img_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=img&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILECOL={col}&TILEROW={row}&TILEMATRIX={level}&tk=cede75bb109d5e8048ebc21308b91e54","credits":""},{"id":"baseMap_2_1","title":"baseMap_2_1","opacity":1,"minScale":0,"maxScale":0,"type":"WebTiledLayer","urlTemplate":"http://t0.tianditu.gov.cn/cia_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=cia&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILECOL={col}&TILEROW={row}&TILEMATRIX={level}&tk=cede75bb109d5e8048ebc21308b91e54","credits":""},{"id":"194","title":"194","opacity":1,"minScale":0,"maxScale":0,"url":"http://localhost:6080/arcgis/rest/services/zhhz/%E6%83%A0%E5%B7%9E%E5%BA%95%E5%9B%BE/MapServer","layers":[{"id":19,"name":"省内驻地符号","layerDefinition":{"source":{"type":"mapLayer","mapLayerId":19}}},{"id":21,"name":"开发区符号","layerDefinition":{"source":{"type":"mapLayer","mapLayerId":21}}},{"id":23,"name":"东沙礁","layerDefinition":{"source":{"type":"mapLayer","mapLayerId":23}}},{"id":25,"name":"惠州色带","layerDefinition":{"source":{"type":"mapLayer","mapLayerId":25}}},{"id":27,"name":"省界","layerDefinition":{"source":{"type":"mapLayer","mapLayerId":27}}},{"id":28,"name":"市界","layerDefinition":{"source":{"type":"mapLayer","mapLayerId":28}}},{"id":29,"name":"县界","layerDefinition":{"source":{"type":"mapLayer","mapLayerId":29}}},{"id":30,"name":"仲恺区大亚湾区界线","layerDefinition":{"source":{"type":"mapLayer","mapLayerId":30}}},{"id":32,"name":"水系边线","layerDefinition":{"source":{"type":"mapLayer","mapLayerId":32}}},{"id":39,"name":"惠州市县界","layerDefinition":{"source":{"type":"mapLayer","mapLayerId":39},"drawingInfo":{"renderer":{"type":"classBreaks","field":"年末男性人口数","minValue":180407,"classBreakInfos":[{"classMaxValue":180407,"label":"180407.000000","description":"","symbol":{"color":[252,225,56,255],"outline":{"color":[255,255,255,255],"width":0.75,"type":"esriSLS","style":"esriSLSSolid"},"type":"esriSFS","style":"esriSFSSolid"}},{"classMaxValue":240693,"label":"180407.000001 - 240693.000000","description":"","symbol":{"color":[188,223,67,255],"outline":{"color":[255,255,255,255],"width":0.75,"type":"esriSLS","style":"esriSLSSolid"},"type":"esriSFS","style":"esriSFSSolid"}},{"classMaxValue":453047,"label":"240693.000001 - 453047.000000","description":"","symbol":{"color":[123,194,73,255],"outline":{"color":[255,255,255,255],"width":0.75,"type":"esriSLS","style":"esriSLSSolid"},"type":"esriSFS","style":"esriSFSSolid"}},{"classMaxValue":457175,"label":"453047.000001 - 457175.000000","description":"","symbol":{"color":[79,165,75,255],"outline":{"color":[255,255,255,255],"width":0.75,"type":"esriSLS","style":"esriSLSSolid"},"type":"esriSFS","style":"esriSFSSolid"}},{"classMaxValue":532128,"label":"457175.000001 - 532128.000000","description":"","symbol":{"color":[72,136,92,255],"outline":{"color":[255,255,255,255],"width":0.75,"type":"esriSLS","style":"esriSLSSolid"},"type":"esriSFS","style":"esriSFSSolid"}}],"classificationMethod":"esriClassifyNaturalBreaks"}}}},{"id":40,"name":"其他市区","layerDefinition":{"source":{"type":"mapLayer","mapLayerId":40}}}]}],"exportOptions":{"outputSize":[1200,1200],"dpi":300},"layoutOptions":{"titleText":"我的地图","authorText":"广东省地图院","scaleBarOptions":{},"legendOptions":{"operationalLayers":[{"id":"194","subLayerIds":[19,21,23,25,27,28,29,30,32,39,40]}]}}}'
# Format for output
Format ="JPG"
if Format == '#' or not Format:
    Format = "PDF"
# Input Layout template
# < OPTION
# value = "CentralUSA" > CentralUSA < / OPTION >
# < OPTION
# value = "ConterminuousUSA" > ConterminuousUSA < / OPTION >
# < OPTION
# value = "NortheasternUSA" > NortheasternUSA < / OPTION >
# < OPTION
# value = "NorthwesternUSA" > NorthwesternUSA < / OPTION >
# < OPTION
# value = "SouthernUSA" > SouthernUSA < / OPTION >
# < OPTION
# value = "SouthwesternUSA" > SouthwesternUSA < / OPTION >
# < OPTION
# value = "Landscape_03_A3_1" > Landscape_03_A3_1 < / OPTION >
Layout_Template = "Portrait_03_A3_1"
if  Layout_Template == '#' or not Layout_Template:
    Layout_Template = ""

# Extra parameter - georef_info
Georef_info = "True"
if Georef_info == '#' or not Georef_info:
    Georef_info = "True"
# Convert Georef_info string to boolean
if Georef_info.lower() == 'false':
    Georef_info_bol = False
elif Georef_info.lower() == 'true':
    Georef_info_bol = True
# Get the requested map document
templateMxd = os.path.join(templatePath, Layout_Template + '.mxd')
# Convert the WebMap to a map document
result = arcpy.mapping.ConvertWebMapToMapDocument(Web_Map_as_JSON, templateMxd)
mxd = result.mapDocument
# Reference the data frame that contains the webmap
# Note: ConvertWebMapToMapDocument renames the active dataframe in the template_mxd to "Webmap"
df = arcpy.mapping.ListDataFrames(mxd, 'Webmap')[0]
# Get a list of all service layer names in the map
serviceLayersNames = [slyr.name for slyr in arcpy.mapping.ListLayers(mxd, data_frame=df)
                      if slyr.isServiceLayer and slyr.visible and not slyr.isGroupLayer]
# Create a list of all possible vector layer names in the map that could have a corresponding service layer
vectorLayersNames = [vlyr.name for vlyr in arcpy.mapping.ListLayers(mxd, data_frame=df)
                     if not vlyr.isServiceLayer and not vlyr.isGroupLayer]
# Get a list of all vector layers that don't have a corresponding service layer
removeLayerNameList = [vlyrName for vlyrName in vectorLayersNames
                       if vlyrName not in serviceLayersNames]
# Remove all vector layers that don't have a corresponding service layer
# for lyr in arcpy.mapping.ListLayers(mxd, data_frame=df):
#     if not lyr.isGroupLayer \
#             and not lyr.isServiceLayer \
#             and lyr.name in removeLayerNameList \
#             and lyr.name in vectorLayersNames:
#         arcpy.mapping.RemoveLayer(df, lyr)

# Reference the legend in the map document 必须要求模板内有图例元素存在 否则报错
legendList=arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT")
#判断当前模板是否含有图例元素
if legendList:
    legend = legendList[0]
    # Get a list of service layers that are on in the legend because the incoming
    # JSON can specify which service layers/sublayers are on/off in the legend
    legendServiceLayerNames = [lslyr.name for lslyr in legend.listLegendItemLayers()
                               if lslyr.isServiceLayer and not lslyr.isGroupLayer]
    # Remove vector layers from the legend where the corresponding service layer
    # is also off in the legend
    for lvlyr in legend.listLegendItemLayers():
        if not lvlyr.isServiceLayer \
                and lvlyr.name not in legendServiceLayerNames \
                and not lvlyr.isGroupLayer \
                and lvlyr.name in vectorLayersNames:
            legend.removeItem(lvlyr)


# Remove all service layers
# This will leave only vector layers that had corresponding service layers

# for slyr in arcpy.mapping.ListLayers(mxd, data_frame=df):
#     if slyr.isServiceLayer:
#         arcpy.mapping.RemoveLayer(df, slyr)

# ConvertWebMapToMapDocument renames the active dataframe in the template_mxd to "Webmap".
# Lets rename it to something more meaningful.
df.name = Layout_Template
# Use the uuid module to generate a GUID as part of the output name
# This will ensure a unique output name
output = 'WebMap_{}.{}'.format(str(uuid.uuid1()), Format)
Output_File = os.path.join("E:\pycharm", output)
# Export the WebMap
if Format.lower() == 'pdf':
    arcpy.mapping.ExportToPDF(mxd, Output_File, georef_info=Georef_info_bol)
elif Format.lower() == 'png':
    arcpy.mapping.ExportToPNG(mxd, Output_File)
# Set the output parameter to be the output file of the server job
arcpy.SetParameterAsText(4, Output_File)
# Clean up - delete the map document reference
filePath = mxd.filePath
del mxd, result
os.remove(filePath)