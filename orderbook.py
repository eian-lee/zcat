from defines import ASK, BID
from collections import OrderedDict as od
# class Access(object):
    
#     def __init__(self, name=None, asks=None, bids=None):
#         self._name = name
#         self._asks = asks or od()
#         self._bids = bids or od()
        
#     @property
#     def name(self):
#         return self._name
    
#     @name.setter
#     def name(self, name):
#         self._name = name

class Meter(object):
    '''meter에 대한 디스크립터 '''

    def __init__(self, value=0.0):
        self.value = float(value)
    def __get__(self, instance, owner):
        return self.value
    def __set__(self, instance, value):
        self.value = float(value)

class Foot(object):
    '''footer에 대한 디스크립터'''

    def __get__(self, instance, owner):
        return instance.meter * 3.2808
    def __set__(self, instance, value):
        instance.meter = float(value) / 3.2808

class Distance(object):
    '''feet 와 meter에 대한 두 개의 디스크립터를 나타내는 클래스입니다.'''
    meter = Meter()
    foot = Foot()
    