#distancia entre dois pontos em UTM
#http://forums.groundspeak.com/GC/index.php?showtopic=146917
from math import sqrt

distancia_pontos = lambda p1,p2 : sqrt((p1.X - p2.X)**2 - (p1.Y - p2.Y)**2)

