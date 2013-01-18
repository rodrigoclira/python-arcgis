import arcpy
mxd = arcpy.mapping.MapDocument("CURRENT")
for lyr in arcpy.mapping.ListLayers(mxd):
    if lyr.longName == 'polylines':
        lyr.showLabels = True
        print 'Chegou'
del mxd
