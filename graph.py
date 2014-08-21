#!/usr/bin/env python2.7

import pool, summary, memory, network, device, coin

coin.createLastBlockTimeGraphs(rrd='COIN.rrd')
coin.createNetworkDifficultyGraphs(rrd='COIN.rrd')
summary.createEfficiencyGraphs(rrd='SUMMARY.rrd')
summary.createBestShareGraphs(rrd='SUMMARY.rrd')
summary.createUptimeGraphs(rrd='SUMMARY.rrd')
summary.createLastgetworkGraphs(rrd='SUMMARY.rrd')
summary.createMHSGraphs(rrd='SUMMARY.rrd')
memory.createMemoryGraphs(rrd='MEMORY.rrd')
network.createBytesGraphs(rrd='NETWORK_wlan0.rrd', device='wlan0')
device.createTemperatureGraphs(rrd='DEVICE_0.rrd', device='0')
device.createTemperatureGraphs(rrd='DEVICE_1.rrd', device='1')
device.createTemperatureGraphs(rrd='DEVICE_2.rrd', device='2')
