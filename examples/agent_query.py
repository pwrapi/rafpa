import Util
import time
from scripts.ILO4.Ilo_Chassis_Power import Ilo_Chassis_Power
cf = Util.initialiseConfiguration()
s = Util.initialiseSession(cf)

k = Ilo_Chassis_Power(cf)
val = k.get("ilo","node0","Chassis","Power")

print(val)
