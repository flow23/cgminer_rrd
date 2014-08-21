#!/usr/bin/env python

import functions
import datetime
import rrdtool
import os.path
from pycgminer import CgminerAPI

'''
u'Hash Method': u'sha256',
u'Current Block Time': 1408543886.163499, => 1
u'Current Block Hash': u'000000000000000000a36bab71fa834231ea959391e37549785f12e29d08c498',
u'LP': True,
u'Network Difficulty': 23844670038.8033 => 2
'''

COIN_ATTRIBUTES = [
    'CurrentBlockTime',
    'NetworkDifficulty'
    ]

COIN = functions.getCoin()

def createCoin(rrd=None, dataSources=None, rra=None):
    if os.path.isfile(rrd) is False:
        dataSources = generateDataSources()
        print dataSources
        rra = functions.generateRRA()
        print rra
        rrdtool.create(rrd,
            '--step', '120',
            dataSources,
            rra)

def generateDataSources():
    dataSources = [
        'DS:CurrentBlockTime:GAUGE:120:0:U',
        'DS:NetworkDifficulty:GAUGE:120:0:U'
        ]

    return dataSources

def populateCoin(rrd=None):
    if rrd == None:
        rrd = 'COIN.rrd'
        createCoin(rrd)
    else:
        createCoin(rrd)
        template = functions.generateTemplate(attributes=COIN_ATTRIBUTES)

        readings = generateCoinReadings(COIN)

        rrdtool.update(rrd,
                    '--template', template, 'N:%s' % readings)

def generateCoinReadings(readings=None):
    if readings is not None:
        separator = ':'
        sequence = (str(readings['Current Block Time']),str(readings['Network Difficulty']))
        readings = separator.join(sequence)
    else:
        print 'FUCK'

    return readings

def createLastBlockTimeGraphs(rrd=None):
    watermark = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f - CEST")

    dictionary = {
        'COIN_CurrentBlockTime_1h.png' : '-1h',
        'COIN_CurrentBlockTime_12h.png' : '-12h',
        'COIN_CurrentBlockTime_1d.png' : '-1d',
        'COIN_CurrentBlockTime_1w.png' : '-1w',
        'COIN_CurrentBlockTime_1m.png' : '-1m'
    }

    for key, value in dictionary.iteritems():
        print key, value
        rrdtool.graph(key,
            '--imgformat', 'PNG',
            '--slope-mode',
            '--width', '500',
            '--height', '150',
            '--start', '%s' % value,
            '--end', 'now',
            '--vertical-label', 'Seconds',
            '--title', 'COIN - Current Block Time',
            '--alt-y-grid', '--rigid',
            '--watermark', watermark,
            'DEF:CurrentBlockTime=%s:CurrentBlockTime:AVERAGE' % rrd,
            'AREA:CurrentBlockTime#A4A4A4',
            'LINE1:CurrentBlockTime#000000:CurrentBlockTime',
            'GPRINT:CurrentBlockTime:LAST:Last\: %5.2lf',
            'GPRINT:CurrentBlockTime:MIN:Min\: %5.2lf',
            'GPRINT:CurrentBlockTime:AVERAGE:Avg\: %5.2lf',
            'GPRINT:CurrentBlockTime:MAX:Max\: %5.2lf'
            )

def createNetworkDifficultyGraphs(rrd=None):
    watermark = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f - CEST")

    dictionary = {
        'COIN_NetworkDifficulty_1h.png' : '-1h',
        'COIN_NetworkDifficulty_12h.png' : '-12h',
        'COIN_NetworkDifficulty_1d.png' : '-1d',
        'COIN_NetworkDifficulty_1w.png' : '-1w',
        'COIN_NetworkDifficulty_1m.png' : '-1m'
    }

    for key, value in dictionary.iteritems():
        print key, value
        rrdtool.graph(key,
            '--imgformat', 'PNG',
            '--slope-mode',
            '--width', '500',
            '--height', '150',
            '--start', '%s' % value,
            '--end', 'now',
            '--vertical-label', 'Difficulty',
            '--title', 'COIN - Network Difficulty',
            '--alt-y-grid', '--rigid',
            '--watermark', watermark,
            'DEF:NetworkDifficulty=%s:NetworkDifficulty:AVERAGE' % rrd,
            'AREA:NetworkDifficulty#A4A4A4',
            'LINE1:NetworkDifficulty#000000:NetworkDifficulty',
            'GPRINT:NetworkDifficulty:LAST:Last\: %5.2lf',
            'GPRINT:NetworkDifficulty:MIN:Min\: %5.2lf',
            'GPRINT:NetworkDifficulty:AVERAGE:Avg\: %5.2lf',
            'GPRINT:NetworkDifficulty:MAX:Max\: %5.2lf'
            )
