#encoding=utf-8
import arcpy
mxd = arcpy.mapping.MapDocument(r"C:\Users\Dell\Desktop\mxdfille\print.mxd")
arcpy.mapping.ExportToAI(mxd, r"C:\Users\Dell\Desktop\print\ProjectDataFrame.ai")
del mxd
