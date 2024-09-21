from mda_core.time import Time
from org.orekit.utils import IERSConventions
from org.orekit.frames import FramesFactory

time_string = "2024-08-29T12:42:00"
EOP=FramesFactory.getEOPHistory(IERSConventions.IERS_2010,False)
LOD = EOP.getLOD(Time(time_string).get_absolutedate())
dUT1 = EOP.getUT1MinusUTC(Time(time_string).get_absolutedate())
Xp = EOP.getPoleCorrection(Time(time_string).get_absolutedate()).getXp()
Yp = EOP.getPoleCorrection(Time(time_string).get_absolutedate()).getYp()
Nuta = EOP.getEquinoxNutationCorrection(Time(time_string).get_absolutedate())
dXdY = EOP.getNonRotatinOriginNutationCorrection(Time(time_string).get_absolutedate())

print(LOD)
print(dUT1)
print(Xp)
print(Yp)
print(Nuta)
print(dXdY)