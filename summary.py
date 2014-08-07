#!/usr/bin/env python

import functions
import datetime
import rrdtool
import os.path
from pycgminer import CgminerAPI

'''
u'Difficulty Accepted': 4676371.0,
u'Pool Rejected%': 0.0519,
u'Network Blocks': 1103,
u'Difficulty Rejected': 2441.0,
u'MHS 15m': 32835.71,
u'Device Rejected%': 0.0524,
u'Pool Stale%': 0.4457,
u'Work Utility': 322.16,
u'Rejected': 202,
u'Elapsed': 867846,
u'Hardware Errors': 761,
u'Accepted': 60962,
u'Found Blocks': 0,
u'Local Work': 5532236,
u'Get Failures': 22,
u'Difficulty Stale': 20945.0,
u'Total MH': 20011541073.0,
u'Device Hardware%': 0.0163,
u'Discarded': 874473,
u'Stale': 289,
u'MHS av': 23058.87,
u'Getworks': 14051,
u'MHS 5s': 40971.84,
u'Best Share': 4832793,
u'MHS 1m': 33392.02,
u'MHS 5m': 33048.98,
u'Last getwork': 1407338237,
u'Remote Failures': 1,
u'Utility': 4.21
'''

SUMMARY_ATTRIBUTES = [
    'DifficultyAccepted',
    'PoolRejectedPct',
    'NetworkBlocks',
    'MHS15m',
    'DeviceRejectedPct',
    'PoolStalePct',
    'WorkUtility',
    'Rejected',
    'Elapsed',
    'HardwareErrors',
    'Accepted',
    'FoundBlocks',
    'LocalWork',
    'GetFailures',
    'DifficultyStale',
    'TotalMH',
    'DeviceHardwarePct',
    'Discarded',
    'Stale',
    'MHSav',
    'Getworks',
    'MHS5s',
    'BestShare',
    'MHS1m',
    'MHS5m',
    'Lastgetwork',
    'RemoteFailures',
    'Utility'
    ]

SUMMARY = functions.getSummary()

def createSummary(rrd=None, dataSources=None, rra=None):
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
        'DS:DifficultyAccepted:GAUGE:120:0:U',
        'DS:PoolRejectedPct:GAUGE:120:0:100',
        'DS:NetworkBlocks:GAUGE:120:0:U',
        'DS:MHS15m:GAUGE:120:0:U',
        'DS:DeviceRejectedPct:GAUGE:120:0:100',
        'DS:PoolStalePct:GAUGE:120:0:100',
        'DS:WorkUtility:GAUGE:120:0:U',
        'DS:Rejected:GAUGE:120:0:U',
        'DS:Elapsed:GAUGE:120:0:U',
        'DS:HardwareErrors:GAUGE:120:0:U',
        'DS:Accepted:GAUGE:120:0:U',
        'DS:FoundBlocks:GAUGE:120:0:U',
        'DS:LocalWork:GAUGE:120:0:U',
        'DS:GetFailures:GAUGE:120:0:U',
        'DS:DifficultyStale:GAUGE:120:0:U',
        'DS:TotalMH:GAUGE:120:0:U',
        'DS:DeviceHardwarePct:GAUGE:120:0:100',
        'DS:Discarded:GAUGE:120:0:U',
        'DS:Stale:GAUGE:120:0:U',
        'DS:MHSav:GAUGE:120:0:U',
        'DS:Getworks:GAUGE:120:0:U',
        'DS:MHS5s:GAUGE:120:0:U',
        'DS:BestShare:GAUGE:120:0:U',
        'DS:MHS1m:GAUGE:120:0:U',
        'DS:MHS5m:GAUGE:120:0:U',
        'DS:Lastgetwork:GAUGE:120:0:U',
        'DS:RemoteFailures:GAUGE:120:0:U',
        'DS:Utility:GAUGE:120:0:U'
        ]

    return dataSources

def populateSummary(rrd=None):
    if rrd == None:
        rrd = 'SUMMARY_UNK.rrd'
        createSummary(rrd)
    else:
        createSummary(rrd)
        template = functions.generateTemplate(attributes=SUMMARY_ATTRIBUTES)

        readings = generateSummaryReadings(SUMMARY)

        rrdtool.update(rrd,
            '--template', template, 'N:%s' % readings)

def generateSummaryReadings(readings=None):
    if readings is not None:
        separator = ':'
        sequence = (str(readings['Difficulty Accepted']),str(readings['Pool Rejected%']),str(readings['Network Blocks']),str(readings['MHS 15m']),str(readings['Device Rejected%']),str(readings['Pool Stale%']),str(readings['Work Utility']),str(readings['Rejected']),str(readings['Elapsed']),str(readings['Hardware Errors']),str(readings['Accepted']),str(readings['Found Blocks']),str(readings['Local Work']),str(readings['Get Failures']),str(readings['Difficulty Stale']),str(readings['Total MH']),str(readings['Device Hardware%']),str(readings['Discarded']),str(readings['Stale']),str(readings['MHS av']),str(readings['Getworks']),str(readings['MHS 5s']),str(readings['Best Share']),str(readings['MHS 1m']),str(readings['MHS 5m']),str(readings['Last getwork']),str(readings['Remote Failures']),str(readings['Utility']))
        readings = separator.join(sequence)
    else:
        print 'FUCK'

    return readings

def createSummaryUptimeGraphs(rrd=None):
    watermark = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f - CEST")

    dictionary = {
        'SUMMARY_1h.png' : '-1h',
        'SUMMARY_12h.png' : '-12h',
        'SUMMARY_1d.png' : '-1d',
        'SUMMARY_1w.png' : '-1w',
        'SUMMARY_1m.png' : '-1m'
    }

    for key, value in dictionary.iteritems():
        print key, value
        rrdtool.graph(key,
            '--imgformat', 'PNG',
            '--slope-mode',
            '--width', '500',
#            '--height', '120',
            '--height', '150',
            '--start', '%s' % value,
            '--end', 'now',
            '--vertical-label', 'Days',
            '--title', 'SUMMARY - Uptime',
            '--alt-y-grid', '--rigid',
            '--watermark', watermark,
            'DEF:Elapsed=%s:Elapsed:AVERAGE' % rrd,
            'CDEF:Uptime=Elapsed,86400,/',
            'AREA:Uptime#00FF00',
            'LINE1:Uptime#0000FF:Uptime',
            'GPRINT:Uptime:LAST:Last\: %5.2lf',
            'GPRINT:Uptime:MIN:Min\: %5.2lf',
            'GPRINT:Uptime:AVERAGE:Avg\: %5.2lf',
            'GPRINT:Uptime:MAX:Max\: %5.2lf'
            )
