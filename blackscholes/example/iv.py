from blackscholes import BSModel
import numpy as np
BS = BSModel([])

bs = BS(1220, 22/365, 2.2719/100, 0, "C", price=36, spot=1240)
print(bs)
print(bs.vol)

bs = BS(1220, 22/365, 2.2719/100, 0, "C", price= np.array([36, 70]), spot=np.array([1240,1243]))
print(bs)
print(bs.vol)