# Black Scholes model 

## Purpose 

1. Make a BS model for option pricing and IV calculation 
2. Make a simple and quick interface to see how price/iv/greeks change when any one of the input parameter changes.

## How to use 

### Requirements

* Numpy 

### Create Model

#### No Greeks (Quickly calculate price and IV)

```python
from blackscholes import BSModel
BS = BSModel([]) # [] stands for no geeks would be calculated
```

#### With Greeks

```python
from blackscholes import BSModel
BS = BSModel() # All suported geeks would be calculated including delta, gamma, vega, theta, rho, vanna, charm, vomma, speed, and zomma
```

```python
from blackscholes import BSModel
BS = BSModel(["delta, gamma"]) # Only delta and gamma would be calculated
```

For details of the greeks please see [Wikipedia Greeks](https://en.wikipedia.org/wiki/Greeks_(finance)) page 

### Pricing 

* One point

```python
from blackscholes import BSModel
import numpy as np
BS = BSModel([])
bs = BS(1220, 22/365, 2.2719/100, 0, "C", vol= 0.2, spot=1240)
print(bs.price)
```

* Vector

```python
from blackscholes import BSModel
import numpy as np
BS = BSModel([])
bs = BS(1220, 22/365, 2.2719/100, 0, "C", vol= np.array([0.2,0.5]), spot=np.array([1240,1243]))
print(bs.price)
```

### Calculate IV

* One point

```python
from blackscholes import BSModel
import numpy as np
BS = BSModel([])

bs = BS(1220, 22/365, 2.2719/100, 0, "C", price=36, spot=1240)
print(bs)
print(bs.vol)
```

* Vector

```python
from blackscholes import BSModel
import numpy as np
BS = BSModel([])
bs = BS(1220, 22/365, 2.2719/100, 0, "C", price= np.array([36, 70]), spot=np.array([1240,1243]))
print(bs)
print(bs.vol)
```

### Calculate Greeks 

* One point

```python
from blackscholes import BSModel
import numpy as np
BS = BSModel()
bs = BS(1220, 22/365, 2.2719/100, 0, "C", vol= 0.2, spot=1240)
print(bs.price)
print(bs.gamma)
print(bs.vega)
print(bs.theta)
print(bs.rho)
print(bs.vanna)
print(bs.charm)
print(bs.vomma)
print(bs.speed)
print(bs.zomma)
```

* Vector

```python
from blackscholes import BSModel
import numpy as np
BS = BSModel()
bs = BS(1220, 22/365, 2.2719/100, 0, "C", vol= np.array([0.2,0.5]), spot=np.array([1240,1243]))
print(bs.price)
print(bs.gamma)
print(bs.vega)
print(bs.theta)
print(bs.rho)
print(bs.vanna)
print(bs.charm)
print(bs.vomma)
print(bs.speed)
print(bs.zomma)
```

### Re-calculate

```python
from blackscholes import BSModel
import numpy as np
BS = BSModel()
bs = BS(1220, 22/365, 2.2719/100, 0, "C", vol= 0.2, spot=1240)
print(bs.price)
print(bs.delta)

bs.fix_vol.spot = 1250				# When volatility stays unchanged and the spot changes to 1250
print(bs.price)						# new price
print(bs.delta)						# new delta

bs.fix_price.tte = 0.01				# when price stays unchanged and time to expiry changes to 0.01 (year)
print(bs.vol)						# new implied volatility

bs.fix_vol.spot = np.array([1250,1260])
print(bs.price)

bs.fix_price.spot = np.array([1220,1230])
print(bs.vol)

```

