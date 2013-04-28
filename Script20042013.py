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
DEBUG = False
def generate_info():
    cur_edificacao = arcpy.SearchCursor("edificacoes_final","","","")
    
    for edificacao in cur_edificacao:
        elevation_2 = edificacao.getValue("Elevatio_2") # Encotrar o lote que ele está contido
        cur_lote = arcpy.SearchCursor('lotes',"","","")
        for lote in cur_lote:
            elevation = lote.getValue('Elevation')
            if elevation == elevation_2:
                #print 'elevation: ',elevation, 'elevation 2: ', elevation_2
                lshape = lote.getValue('Shape')
                selo = edificacao.getValue('OBJECTID')
                eshape = edificacao.getValue("Shape")
                print 'Eshape', eshape
                #INICIO DA MANIPULACAO#
                pontos = []
                pontos_agrupados = []
                pontos_distancia = []
                confrontantes = []
                for array in lshape.getPart():
                    for ponto in array:
                        pontos.append(ponto)
#                print pontos
                referencias  = filter(lambda (x,y,z,w):  int(x) == int(selo),REFERENCIAS)

                #Distancia dos lados
                pontos_agrupados = agrupar_pontos(pontos)
                for ponto in pontos_agrupados:
                    distancia = distancia_pontos(ponto[0], ponto[1])
                    pontos_distancia.append((ponto[0], ponto[1], distancia))                

                #Confrontantes
                """
                for referencia in referencias:
                    cur2_edificacao = arcpy.SearchCursor("edificacoes_final","","","")
                    array_distancia = []
                    print referencia
                    for ed in cur2_edificacao:
                        objectid = ed.getValue('OBJECTID')
                        if (objectid != selo):  
                            ed_shape = ed.getValue('shape')
                            distancia = distancia_pontos(referencia[1].centroid, ed_shape.centroid)
                            array_distancia.append((objectid, distancia))
                    array_distancia.sort(lambda x,y: cmp(x[-1],y[-1]))
                    print array_distancia
                    confrontantes.append((referencia[-1], array_distancia[0][0]))
                """
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
        elevation = referencia.getValue('Elevation_')
        cur_edificacao = arcpy.SearchCursor("lotes","","","")
        distancia = 0
        array_distancia = []
        for ed in cur_edificacao:            
            objectid = ed.getValue('OBJECTID')
            if (objectid != elevation):
                ed_shape = ed.getValue('shape')
                distancia = distancia_pontos(shape.centroid, ed_shape.centroid)
                array_distancia.append((objectid, distancia))
                array_distancia.sort(lambda x,y: cmp(x[-1],y[-1]))
        REFERENCIAS.append((elevation, shape, posicao, array_distancia[0][0]))
    print REFERENCIAS
    
if __name__ == '__main__':
    load_referencias()
    generate_info()
