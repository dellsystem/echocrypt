#!/usr/bin/env python
# encoding: utf-8

"""
Copyright (c) 2010 The Echo Nest. All rights reserved.
Created by Tyler Williams on 2011-04-08

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
From: http://developer.echonest.com/raw_tutorials/faqs/faq_02.html
"""

# ========================
# = personal_catalog_scanner.py =
# ========================
#
# create a personal catalog by scanning a directory of mp3s with eyeD3
#

import sys
import os
import time
import pprint
from optparse import OptionParser
import hashlib

from pyechonest import config, catalog, song
import eyeD3
import settings
config.ECHO_NEST_API_KEY=settings.api_key

def collect_ids(catalog, ids):
    size = 100
    start = 0
    while True:
        items = catalog.read_items(results=size, start=start)
        if len(items) == 0:
            break;
        for item in items:
            if isinstance(item, song.Song):
                request = item.request
            else:
                request = item['request']
            ids.add(request['item_id'])
        start += size
    print 'read', len(ids), 'ids'

        
def process_queue(catalog, queue):
    max_size = 10000
    batch = []
    done = set()

    collect_ids(catalog, done)

    for which, file_path in enumerate(queue):
        print which, 'of', len(queue)
        # is it an mp3?
        if not file_path.lower().endswith(".mp3"):
            continue

        # try to pull our data
        fileinfo = {}
        try:
            tag = eyeD3.Tag()
            tag.link(file_path)
            md5_hash = hashlib.md5(open(file_path, "r").read()).hexdigest()

            fileinfo['artist_name'] = tag.getArtist()
            fileinfo['release'] = tag.getAlbum()
            fileinfo['song_name'] = tag.getTitle()
            fileinfo['url'] = file_path
            fileinfo['item_id'] = md5_hash
            #print tag.getArtist(), ' - ', tag.getTitle()
        except Exception,e:
            print "trouble:",e
            continue
        
        if not md5_hash in done:
            done.add(md5_hash)
            cat_item = {'action':'update', 'item':fileinfo}
            batch.append(cat_item)
            if len(batch) >= max_size:
                print which, 'of', len(queue), 'files'
                push_batch(batch, catalog)
                batch = []
    if len(batch) > 0:
        push_batch(batch, catalog)
        batch = []

def push_batch(batch, catalog):
    start = time.time()
    ticket = catalog.update(batch)
    delta = time.time() - start
    print 'Upload took', delta, 'seconds'
    wait_for_update(catalog, ticket)

def wait_for_update(catalog, ticket):
    start = time.time()
    status = 'incomplete'
    while status <> 'complete' and status <> 'error':
        tstatus = catalog.status(ticket)
        status = tstatus['ticket_status']
        #print 'status', status, 'percent', tstatus['percent_complete'] 

        time.sleep(3)
    delta = time.time() - start
    print 'Update took', delta, 'seconds'

def scan(directory, list):
    for folder, subs, files in os.walk(directory):
        for filename in files:
            list.append(os.path.join(folder, filename))

# Callable by other python scripts
def run(catalog_name, directory):
	queue = []
	c = catalog.Catalog(catalog_name, 'song')
	scan(directory, queue)
	process_queue(c, queue)
	pprint.pprint(c.profile)

def main():
    usage = 'usage: %prog [options]  "directory1" "directory2" ... "directoryN"'
    parser = OptionParser(usage=usage)

    parser.add_option("-c", "--catalog", metavar="CATNAME", help="catalog name")
    parser.add_option("-t", "--type", metavar="CATTYPE", help="catalog type", default='song')

    (options, args) = parser.parse_args()

    if not options.catalog:
        parser.error("please provide a catalog name with the -c parameter")

    if not options.type:
        parser.error("please specify a catalog type with the -t parameter")

    if len(args) < 1:
        parser.error("you must provide at least 1 directory containing mp3s!")
    
    c = catalog.Catalog(options.catalog, options.type)

    queue = []
    for directory in args:
        print "scanning directory: directory"
        scan(directory, queue)
        print "Found %d files" % (len(queue))
        process_queue(c, queue)


    pprint.pprint(c.profile)
    print "all done!"

if __name__ == "__main__":
    main()
