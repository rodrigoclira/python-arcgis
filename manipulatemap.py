import arcpy
mxd = arcpy.mapping.MapDocument('Current')

for df in arcpy.mapping.ListDataFrames(mxd):
	df.rotation = 0
	df.scale = 10000
	outfile = r'C:\Documents and Settings\\rcls\\Meus documentos\\ArcGIS\\MXD\\Output'+ '\\' + df.name + '.tif'
	arcpy.mapping.ExportToTIFF(mxd, outfile, df)
	
del mxd