import arcpy
curr  = arcpy.SearchCursor('RFPM_Edificacoes_dwg_Polygon')
cont = 10
for row in curr:
    if int(row.getValue('Elevation')) == 103012:
	print row.getValue('FID')
	poligono = row.getValue('Shape')
        entidade = row.getValue('Entity')
	break
