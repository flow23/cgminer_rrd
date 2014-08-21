#!/usr/bin/env python2.7

import pool, summary, memory, network, device, coin

pool.populatePool(url='http://rr.btcmp.com:3333',rrd='POOL_btcmp.rrd')
summary.populateSummary(rrd='SUMMARY.rrd')
memory.populateMemory(rrd='MEMORY.rrd')
network.populateNetwork(rrd='NETWORK_eth0.rrd',device='eth0')
network.populateNetwork(rrd='NETWORK_wlan0.rrd',device='wlan0')
coin.populateCoin(rrd='COIN.rrd')
device.populateDevice(rrd='DEVICE_0.rrd',device='0')
device.populateDevice(rrd='DEVICE_1.rrd',device='1')
device.populateDevice(rrd='DEVICE_2.rrd',device='2')
