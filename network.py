#!/usr/bin/env python

import functions
import datetime
import rrdtool
import os.path
import psutil

'''
psutil.net_io_counters(pernic=True)
{'lo': snetio(bytes_sent=508567, bytes_recv=508567, packets_sent=4380, packets_recv=4380, errin=0, errout=0, dropin=0, dropout=0), 'ifb1': snetio(bytes_sent=0, bytes_recv=0, packets_sent=0, packets_recv=0, errin=0, errout=0, dropin=0, dropout=0), 'ifb0': snetio(bytes_sent=0, bytes_recv=0, packets_sent=0, packets_recv=0, errin=0, errout=0, dropin=0, dropout=0),
'wlan0': snetio(bytes_sent=3714895, bytes_recv=1830107, packets_sent=10635, packets_recv=10709, errin=0, errout=0, dropin=1208, dropout=0), 'eth0': snetio(bytes_sent=0, bytes_recv=0, packets_sent=0, packets_recv=0, errin=0, errout=0, dropin=0, dropout=0)}
'''

NETWORK_ATTRIBUTES = [
    'BytesSent',
    'BytesReceived',
    'PacketsSent',
    'PacketsReceived',
    'ErrorIn',
    'ErrorOut',
    'PacketsDropIn',
    'PacketsDropOut'
    ]

def createRRD(rrd=None, dataSources=None, rra=None):
    if os.path.isfile(rrd) is False:
        dataSources = generateDataSources()

        rra = functions.generateRRA()

        rrdtool.create(rrd,
            '--step', '120',
            dataSources,
            rra)

def generateDataSources():
    dataSources = [
        'DS:BytesSent:GAUGE:120:0:U',
        'DS:BytesReceived:GAUGE:120:0:U',
        'DS:PacketsSent:GAUGE:120:0:U',
        'DS:PacketsReceived:GAUGE:120:0:U',
        'DS:ErrorIn:GAUGE:120:0:U',
        'DS:ErrorOut:GAUGE:120:0:U',
        'DS:PacketsDropIn:GAUGE:120:0:U',
        'DS:PacketsDropOut:GAUGE:120:0:U'
        ]

    return dataSources

def populateNetwork(rrd=None, device=None):
    if rrd == None:
        rrd = 'NETWORK_UNK.rrd'
        createRRD(rrd)
    else:
        createRRD(rrd)
        template = functions.generateTemplate(attributes=NETWORK_ATTRIBUTES)

        if device is None:
            device = 'lo'

        readings = generateNetworkReadings(readings=psutil.net_io_counters(pernic=True), device=device)

        rrdtool.update(rrd,
            '--template', template, 'N:%s' % readings)

def generateNetworkReadings(readings=None, device=None):
    if readings is not None:
        for key, value in readings.iteritems():
            if key == device:
                separator = ':'
                sequence = (str(value[0]),str(value[1]),str(value[2]),str(value[3]),str(value[4]),str(value[5]),str(value[6]),str(value[7]))
                readings = separator.join(sequence)
    else:
        print 'FUCK'

    return readings

def createBytesGraphs(rrd=None, device=None):
    watermark = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f - CEST")

    dictionary = {
        'NETWORK_%s_Bytes_1h.png' % device : '-1h',
        'NETWORK_%s_Bytes_12h.png' % device : '-12h',
        'NETWORK_%s_Bytes_1d.png' % device : '-1d',
        'NETWORK_%s_Bytes_1w.png' % device : '-1w',
        'NETWORK_%s_Bytes_1m.png' % device : '-1m'
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
            '--vertical-label', 'Bytes',
            '--title', 'NETWORK %s - Traffic' % device,
            '--alt-y-grid', '--rigid',
            '--watermark', watermark,
            'DEF:BytesReceived=%s:BytesReceived:AVERAGE' % rrd,
            'DEF:BytesSent=%s:BytesSent:AVERAGE' % rrd,
            'CDEF:BytesSent_=BytesSent,-1,*',
            'AREA:BytesReceived#339933:BytesReceived',
            'GPRINT:BytesReceived:LAST:Last\: %5.2lf %s',
            'GPRINT:BytesReceived:MIN:Min\: %5.2lf %s',
            'GPRINT:BytesReceived:AVERAGE:Avg\: %5.2lf %s',
            'GPRINT:BytesReceived:MAX:Max\: %5.2lf %s',
            'AREA:BytesSent_#aa3333:BytesSent',
            'GPRINT:BytesSent:LAST:Last\: %5.2lf %s',
            'GPRINT:BytesSent:MIN:Min\: %5.2lf %s',
            'GPRINT:BytesSent:AVERAGE:Avg\: %5.2lf %s',
            'GPRINT:BytesSent:MAX:Max\: %5.2lf %s',
            'HRULE:0#000000'
            )
