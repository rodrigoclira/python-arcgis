# -*- coding: cp1252 -*-
#Script de entrega#
import arcpy
from glob import glob
from math import sqrt
from os import remove
distancia_pontos = lambda p1,p2 : sqrt((p1.X - p2.X)**2 + (p1.Y - p2.Y)**2)
agrupar_pontos = lambda pontos : zip(pontos,pontos[1:])



def calcular_distancia_entre_pontos():
    pontos_agrupados = agrupar_pontos(self.pontos)
    for ponto in pontos_agrupados:
        distancia = distancia_pontos(ponto[0], ponto[1])
        self.pontos_distancia.append((ponto[0], ponto[1], distancia))

INFO = {}
DEBUG = True
def generate_info():
    cur_edificacao = arcpy.SearchCursor("edificacoes_final","","","")
    
    for edificacao in cur_edificacao:
        ecod_lote = edificacao.getValue("Cod_Lote") # Encotrar o lote que ele está contido
        cur_lote = arcpy.SearchCursor('BPM_Lotes',"","","")
        for lote in cur_lote:
            lcod_lote = lote.getValue("Cod_Lote")
            if lcod_lote == ecod_lote:
                #print 'elevation: ',elevation, 'elevation 2: ', elevation_2
                lshape = lote.getValue('Shape')
                selo = edificacao.getValue('Cod_Imo')
                eshape = edificacao.getValue("Shape")
                #print 'Eshape', eshape
                #INICIO DA MANIPULACAO#
                pontos = []
                pontos_agrupados = []
                pontos_distancia = []
                confrontantes = []
                for array in lshape.getPart():
                    for ponto in array:
                        pontos.append(ponto)
#                print pontos
                referencias  = filter(lambda (x,y,z,w):  int(x) == int(ecod_lote), REFERENCIAS)

                #Distancia dos lados
                pontos_agrupados = agrupar_pontos(pontos)
                for ponto in pontos_agrupados:
                    distancia = distancia_pontos(ponto[0], ponto[1])
                    pontos_distancia.append((ponto[0], ponto[1], distancia))                

                #Confrontantes
                cur_referencia_final = arcpy.SearchCursor("referencia_final","","","posicao; Elevation_; Shape")
                for referencia in cur_referencia_final:
                    elevation_ = referencia.getValue("Elevation_")
                    if (elevation_ == lcod_lote):
                        cur2_edificacao = arcpy.SearchCursor("edificacoes_final","","","")
                        array_distancia = []
                        ponto = referencia.getValue("Shape")
                        posicao = referencia.getValue("posicao")
                        for ed in cur2_edificacao:
                            cod_imo = ed.getValue('Cod_Imo')
                            if (cod_imo != selo):  
                                ed_shape = ed.getValue('shape')
                                distancia = distancia_pontos(ponto.centroid, ed_shape.centroid)
                                array_distancia.append((cod_imo, distancia))
                        array_distancia.sort(lambda x,y: cmp(x[-1],y[-1]))
                        #print array_distancia
                        #print posicao
                        confrontantes.append((posicao, array_distancia[0][0]))
                
                if DEBUG:    
                    print "--- INFO ---"
                    print "Selo do imovel %d" % selo
                    print "Area Lote: %f" % lshape.area
                    print "Area Edificacao %f" % eshape.area
                    print "Centroid do lote", lshape.centroid
                    print "Centroid da edificacao", eshape.centroid
                    print "Pontos Distancia", pontos_distancia
                    print "Confrontantes", confrontantes
                    print "------------"
                    
                INFO[selo] = { "area_lote":lshape.area, "area_edificacao":eshape.area,
                              "centroid_lote":lshape.centroid, "centroid_edificacao":eshape.centroid,
                              "pontos_distancia":pontos_distancia, "confrontantes": confrontantes,
                               "referencias": referencias}
                break

            
REFERENCIAS = []
def load_referencias():
    cur_referencia_final = arcpy.SearchCursor("referencia_final","","","posicao; Elevation_; Shape")
    for referencia in cur_referencia_final:
        posicao = referencia.getValue('posicao')
        shape = referencia.getValue('Shape')
        cod_lote = referencia.getValue('Elevation_')
        cur_lote = arcpy.SearchCursor("BPM_Lotes","","","")
        distancia = 0
        array_distancia = []
        for lote in cur_lote:      
            cod_elote = lote.getValue('Cod_Lote')
            if (cod_elote != cod_lote):
                lote_shape = lote.getValue('shape')
                distancia = distancia_pontos(shape.centroid, lote_shape.centroid)
                array_distancia.append((cod_lote, distancia))
                array_distancia.sort(lambda x,y: cmp(x[-1],y[-1]))
        REFERENCIAS.append((cod_lote, shape, posicao, array_distancia[0][0]))
#    print REFERENCIAS
    
if __name__ == '__main__':
    #load_referencias()
    generate_info()
