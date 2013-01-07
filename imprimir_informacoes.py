#-*- coding: utf-8 -*-
import arcpy


distancia_pontos = lambda p1,p2 : sqrt((p1.X - p2.X)**2 - (p1.Y - p2.Y)**2)

class Resultado():
    def __init__(self, selo_edificacao, lote, edificacao):
        self.selo_edificacao = int(selo_edificacao)
        self.lote = lote
        self.edificacao = edificacao

    def area_lote(self):
        return self.lote.area

    def area_edificacao(self):
        return self.edificacao.area

    def __str__(self):
        retorno = "Selo: " + str(self.selo_edificacao) + "\n"
        retorno += "Área do lote: " + str(self.area_lote()) + "\n"
        retorno += "Pontos do lote\n"
        
        for array in self.lote.getPart():
            for ponto in array:
                retorno += str(ponto) + "\n"
        return retorno
    

#Procura o lote da edificacao
def procurar_lote(edificacao):
    cur_lote = arcpy.SearchCursor('RFPM_Lotes')
    pol_edificacao = edificacao.getValue('Shape')
    res = None
    for lote in cur_lote:
        pol_lote = lote.getValue("Shape")
        if pol_lote.contains(pol_edificacao.centroid):
            elevation = edificacao.getValue('Elevation')
            res = Resultado(elevation, pol_lote, pol_edificacao)
#            for array in pol_lote.getPart():
#                for ponto in array:
#                    print ponto
            break
    del(cur_lote)
    return res
    

if __name__ == '__main__':
    cur_edificacao  = arcpy.SearchCursor('RFPM_Edificacoes_dwg_Polygon')
    for edificacao in cur_edificacao:
        elevation = int(edificacao.getValue('Elevation'))
        FID = int(edificacao.getValue('FID'))  
        if (elevation > 0) and (FID != 66) and (FID > 0 and FID <113):
            print procurar_lote(edificacao)
            
