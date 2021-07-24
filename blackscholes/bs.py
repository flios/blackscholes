from typing import overload
import numpy as np
from scipy.optimize import bisect, root
from scipy.stats import norm
from blackscholes.base import PricingMetaClass, PricingModelBase



def gen_getter(key:str):
    def getter(self):
        self._update_values()
        return getattr(self, f"_{key}")
    return getter

def BSModel(greeks=["delta","gamma","vega","theta","rho","vanna","charm","vomma","speed","zomma",]):
    BaseModel = PricingModelBase(greeks, getter_generator=gen_getter)
    class BS(BaseModel, metaclass=PricingMetaClass, getter_generator=gen_getter, greeks=greeks):
        def __init__(self, strike, tte, ir, div, option_type, spot, price=np.nan, vol=np.nan):
            super().__init__(strike, tte, ir, div, option_type, spot, price, vol)
            self._d1 = np.nan
            self._d2 = np.nan

        @property
        def pricing(self):
            return self._bs_call if self.is_call else self._bs_put

        @property
        def d1(self):
            return self._d1
        
        @property
        def d2(self):
            return self._d2
        
        def _cal_iv(self):
            try:
                price = np.array(self._price).reshape(1,-1).flatten()
                res = root(lambda x: self.pricing(x)-price, np.ones_like(price)*0.2)
                res = res.x
                if len(res)>1:
                    res = np.array(res)
                else:
                    res, = res
                self._d1, self._d2 = self._update_d(res)
                self._vol = res
            except:
                self._vol = np.nan


        def _cal_price(self):
            self._d1, self._d2 = self._update_d(self._vol)
            self._price = self.pricing(self._vol)

        def _bs_call(self, vol):
            d1, d2 = self._update_d(vol)
            df = np.exp(-self._ir*self._tte)
            div_dv = np.exp(-self._div*self._tte)
            return norm.cdf(d1)*self._spot*div_dv - norm.cdf(d2)*df*self._strike
        
        def _bs_put(self, vol):
            d1, d2 = self._update_d(vol)
            df = np.exp(-self._ir*self._tte)
            div_dv = np.exp(-self._div*self._tte)
            return norm.cdf(-d2)*df*self._strike - norm.cdf(-d1)*self._spot*div_dv

        def _update_d(self, vol):
            d1 = 1/(vol * np.sqrt(self._tte)) * (np.log(self._spot/self._strike)+1/2*(self._ir+vol**2/2)*(self._tte))
            d2 = d1-vol*np.sqrt(self._tte)
            return d1, d2


        def _update_delta(self):
            if self.is_call:
                self._delta = np.exp(-self.div*self.tte) * norm.cdf(self.d1) 
            else:
                self._delta =  -np.exp(-self.div*self.tte) * norm.cdf(-self.d1)

        def _update_gamma(self):
            self._gamma = np.exp(-self.div*self.tte) * norm.pdf(self.d1)/(self.spot * self.vol * np.sqrt(self.tte))

        def _update_vega(self):
            self._vega = np.exp(-self.div*self.tte) * self.spot * norm.pdf(self.d1) * np.sqrt(self.tte)

        def _update_theta(self):
            if self.is_call:
                self._theta = (
                    - np.exp(-self.div*self.tte)*(self.spot * norm.pdf(self.d1) * self.vol)/(2*np.sqrt(self.tte)) 
                    - (self.ir * self.strike * np.exp(-self.ir*self.tte)*norm.cdf(self.d2)) 
                    + self.div*self.spot*np.exp(-self.div*self.tte)*norm.cdf(self.d1))
            else:
                self._theta = (
                    - np.exp(-self.div*self.tte)*(self.spot * norm.pdf(self.d1) * self.vol)/(2*np.sqrt(self.tte)) 
                    + (self.ir * self.strike * np.exp(-self.ir*self.tte)*norm.cdf(-self.d2)) 
                    - self.div*self.spot*np.exp(-self.div*self.tte)*norm.cdf(-self.d1))

        def _update_rho(self):
            if self.is_call:
                self._rho = self.strike*self.tte*np.exp(-self.ir*self.tte)*norm.cdf(self.d2)
            else:
                self._rho = -self.strike*self.tte*np.exp(-self.ir*self.tte)*norm.cdf(-self.d2)

        def _update_vanna(self):
            self._vanna = -np.exp(-self.div*self.tte)*norm.pdf(self.d1)*self.d2/self.vol

        def _update_charm(self):
            if self.is_call:
                self._charm = self.div * np.exp(-self.div*self.tte) * norm.cdf(self.d1) - np.exp(-self.div*self.tte) * norm.pdf(self.d1) * (2*(self.ir-self.div)*self.tte - self.d2*self.vol*np.sqrt(self.tte))/(2*self.tte*self.vol*np.sqrt(self.tte))
            else:
                self._charm = -self.div * np.exp(-self.div*self.tte) * norm.cdf(-self.d1) - np.exp(-self.div*self.tte) * norm.pdf(self.d1) * (2*(self.ir-self.div)*self.tte - self.d2*self.vol*np.sqrt(self.tte))/(2*self.tte*self.vol*np.sqrt(self.tte))

        def _update_vomma(self):
            self._vomma = np.exp(-self.div*self.tte) * self.spot * norm.pdf(self.d1)*np.sqrt(self.tte)*self.d1*self.d2/self.vol

        def _update_speed(self):
            self._speed = -np.exp(-self.div*self.tte) * norm.pdf(self.d1)/(self.spot**2 * self.vol * np.sqrt(self.tte))*(self.d1/(self.vol * np.sqrt(self.tte))+1)

        def _update_zomma(self):
            self._zomma = np.exp(-self.div*self.tte) * norm.pdf(self.d1)*(self.d1*self.d2-1)/(self.spot**2 * self.vol * np.sqrt(self.tte))
    return BS
