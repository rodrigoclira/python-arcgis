#-*- coding: utf-8 -*-
import arcpy
from glob import glob
from math import sqrt
from os import remove
#from pegar_imagem import make_image
#from label_properties import show_label
distancia_pontos = lambda p1,p2 : sqrt((p1.X - p2.X)**2 + (p1.Y - p2.Y)**2)
agrupar_pontos = lambda pontos : zip(pontos,pontos[1:])

edificacoes = []

def show_label():
    mxd = arcpy.mapping.MapDocument('Current')
    for lyr in arcpy.mapping.ListLayers(mxd):
        if lyr.longName == 'polylines':
            lyr.showLabels = True
            default = lyr.labelClasses[0]
            default.expression = '"%s" & Round([Shape_Leng], 2) & "%s"' %("<BOL><FNT name='Arial' size='18'>","</FNT></BOL>")
            break

    arcpy.RefreshActiveView()


#Selecionar a edificacao
def make_image(selo):
    mxd = arcpy.mapping.MapDocument('Current')
    #Selos Repetidos
    #arcpy.SelectLayerByAttribute_management("RFPM_Edificacoes_dwg_Polygon","NEW_SELECTION",'"Elevation"=%d' % selo)
    for df in arcpy.mapping.ListDataFrames(mxd):
        outfile = r'C:\Documents and Settings\\rcls\\Meus documentos\\ArcGIS\\MXD\\Output'+ '\\' + str(selo) + '.jpg'
        df.zoomToSelectedFeatures()
        arcpy.mapping.ExportToJPEG(mxd, outfile, df)

class Edificacao():
    def __init__(self, selo_edificacao, lote, edificacao):
        self.selo_edificacao = int(selo_edificacao)
        self.lote = lote
        self.edificacao = edificacao
        self.pontos = []
        self.fi = 0
        self.referencias = []
        print 'SELF.EDIFICACAO', self.edificacao
        for array in self.lote.getPart():
            for ponto in array:
                self.pontos.append(ponto)
        
        self.pontos_distancia = []

    def centroide_lote(self):
        return self.lote.centroid
    def area_lote(self):
        return self.lote.area

    def area_edificacao(self):
        return self.edificacao.area

    def calcular_distancia_entre_pontos(self):
        pontos_agrupados = agrupar_pontos(self.pontos)
        for ponto in pontos_agrupados:
            distancia = distancia_pontos(ponto[0], ponto[1])
            self.pontos_distancia.append((ponto[0], ponto[1], distancia))

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

    def criar_contorno(self):
        if self.pontos_distancia:
            array = arcpy.Array()
            featuredList = []
            for linha in self.pontos_distancia:
                array.append(linha[0])
                array.append(linha[1])
                line = arcpy.Polyline(array)
                featuredList.append(line)
                array.removeAll()
            files = glob(r"C:\Documents and Settings\rcls\Meus documentos\ArcGIS\MXD\linhas\*")
            for arquivo in files:
                remove(arquivo)
            flag = True
            while flag:
                try:
                    arcpy.CopyFeatures_management(featuredList, r"C:\Documents and Settings\rcls\Meus documentos\ArcGIS\MXD\linhas\polylines.shp")
                    flag = False
                except Exception as e:
                    print e.message
        show_label()
        
    def criar_image(self):
        make_image(self.selo_edificacao)

    def encontrar_confrontantes(self):
        proximos = self.calcular_proximidade()
        array_proximidade = []
        self.confrontantes = []
        pos = 0
        cur_referencia = arcpy.SearchCursor('referencia_final',"","","")
        for referencia in cur_referencia:
            elevation = referencia.getValue('Elevation_')
            if elevation == self.selo_edificacao:
                ponto = referencia.getValue('Shape')
                array_proximidade = []
                print "SELO: ", self.selo_edificacao, "Proximos: ", proximos
                for info in proximos[1:]:
                    pos = info[0]
                    print "Ponto: ",ponto, "Centroid: ",ponto.centroid
                    proximidade = distancia_pontos(ponto.centroid, edificacoes[pos].edificacao.centroid)
                    array_proximidade.append((pos, proximidade))
                print "array proximidade:",array_proximidade
                array_proximidade.sort(lambda x,y: cmp(x[-1],y[-1]))
                print "array proximidade:",array_proximidade
                pos = array_proximidade[0][0]
                posicao = referencia.getValue('posicao')
                self.confrontantes.append((posicao, edificacoes[pos]))
                               
    def calcular_proximidade(self):
        array_proximidade = []
        for pos, ed in enumerate(edificacoes):
            proximidade = distancia_pontos(self.edificacao.centroid, ed.edificacao.centroid)
            array_proximidade.append((pos, ed.selo_edificacao, proximidade))
        array_proximidade.sort(lambda x,y: cmp(x[-1],y[-1]))
        return array_proximidade



        
def inserir_referencias():
    print 'teste'
#    cur_referencia = arcpy.SearchCursor('referencia_final',"","","")
    print 'teste'
    for referencia in cur_referencia:
        elevation = referencia.getValue('Elevation_')
        for edificacao in edificacoes:
            if edificacao.selo_edificacao == elevation:
                posicao = referencia.getValue('posicao')
                ponto = referencia.getValue('Shape')
                edificacao.referencias.append((ponto, posicao))
                break   

def load():  
    cur_edificacao = arcpy.SearchCursor("edificacoes_final","","","")
    for edificacao in cur_edificacao:
        elevation_2 = edificacao.getValue("Elevatio_2") # Encotrar o lote que ele está contido
        cur_lote = arcpy.SearchCursor('lotes',"","","")
        #cur_lote = arcpy.SearchCursor('lotes',"","","Shape; Elevation")
        for lote in cur_lote:
            elevation = lote.getValue('Elevation')
            if elevation == elevation_2:
                print 'elevation: ',elevation, 'elevation 2: ', elevation_2
                lshape = lote.getValue('Shape')
                objectid = edificacao.getValue('OBJECTID')
                eshape = edificacao.getValue("Shape")
                print 'Eshape', eshape
                edificacoes.append(Edificacao(objectid, lshape, eshape))
                break
            

if __name__== '__main__':
    load()
    ed = edificacoes[0]
#    ed.encontrar_confrontantes()
    #inserir_referencias()
    #ed = edificacoes[1]
    #print ed.referencias
    #ed.encontrar_confrontantes()
    #cur_referencia = arcpy.SearchCursor('referencia_final',"","","")
    #for referencia in cur_referencia:
    #    elevation = referencia.getValue('Elevation_')
    #    ponto = referencia.getValue('Shape')
    #    print elevation,ponto, ponto.centroid
