#encoding=utf-8
import arcpy, os
# The path to the registered folder where the template MXDs reside
folderPath = u"E:/智慧惠州/template/USA"
# The location of TemplateData.gdb within the registered folder
newPath = u"E:/智慧惠州/template/USA/TemplateData.gdb"
# Loop through all MXDs in the specified folder and change the layer's data source to the new path
for filename in os.listdir(folderPath):
    fullpath = os.path.join(folderPath, filename)
    if os.path.isfile(fullpath):
        basename, extension = os.path.splitext(fullpath)
        if extension.lower() == ".mxd":
            mxd = arcpy.mapping.MapDocument(fullpath)
            mxd.findAndReplaceWorkspacePaths(arcpy.mapping.ListLayers(mxd)[1].workspacePath, newPath)
            mxd.save()
            print(fullpath)
print "done"