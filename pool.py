#!/usr/bin/env python

import functions
import rrdtool
import os.path
from pycgminer import CgminerAPI

'''
u'Stratum Active': True,
u'Difficulty Accepted': 4483024.0, => 1
u'Pool Rejected%': 0.048, => 2
u'Difficulty Rejected': 2162.0, => 3
u'Diff1 Shares': 4462309, => 4
u'Status': u'Alive',
u'Proxy Type': u'',
u'Best Share': 4832793, => 7
u'Pool Stale%': 0.4586, => 8
u'Quota': 1, => 9
u'Rejected': 199, => 10
u'Stratum URL': u'rr.btcmp.com',
u'User': u'flow.worker',
u'Long Poll': u'N',
u'Accepted': 58883, => 14
u'Proxy': u'',
u'Get Failures': 22, => 16
u'Difficulty Stale': 20666.0, => 17
u'URL': u'http://rr.btcmp.com:3333',
u'Discarded': 816958, => 18
u'Has Stratum': True,
u'Last Share Time': 1407312374, => 20
u'Stale': 286, => 21
u'Works': 4459441, => 22
u'POOL': 0,
u'Priority': 0, => 24
u'Getworks': 13455, => 25
u'Has GBT': False,
u'Last Share Difficulty': 93.0, => 27
u'Remote Failures': 1 => 28
'''

POOL_ATTRIBUTES = [
    'DifficultyAccepted',
    'PoolRejectedPct',
    'DifficultyRejected',
    'Diff1Shares',
    'BestShare',
    'PoolStalePct',
    'Quota',
    'Rejected',
    'Accepted',
    'GetFailures',
    'DifficultyStale',
    'Discarded',
    'LastShareTime',
    'Stale',
    'Works',
    'Priority',
    'Getworks',
    'LastShareDifficulty',
    'RemoteFailures']

POOLS = functions.getCgminerFactory().pools()
POOLS_COUNT = functions.getPoolCount()

def createPool(rrd=None, dataSources=None, rra=None):
    if os.path.isfile(rrd) is False:
        dataSources = generatePoolDataSources()
        print dataSources
        rra = functions.generateRRA()
        print rra
        rrdtool.create(rrd,
            '--step', '120',
            dataSources,
            rra)

def generatePoolDataSources():
    dataSources = [
        'DS:DifficultyAccepted:GAUGE:120:0:U',
        'DS:PoolRejectedPct:GAUGE:120:0:100',
        'DS:DifficultyRejected:GAUGE:120:0:U',
        'DS:Diff1Shares:GAUGE:120:0:U',
        'DS:BestShare:GAUGE:120:0:U',
        'DS:PoolStalePct:GAUGE:120:0:100',
        'DS:Quota:GAUGE:120:0:U',
        'DS:Rejected:GAUGE:120:0:U',
        'DS:Accepted:GAUGE:120:0:U',
        'DS:GetFailures:GAUGE:120:0:U',
        'DS:DifficultyStale:GAUGE:120:0:U',
        'DS:Discarded:GAUGE:120:0:U',
        'DS:LastShareTime:GAUGE:120:0:U',
        'DS:Stale:GAUGE:120:0:U',
        'DS:Works:GAUGE:120:0:U',
        'DS:Priority:GAUGE:120:0:U',
        'DS:Getworks:GAUGE:120:0:U',
        'DS:LastShareDifficulty:GAUGE:120:0:U',
        'DS:RemoteFailures:GAUGE:120:0:U'
        ]

    return dataSources

def generatePoolRRA():
    rra = [
        'RRA:MIN:0.5:1:1500',
        'RRA:MAX:0.5:1:1500',
        'RRA:AVERAGE:0.5:1:1500'
        ]

    return rra

def populatePool(url=None, rrd=None):
    if url == None or rrd == None:
        if url is not None:
            rrd = 'POOL_UNK.rrd'
            createPool(rrd)
    else:
        createPool(rrd)
        template = functions.generateTemplate(attributes=POOL_ATTRIBUTES)

        i = 0
        while (i<POOLS_COUNT):
            pool = POOLS['POOLS'][i]
            if pool['URL'] == 'http://rr.btcmp.com:3333':
                readings = generatePoolReadings(pool)

                rrdtool.update(rrd,
                    '--template', template, 'N:%s' % readings)
            i = i+1

def generatePoolReadings(readings=None):
    if readings is not None:
        separator = ':'
        sequence = (str(readings['Difficulty Accepted']),str(readings['Pool Rejected%']),str(readings['Difficulty Rejected']),str(readings['Diff1 Shares']),str(readings['Best Share']),str(readings['Pool Stale%']),str(readings['Quota']),str(readings['Rejected']),str(readings['Accepted']),str(readings['Get Failures']),str(readings['Difficulty Stale']),str(readings['Discarded']),str(readings['Last Share Time']),str(readings['Stale']),str(readings['Works']),str(readings['Priority']),str(readings['Getworks']),str(readings['Last Share Difficulty']),str(readings['Remote Failures']))
        readings = separator.join(sequence)
    else:
        print 'FUCK'

    return readings
