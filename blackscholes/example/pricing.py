from blackscholes import BSModel
import numpy as np
BS = BSModel([])
bs = BS(1220, 22/365, 2.2719/100, 0, "C", vol= 0.2, spot=1240)
print(bs)
print(bs.price)

bs = BS(1220, 22/365, 2.2719/100, 0, "C", vol= np.array([0.2,0.3]), spot=1240)
print(bs)
print(bs.price)

bs = BS(1220, 22/365, 2.2719/100, 0, "C", vol= np.array([0.2,0.5]), spot=np.array([1240,1243]))
print(bs)
print(bs.price)