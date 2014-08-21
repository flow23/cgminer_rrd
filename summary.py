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

def createUptimeGraphs(rrd=None):
    watermark = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f - CEST")

    dictionary = {
        'SUMMARY_Uptime_1h.png' : '-1h',
        'SUMMARY_Uptime_12h.png' : '-12h',
        'SUMMARY_Uptime_1d.png' : '-1d',
        'SUMMARY_Uptime_1w.png' : '-1w',
        'SUMMARY_Uptime_1m.png' : '-1m'
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
            '--vertical-label', 'Days',
            '--title', 'SUMMARY - Uptime',
            '--alt-y-grid', '--rigid',
            '--watermark', watermark,
            'DEF:Elapsed=%s:Elapsed:AVERAGE' % rrd,
            'CDEF:Uptime=Elapsed,86400,/',
            'AREA:Uptime#A4A4A4',
            'LINE1:Uptime#000000:Uptime',
            'GPRINT:Uptime:LAST:Last\: %5.2lf',
            'GPRINT:Uptime:MIN:Min\: %5.2lf',
            'GPRINT:Uptime:AVERAGE:Avg\: %5.2lf',
            'GPRINT:Uptime:MAX:Max\: %5.2lf'
            )

def createLastgetworkGraphs(rrd=None):
    watermark = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f - CEST")

    dictionary = {
        'SUMMARY_Lastgetwork_1h.png' : '-1h',
        'SUMMARY_Lastgetwork_12h.png' : '-12h',
        'SUMMARY_Lastgetwork_1d.png' : '-1d',
        'SUMMARY_Lastgetwork_1w.png' : '-1w',
        'SUMMARY_Lastgetwork_1m.png' : '-1m'
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
            '--title', 'SUMMARY - Last getwork',
            '--alt-y-grid', '--rigid',
            '--watermark', watermark,
            'DEF:Lastgetwork=%s:Lastgetwork:AVERAGE' % rrd,
            'AREA:Lastgetwork#A4A4A4',
            'LINE1:Lastgetwork#000000:Lastgetwork',
            'GPRINT:Lastgetwork:LAST:Last\: %10.0lf',
            'GPRINT:Lastgetwork:MIN:Min\: %10.0lf',
            'GPRINT:Lastgetwork:AVERAGE:Avg\: %10.0lf',
            'GPRINT:Lastgetwork:MAX:Max\: %10.0lf'
            )

def createMHSGraphs(rrd=None):
    watermark = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f - CEST")

    dictionary = {
        'SUMMARY_MHS_1h.png' : '-1h',
        'SUMMARY_MHS_12h.png' : '-12h',
        'SUMMARY_MHS_1d.png' : '-1d',
        'SUMMARY_MHS_1w.png' : '-1w',
        'SUMMARY_MHS_1m.png' : '-1m'
    }

    for key, value in dictionary.iteritems():
        print key, value
        rrdtool.graph(key,
            '--imgformat', 'PNG',
            '--width', '500',
            '--height', '150',
            '--start', '%s' % value,
            '--end', 'now',
            '--vertical-label', 'MH/s',
            '--title', 'SUMMARY - Hashrate',
            '--alt-y-grid', '--rigid',
            '--watermark', watermark,
            'DEF:MHS1m=%s:MHS1m:AVERAGE' % rrd,
            'DEF:MHS5m=%s:MHS5m:AVERAGE' % rrd,
            'DEF:MHS15m=%s:MHS15m:AVERAGE' % rrd,
            'DEF:MHSav=%s:MHSav:AVERAGE' % rrd,
            'AREA:MHS1m#FF0000:MHS1m',
            'GPRINT:MHS1m:LAST:\tLast\: %5.2lf %s',
            'GPRINT:MHS1m:MIN:Min\: %5.2lf %s',
            'GPRINT:MHS1m:AVERAGE:Avg\: %5.2lf %s',
            'GPRINT:MHS1m:MAX:Max\: %5.2lf %s\\n',
            'AREA:MHS5m#FF9900:MHS5m',
            'GPRINT:MHS5m:LAST:\tLast\: %5.2lf %s',
            'GPRINT:MHS5m:MIN:Min\: %5.2lf %s',
            'GPRINT:MHS5m:AVERAGE:Avg\: %5.2lf %s',
            'GPRINT:MHS5m:MAX:Max\: %5.2lf %s\\n',            
            'AREA:MHS15m#FFFF00:MHS15m',
            'GPRINT:MHS15m:LAST:Last\: %5.2lf %s',
            'GPRINT:MHS15m:MIN:Min\: %5.2lf %s',
            'GPRINT:MHS15m:AVERAGE:Avg\: %5.2lf %s',
            'GPRINT:MHS15m:MAX:Max\: %5.2lf %s',
            'LINE1:MHS5m#FF9900',
            'LINE1:MHS1m#FF0000',
            'LINE2:MHSav#000000::dashes'
            )

def createEfficiencyGraphs(rrd=None):
    watermark = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f - CEST")

    dictionary = {
        'SUMMARY_Efficiency_1h.png' : '-1h',
        'SUMMARY_Efficiency_12h.png' : '-12h',
        'SUMMARY_Efficiency_1d.png' : '-1d',
        'SUMMARY_Efficiency_1w.png' : '-1w',
        'SUMMARY_Efficiency_1m.png' : '-1m'
    }

    for key, value in dictionary.iteritems():
        print key, value
        rrdtool.graph(key,
            '--imgformat', 'PNG',
            '--width', '500',
            '--height', '150',
            '--start', '%s' % value,
            '--end', 'now',
            '--vertical-label', 'Percent',
            '--title', 'SUMMARY - Efficiency -- (WU/m)/(KH/s)',
            '--alt-y-grid', '--rigid',
            '--watermark', watermark,
            'DEF:MHSav=%s:MHSav:AVERAGE' % rrd,
            'DEF:WorkUtility=%s:WorkUtility:AVERAGE' % rrd,
            'CDEF:Efficiency=MHSav,WorkUtility,/',
            'AREA:Efficiency#E6E6FF:Efficiency',
            'LINE1:Efficiency#0000FF',
            'GPRINT:Efficiency:LAST:\tLast\: %5.2lf %s',
            'GPRINT:Efficiency:MIN:Min\: %5.2lf %s',
            'GPRINT:Efficiency:AVERAGE:Avg\: %5.2lf %s',
            'GPRINT:Efficiency:MAX:Max\: %5.2lf %s\\n',
            )

def createBestShareGraphs(rrd=None):
    watermark = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f - CEST")

    dictionary = {
        'SUMMARY_BestShare_1h.png' : '-1h',
        'SUMMARY_BestShare_12h.png' : '-12h',
        'SUMMARY_BestShare_1d.png' : '-1d',
        'SUMMARY_BestShare_1w.png' : '-1w',
        'SUMMARY_BestShare_1m.png' : '-1m'
    }

    for key, value in dictionary.iteritems():
        print key, value
        rrdtool.graph(key,
            '--imgformat', 'PNG',
            '--width', '500',
            '--height', '150',
            '--start', '%s' % value,
            '--end', 'now',
            '--vertical-label', '???',
            '--title', 'SUMMARY - Best Share',
            '--alt-y-grid', '--rigid',
            '--watermark', watermark,
            'DEF:BestShare=%s:BestShare:AVERAGE' % rrd,
            'AREA:BestShare#E6E6FF:BestShare',
            'LINE1:BestShare#0000FF',
            'GPRINT:BestShare:LAST:\tLast\: %5.2lf %s',
            'GPRINT:BestShare:MIN:Min\: %5.2lf %s',
            'GPRINT:BestShare:AVERAGE:Avg\: %5.2lf %s',
            'GPRINT:BestShare:MAX:Max\: %5.2lf %s\\n',
            )

