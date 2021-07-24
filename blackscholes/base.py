from typing import Sequence
import numpy as np


base_properties=[
    "price",
    "vol",
    "spot",
    "strike",
    "tte",
    "ir",
    "div"
]

def base_getter(key:str):
    def getter(self):
        return getattr(self, f"_{key}")
    return getter

def base_setter(key:str):
    def setter(self, value):
        return setattr(self, f"_{key}", value)
    return setter

def base_repr(greeks:Sequence[str]):
    def repr(self):
        keys = [*base_properties, *greeks]
        values = [f"{k}:{getattr(self,k)}" for k in keys]
        output = f"{self.__class__.__name__}("+",".join(values) + ")"
        return output
    return repr

class PricingMetaClass(type):
    def __new__(cls, name, bases, attrs, getter_generator=base_getter, setter_generator=base_setter, greeks=["delta","gamma","vega","theta","rho","vanna","charm","vomma","speed","zomma",]):        

        for v in greeks:
            if v not in attrs:
                attrs[v] =  property(getter_generator(v))
                attrs[f"_{v}"] = np.nan
        for v in base_properties:
            if v not in attrs:
                attrs[v] =  property(getter_generator(v), setter_generator(v))
                attrs[f"_{v}"] = np.nan
        attrs["__repr__"] = base_repr(greeks)

        return super().__new__(cls, name, bases, attrs)

def PricingModelBase(greeks=["delta","gamma","vega","theta","rho","vanna","charm","vomma","speed","zomma",], getter_generator=base_getter, setter_generator=base_setter):
    class Model(metaclass=PricingMetaClass, getter_generator=getter_generator, setter_generator=setter_generator, greeks=greeks):
        def __init__(self, strike, tte, ir, div, option_type, spot, price=np.nan, vol=np.nan):
            self._strike = strike
            self._tte = tte
            self._ir = ir
            self._div = div
            self._vol = vol
            self._price = price
            self._spot = spot
            self.option_type = option_type
            self._is_call = self.option_type.upper() in ["C","CALL"]

        @property
        def float_vol(self):
            self.vol = np.nan
            return self

        @property
        def fix_price(self):
            self.vol = np.nan
            return self

        @property
        def float_price(self):
            self.price = np.nan
            return self

        @property
        def fix_vol(self):
            self.price = np.nan
            return self

        @property
        def is_call(self):
            return self._is_call

        @property
        def price(self):
            if np.isnan(self._price):
                self._update_values()
            return self._price

        @price.setter
        def price(self, value):
            if not np.isnan(value):
                self._vol = np.nan
            self._price = value

        @property
        def vol(self):
            if np.isnan(self._vol):
                self._update_values()
            return self._vol

        @vol.setter
        def vol(self, value):
            if not np.isnan(value):
                self._price = np.nan
            self._vol = value


        def _update_values(self):
            if np.any(np.isnan(self._vol)):
                self._cal_iv()
                self._update_greeks()
            elif np.any(np.isnan(self._price)):
                self._cal_price()
                self._update_greeks()
            else:
                pass

        def _cal_iv(self):
            self._vol = np.nan

        def _cal_price(self):
            self._price = np.nan

        def _update_greeks(self):
            if getattr(self.__class__, "_delta", None) is not None:
                self._update_delta()
            if getattr(self.__class__, "_gamma", None) is not None:
                self._update_gamma()
            if getattr(self.__class__, "_vega", None) is not None:
                self._update_vega()
            if getattr(self.__class__, "_rho", None) is not None:
                self._update_rho()
            if getattr(self.__class__, "_theta", None) is not None:
                self._update_theta()
            if getattr(self.__class__, "_vanna", None) is not None:
                self._update_vanna()
            if getattr(self.__class__, "_charm", None) is not None:
                self._update_charm()
            if getattr(self.__class__, "_vomma", None) is not None:
                self._update_vomma()
            if getattr(self.__class__, "_speed", None) is not None:
                self._update_speed()
            if getattr(self.__class__, "_zomma", None) is not None:
                self._update_zomma()

        def _update_delta(self):
            self._delta = np.nan

        def _update_gamma(self):
            self._gamma = np.nan

        def _update_vega(self):
            self._vega = np.nan

        def _update_theta(self):
            self._theta = np.nan

        def _update_rho(self):
            self._rho = np.nan

        def _update_vanna(self):
            self._vanna = np.nan

        def _update_charm(self):
            self._charm = np.nan

        def _update_vomma(self):
            self._vomma = np.nan

        def _update_speed(self):
            self._speed = np.nan

        def _update_zomma(self):
            self._zomma = np.nan

    return Model