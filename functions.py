#!/usr/bin/python2.7

import rrdtool
import os.path
from pycgminer import CgminerAPI

def getCgminerFactory():
    return CgminerAPI()

def getSummary():
    summary = getCgminerFactory().summary()
    summary = summary['SUMMARY']
    summary = summary[0]

    return summary

def getPoolCount():
    cgm = getCgminerFactory()

    poolCount = cgm.config()
    poolCount = poolCount['CONFIG']
    poolCount = poolCount[0]['Pool Count']

    return poolCount

def getASICDevicesCount():
    cgm = getCgminerFactory()

    ascCount = cgm.config()
    ascCount = ascCount['CONFIG']
    ascCount = ascCount[0]['ASC Count']

    return ascCount

def getASICDevice(device=None):
    if device is not None:
        asc = getCgminerFactory().asc(device)
        device = asc['ASC'][0]

    return device

def getCoin():
   cgm = getCgminerFactory()

   coin = cgm.coin()
   coin = coin['COIN']
   coin = coin[0]

   return coin

def generateTemplate(attributes=None):
    if attributes is None:
        print 'Nono'
    else:
        seperator = ':'
        template = seperator.join(attributes)
        #for index, item in enumerate(attributes):
        #    print index, item

    return template

def generateRRA():
    rra = [
        'RRA:MIN:0.5:1:1500',
        'RRA:MAX:0.5:1:1500',
        'RRA:AVERAGE:0.5:1:1500'
        ]

    return rra
