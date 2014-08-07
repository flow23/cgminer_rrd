#!/usr/bin/env python

import pool, summary

pool.populatePool(url='http://rr.btcmp.com:3333',rrd='POOL_btcmp.rrd')
summary.populateSummary(rrd='SUMMARY.rrd')
