#!/usr/bin/env python

import functions
import rrdtool
import os.path
from pycgminer import CgminerAPI

'''
u'Difficulty Accepted': 325872.0, => 1
u'Temperature': 75.0, => 2
u'Difficulty Rejected': 15320.0, => 3
u'MHS 15m': 33277.93, => 4
u'Status': u'Alive', 
u'Device Rejected%': 4.3355, => 5
u'Rejected': 66, => 6
u'ID': 0,
u'ASC': 0,
u'Hardware Errors': 17630, => 7
u'Accepted': 1271, => 8
u'No Device': False,
u'Last Share Pool': 0, => 9
u'Diff1 Work': 353360, => 10
u'Name': u'LIN',
u'Total MH': 1517510207.0, => 11
u'Enabled': u'Y',
u'Device Hardware%': 4.7521, => 12
u'Last Valid Work': 1408429716, => 13
u'Last Share Time': 1408429628, => 14
u'Device Elapsed': 46324, => 15
u'MHS av': 32758.88, => 16
u'MHS 5s': 35309.89, => 17
u'Last Share Difficulty': 300.0, => 18
u'MHS 1m': 33025.23, => 19
u'MHS 5m': 33336.83, => 20
u'Utility': 1.65 => 21
'''

DEVICE_ATTRIBUTES = [
    'DifficultyAccepted',
    'Temperature',
    'DifficultyRejected',
    'MHS15m',
    'DeviceRejectedPct',
    'Rejected',
    'HardwareErrors',
    'Accepted',
    'LastSharePool',
    'Diff1Work',
    'TotalMH',
    'DeviceHardwarePct',
    'LastValidWork',
    'LastShareTime',
    'DeviceElapsed',
    'MHSav',
    'MHS5s',
    'LastShareDifficulty',
    'MHS1m',
    'MHS5m',
    'Utility'
    ]

DEVICES_COUNT = functions.getPoolCount()

def createDevice(rrd=None, dataSources=None, rra=None):
    if os.path.isfile(rrd) is False:
        dataSources = generateDeviceDataSources()
        print dataSources
        rra = functions.generateRRA()
        print rra
        rrdtool.create(rrd,
            '--step', '120',
            dataSources,
            rra)

def generateDeviceDataSources():
    dataSources = [
        'DS:DifficultyAccepted:GAUGE:120:0:U',
        'DS:Temperature:GAUGE:120:0:U',
        'DS:DifficultyRejected:GAUGE:120:0:U',
        'DS:MHS15m:GAUGE:120:0:U',
        'DS:DeviceRejectedPct:GAUGE:120:0:100',
        'DS:Rejected:GAUGE:120:0:U',
        'DS:HardwareErrors:GAUGE:120:0:U',
        'DS:Accepted:GAUGE:120:0:U',
        'DS:LastSharePool:GAUGE:120:0:U',
        'DS:Diff1Work:GAUGE:120:0:U',
        'DS:TotalMH:GAUGE:120:0:U',
        'DS:DeviceHardwarePct:GAUGE:120:0:100',
        'DS:LastValidWork:GAUGE:120:0:U',
        'DS:LastShareTime:GAUGE:120:0:U',
        'DS:DeviceElapsed:GAUGE:120:0:U',
        'DS:MHSav:GAUGE:120:0:U',
        'DS:MHS5s:GAUGE:120:0:U',
        'DS:LastShareDifficulty:GAUGE:120:0:U',
        'DS:MHS1m:GAUGE:120:0:U',
        'DS:MHS5m:GAUGE:120:0:U',
        'DS:Utility:GAUGE:120:0:U',
        ]

    return dataSources

def populateDevice(device=None, rrd=None):
    if device == None or rrd == None:
        if url is not None:
            rrd = 'DEVICE_UNK.rrd'
            createDevice(rrd)
    else:
        createDevice(rrd)
        template = functions.generateTemplate(attributes=DEVICE_ATTRIBUTES)

        device = functions.getASICDevice(device)
        readings = generateDeviceReadings(device)

        rrdtool.update(rrd,'--template', template, 'N:%s' % readings)


def generateDeviceReadings(readings=None):
    if readings is not None:
        separator = ':'
        sequence = (str(readings['Difficulty Accepted']),str(readings['Temperature']),str(readings['Difficulty Rejected']),str(readings['MHS 15m']),str(readings['Device Rejected%']),str(readings['Rejected']),str(readings['Hardware Errors']),str(readings['Accepted']),str(readings['Last Share Pool']),str(readings['Diff1 Work']),str(readings['Total MH']),str(readings['Device Hardware%']),str(readings['Last Valid Work']),str(readings['Last Share Time']),str(readings['Device Elapsed']),str(readings['MHS av']),str(readings['MHS 5s']),str(readings['Last Share Difficulty']),str(readings['MHS 1m']),str(readings['MHS 5m']),str(readings['Utility']))
        readings = separator.join(sequence)
    else:
        print 'FUCK'

    return readings
