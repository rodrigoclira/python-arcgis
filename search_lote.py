#Procura o lote da edificacao

import arcpy
cur_edificacao  = arcpy.SearchCursor('RFPM_Edificacoes_dwg_Polygon')
cur_lote = arcpy.SearchCursor('RFPM_Lotes')
flag = False
for edificacao in cur_edificacao:
    if int(row.getValue('Elevation')) == 103012:
	poligono = row.getValue('Shape')
        centroide = poligono.centroid
        if flag:
            break
	for lote in cur_lote:
            pol_lote = lote.getValue("Shape")
            if pol_lote.contains(centroide):
                print "FID do LOTE", lote.getValue("FID")
                print "Area", pol_lote.area
                print "Pontos", pol_lote.getPart()
                for array in pol_lote.getPart():
                    for ponto in array:
                        print ponto
                flag = True
                break
            
