#!/usr/bin/env python

import functions
import datetime
import rrdtool
import os.path
import psutil

'''
psutil.virtual_memory()
svmem(total=8374149120L, available=2081050624L, percent=75.1, used=8074080256L, free=300068864L, active=3294920704, inactive=1361616896, buffers=529895424L, cached=1251086336)
'''

'''
psutil.swap_memory()
sswap(total=2097147904L, used=296128512L, free=1801019392L, percent=14.1, sin=304193536, sout=677842944)
'''

MEMORY_ATTRIBUTES = [
    'VmemTotal',
    'VmemAvailable',
    'VmemPercent',
    'VmemUsed',
    'VmemFree',
    'VmemActive',
    'VmemInactive',
    'VmemBuffers',
    'VmemCached',
    'SwapTotal',
    'SwapUsed',
    'SwapFree',
    'SwapPercent',
    'SwapSin',
    'SwapSout'
    ]

SUMMARY = functions.getSummary()

def createRRD(rrd=None, dataSources=None, rra=None):
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
        'DS:VmemTotal:GAUGE:120:0:U',
        'DS:VmemAvailable:GAUGE:120:0:U',
        'DS:VmemPercent:GAUGE:120:0:100',
        'DS:VmemUsed:GAUGE:120:0:U',
        'DS:VmemFree:GAUGE:120:0:U',
        'DS:VmemActive:GAUGE:120:0:U',
        'DS:VmemInactive:GAUGE:120:0:U',
        'DS:VmemBuffers:GAUGE:120:0:U',
        'DS:VmemCached:GAUGE:120:0:U',
        'DS:SwapTotal:GAUGE:120:0:U',
        'DS:SwapUsed:GAUGE:120:0:U',
        'DS:SwapFree:GAUGE:120:0:U',
        'DS:SwapPercent:GAUGE:120:0:100',
        'DS:SwapSin:GAUGE:120:0:U',
        'DS:SwapSout:GAUGE:120:0:U'
        ]

    return dataSources

def populateMemory(rrd=None):
    if rrd == None:
        rrd = 'MEMORY_UNK.rrd'
        createRRD(rrd)
    else:
        createRRD(rrd)
        template = functions.generateTemplate(attributes=MEMORY_ATTRIBUTES)

        readings = generateMemoryReadings(vMemReadings=psutil.virtual_memory(), swapReadings=psutil.swap_memory())

        rrdtool.update(rrd,
            '--template', template, 'N:%s' % readings)

def generateMemoryReadings(vMemReadings=None, swapReadings=None):
    if vMemReadings is not None and swapReadings is not None:
        separator = ':'
        sequence = (str(int(vMemReadings.total)), str(int(vMemReadings.available)), str(int(vMemReadings.percent)), str(int(vMemReadings.used)), str(int(vMemReadings.free)), str(int(vMemReadings.active)), str(int(vMemReadings.inactive)), str(int(vMemReadings.buffers)), str(int(vMemReadings.cached)), str(int(swapReadings.total)), str(int(swapReadings.used)), str(int(swapReadings.free)), str(int(swapReadings.percent)), str(int(swapReadings.sin)), str(int(swapReadings.sout)))
        readings = separator.join(sequence)
    else:
        print 'FUCK'

    return readings

def createMemoryGraphs(rrd=None):
    watermark = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f - CEST")

    dictionary = {
        'MEMORY_Memory_1h.png' : '-1h',
        'MEMORY_Memory_12h.png' : '-12h',
        'MEMORY_Memory_1d.png' : '-1d',
        'MEMORY_Memory_1w.png' : '-1w',
        'MEMORY_Memory_1m.png' : '-1m'
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
            '--vertical-label', 'Byte',
            '--title', 'MEMORY - Virtual memory',
            '--alt-y-grid', '--rigid',
            '--watermark', watermark,
            'DEF:mem_total=%s:VmemTotal:AVERAGE' % rrd,
            'DEF:mem_used=%s:VmemUsed:AVERAGE' % rrd,
            'DEF:mem_free=%s:VmemFree:AVERAGE' % rrd,
            'DEF:mem_buffers=%s:VmemBuffers:AVERAGE' % rrd,
            'LINE1:mem_total#000000:mem_total',
            'LINE2:mem_used#D7CC00:mem_used',
            'LINE2:mem_free#00CC00:mem_free',
            'LINE2:mem_buffers#D73600:mem_buffers'
            )
