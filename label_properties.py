import arcpy
mxd = arcpy.mapping.MapDocument("CURRENT")

def show_label():
    for lyr in arcpy.mapping.ListLayers(mxd):
        if lyr.longName == 'polylines':
            lyr.showLabels = True
            default = lyr.labelClasses[0]
            default.expression = '"%s" & Round([Shape_Leng], 2) & "%s"' %("<BOL><FNT name='Arial' size='18'>","</FNT></BOL>")
            break

    arcpy.RefreshActiveView()
#del mxd
