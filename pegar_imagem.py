import arcpy

mxd = arcpy.mapping.MapDocument('Current')


#Selecionar a edificacao
def make_image(selo):
    #arcpy.SelectLayerByAttribute_management("RFPM_Edificacoes_dwg_Polygon","NEW_SELECTION",'"Elevation"=%s' % selo)
    
    for df in arcpy.mapping.ListDataFrames(mxd):
        outfile = r'C:\Documents and Settings\\rcls\\Meus documentos\\ArcGIS\\MXD\\Output'+ '\\' + selo + '.jpg'
        df.zoomToSelectedFeatures()
        arcpy.mapping.ExportToJPEG(mxd, outfile, df)


if __name__ == '__main__':
    make_image("103012")
    



    
