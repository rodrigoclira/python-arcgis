#-*- coding: utf-8 -*-
import arcpy

from math import sqrt

distancia_pontos = lambda p1,p2 : sqrt((p1.X - p2.X)**2 + (p1.Y - p2.Y)**2)
agrupar_pontos = lambda pontos : zip(pontos,pontos[1:])                                                              

class Resultado():
    def __init__(self, selo_edificacao, lote, edificacao):
        self.selo_edificacao = int(selo_edificacao)
        self.lote = lote
        self.edificacao = edificacao
        self.pontos = []
        self.fi = 0
        for array in self.lote.getPart():
            for ponto in array:
                self.pontos.append(ponto)
        self.pontos_distancia = []
    def area_lote(self):
        return self.lote.area

    def area_edificacao(self):
        return self.edificacao.area
    
    def calcular_distancia_entre_pontos(self):
        pontos_agrupados = agrupar_pontos(self.pontos) # [1,2,3,4] = [(1,2),(2,3),(3,4)]
        
        for ponto in pontos_agrupados:
            distancia = distancia_pontos(ponto[0],ponto[1])
            self.pontos_distancia.append((ponto[0],ponto[1],distancia))
    
    def __str__(self):
        retorno = "Selo: " + str(self.selo_edificacao) + "\n"
        retorno += "Área do lote: " + str(self.area_lote()) + "\n"
        retorno += "Pontos do lote\n"
        
        for array in self.lote.getPart():
            for ponto in array:
                retorno += str(ponto) + "\n"
        return retorno
    
    def fracao_ideal(self):
        self.fi = (self.lote.area * self.edificacao.area) / float(self.edificacao.area)


        
#Procura o lote da edificacao
def procurar_lote(edificacao):
    cur_lote = arcpy.SearchCursor('RFPM_Lotes',"","","Shape")
    pol_edificacao = edificacao.getValue('Shape')
    res = None
    for lote in cur_lote:
        pol_lote = lote.getValue("Shape")
        if pol_lote.contains(pol_edificacao.centroid):
            elevation = edificacao.getValue('Elevation')
            res = Resultado(elevation, pol_lote, pol_edificacao)
            break
    del(cur_lote)
    return res
    

if __name__ == '__main__':
    cur_edificacao  = arcpy.SearchCursor('RFPM_Edificacoes_dwg_Polygon',"","","FID; Shape; Elevation")
    res= None
    for edificacao in cur_edificacao:
        elevation = int(edificacao.getValue('Elevation'))
        if elevation != 103012:
            continue
        FID = int(edificacao.getValue('FID'))  
        if (elevation > 0) and (FID != 66) and (FID > 0 and FID <113):
            res = procurar_lote(edificacao)
            print res
        break    
