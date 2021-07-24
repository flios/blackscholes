from blackscholes import BSModel
import numpy as np
BS = BSModel()
bs = BS(1220, 22/365, 2.2719/100, 0, "C", vol= 0.2, spot=1240)
print(bs.price)
print(bs.delta)

bs.fix_vol.spot = 1250
print(bs.price)
print(bs.delta)

bs.fix_price.tte = 0.01
print(bs.vol)

bs.fix_vol.spot = np.array([1250,1260])
print(bs.price)

bs.fix_price.spot = np.array([1220,1230])
print(bs.vol)
