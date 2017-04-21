import Util
import time
from scripts.ILO4.Ilo_Memory_Temperature import Ilo_Memory_Temperature
cf = Util.initialiseConfiguration()
s = Util.initialiseSession(cf)

k = Ilo_Memory_Temperature(cf)
val = k.get("ilo","node0","proc1.dimm8","Temperature")

print(val)
