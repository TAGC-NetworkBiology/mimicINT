#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, errno, re, json, ssl
from urllib import request
from urllib.error import HTTPError
from time import sleep

# This script allows to download all the Pfam entries with
# the InterPro in which they have been integrated.

# ===========================================
# Constants
# ===========================================

# URL to perform the request
BASE_URL = "https://www.ebi.ac.uk:443/interpro/api/entry/pfam/?page_size={page_size}"

# Page size to perform the query
PAGE_SIZE = '200'



# ===========================================
# Methods
# ===========================================

## download_pfam_interpro_mapping
#  ------------------------------
#
# This script allows to download all the Pfam entries with the accession 
# of the InterPro in which they have been integrated.
# Only Pfam entries mapped to InterPro entries are downloaded.
#
# It uses the EBI REST API and has been adapted from the script provided 
# by the InterPro documentation at: 
# https://www.ebi.ac.uk/interpro/result/download/#/proteome/uniprot/|json
#
# The entries are written as tsv format to the standard output
# and contains the following columns:
# - Pfam_accession: String - The Pfam accession.
# - name: String - The name of the Pfam entry.
# - type: String - The type of entry (family, domain, repeats, motif, coiled-coil, disordered).
#                  See https://www.ebi.ac.uk/training/online/courses/pfam-creating-protein-families/pfam-entry-types/
# - InterPro_accession: String - The InterPro accession corresponding to the Pfam entry.
# 
def download_pfam_interpro_mapping():
    
    # Disable SSL verification to avoid config issues
    context = ssl._create_unverified_context()
    
    # The next property is the link to the next page
    # (results are paginated to allow large queries)
    next = BASE_URL.format( page_size = PAGE_SIZE )
    last_page = False

    
    # Print header
    header = [ 'Pfam_accession',
               'name',
               'type',
               'InterPro_accession' ]
    sys.stdout.write( '\t'.join( header ) + '\n' )
    
    # Instantiate a counter that will register the number
    # of times the request has been submitted to the server
    attempts = 0
    
    while next:
        
        # Perform the request
        try:
            req = request.Request( next,
                                   headers = { 'Accept' : 'application/json' } )
            res = request.urlopen( req,
                                   context = context )
            
            # If the API times out due a long running query
            if ( res.status == 408 ):
                # wait just over a minute
                sleep(61)
                # then continue this loop with the same URL
                continue
            
            elif ( res.status == 204 ):
                # No data so leave loop
                break
            
            # If the request succeed, then parse the json results 
            # as a Python dictionary
            payload = json.loads( res.read().decode() )
            
            # Get the URL of the next request
            next = payload[ 'next' ]
            
            if not next:
                last_page = True
            
            # Reset the counter of attemps
            attempts = 0
            
                
        except HTTPError as e:
            
            if ( e.code == 408 ):
                sleep(61)
                continue
            
            else:
                # If there is a different HTTP error, 
                # re-try 3 times before failing
                if ( attempts < 3 ):
                    attempts += 1
                    sleep(61)
                    continue
                
                else:
                    sys.stderr.write( 'Request failed, last URL used was:' + 
                                      next )
                    raise e
        
        # For each entry, parse the results to print them as tab-separated values
        for ( i, item ) in enumerate( payload[ 'results' ] ):
            
            # Parse the information about the Pfam entry
            pfam_accession = item[ 'metadata' ][ 'accession' ]
            entry_name = item[ 'metadata' ][ 'name' ]
            entry_type = item[ 'metadata' ][ 'type' ]
            interpro_accession = item[ 'metadata' ][ 'integrated' ]
            
            # Check only entries from Pfam are provided
            source_database = item[ 'metadata' ][ 'source_database' ]
            if ( source_database != 'pfam' ):
                raise Exception( 'The entry with accession ' + pfam_accession + 
                                 '(' + entry_name + ') comes from another source than Pfam (' +
                                 source_database + ').' )
                
            # Add a new line to the file
            if interpro_accession:
                line = [ pfam_accession,
                         entry_name,
                         entry_type,
                         interpro_accession ]
                sys.stdout.write( '\t'.join( line ) + '\n' )
            
            if ( last_page 
                 and ( i + 1 == len( payload[ 'results' ] ) ) ):
                sys.stdout.write( '' )
            
        # Wait one second to do not overload the server
        if next:
            sleep(1)
                



# ===========================================
# Parse options and run script
# ===========================================

if ( __name__ == '__main__' ):
    
    # Download the Pfam - InterPro cross-references
    download_pfam_interpro_mapping()
    