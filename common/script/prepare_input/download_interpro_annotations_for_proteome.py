#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from optparse import OptionParser
import sys, errno, re, json, ssl
from urllib import request
from urllib.error import HTTPError
from time import sleep

# This script allows to download from the EBI all the InterPro annotations 
# for all the reviewed proteins from a proteome.

# ===========================================
# Constants
# ===========================================

# URL to perform the request
BASE_URL = 'https://www.ebi.ac.uk:443/interpro/api/protein/reviewed/entry/interpro/proteome/uniprot/{proteome_id}/?page_size={page_size}'

# Page size to perform the query
PAGE_SIZE = '2000'


# List of options allowed
# -----------------------

# The proteome identifier to use
PROTEOME_IDENTIFIER_OPTION = 'PROTEOME_IDENTIFIER'

# Default value for the proteome identifier 
# (UP000005640: H. sapiens)
PROTEOME_IDENTIFIER_DEFAULT = 'UP000005640'

OPTION_LIST = [ [ '-p', '--proteomeID', 'store', 'string', PROTEOME_IDENTIFIER_OPTION, PROTEOME_IDENTIFIER_DEFAULT,
                  'The UniProt proteome identifier. Allowed identifiers may be found at https://www.uniprot.org/proteomes/.' ] ]



# ===========================================
# Methods
# ===========================================

## download_interpro_entries
#  -------------------------
#
# This script allows to download from the EBI all the InterPro annotations 
# for all the reviewed proteins from a proteome.
#
# It uses the EBI REST API and has been adapted from the script provided 
# by the InterPro documentation at: 
# https://www.ebi.ac.uk/interpro/result/download/#/proteome/uniprot/|json
#
# The entries are written as tsv format to the standard output
# and contains the following columns:
# - UniProtKB_accession: String - The protein accession in UniProtKB.
# - name: String - The name of the protein.
# - length: Integer - The length of the protein.
# - InterPro_accession: String - The InterPro accession.
# - entry_type: String - The type of InterPro entry (homologous superfamily, protein family, 
#                        domain or repeat).
#                        See https://www.ebi.ac.uk/training/online/courses/interpro-functional-and-structural-analysis/what-is-an-interpro-entry/interpro-entry-types/ 
#                        for more information about the entry types.
# - start: Integer - The start position of the entry on the protein. 
#                    If the entry is fragmented, this position corresponds to 
#                    the lowest value of all start positions.
# - end: Integer - The end position of the entry on the protein.
#                  If the entry is fragmented, this position corresponds to 
#                  the highest value of all start positions.
# - fragmented: Boolean - Is the entry fragmented?
#
# @param proteome_id: String - The UniProt proteome identifier (ID).
#                              The identifiers may be found at https://www.uniprot.org/proteomes/.
# 
def download_interpro_entries( proteome_id ):
    
    # Disable SSL verification to avoid config issues
    context = ssl._create_unverified_context()
    
    # The next property is the link to the next page
    # (results are paginated to allow large queries)
    next = BASE_URL.format( proteome_id = proteome_id,
                            page_size = PAGE_SIZE )
    last_page = False

    
    # Print header
    header = [ 'UniProtKB_accession',
               'name',
               'length',
               'InterPro_accession',
               'entry_type',
               'start',
               'end',
               'fragmented' ]
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
            
            # Get information about the protein
            protein_accession = item[ 'metadata' ][ 'accession' ]
            protein_name = item[ 'metadata' ][ 'name' ]
            protein_length = item[ 'metadata' ][ 'length' ]
            
            # Check only reviewed entries are provided
            source_database = item[ 'metadata' ][ 'source_database' ]
            if ( source_database != 'reviewed' ):
                raise Exception( 'The protein with UniProtKB accession ' + protein_accession + 
                                 '(' + protein_name + ') is non reviewed (' +
                                 source_database + ').' )
            
            # Get information about the InterPro entry
            for k in range( 0, len( item[ 'entry_subset' ] ) ):
                
                entry_accession = item[ 'entry_subset' ][ k ][ 'accession' ]
                entry_type = item[ 'entry_subset' ][ k ][ 'entry_type' ]
                
                # Check the entry comes from InterPro
                source_database = item[ 'entry_subset' ][ k ][ 'source_database' ]
                if ( source_database != 'interpro' ):
                    raise Exception( 'The entry with accession ' + entry_accession + '(' + entry_type + 
                                     ') does not come from InterPro (source database: ' + source_database + ').' )
                
            
                # NB: Both homologous superfamily, protein family, domain, repeat 
                #     and site entries are registered.
                #     See https://www.ebi.ac.uk/training/online/courses/interpro-functional-and-structural-analysis/what-is-an-interpro-entry/interpro-entry-types/ 
                #     for more information.
                entry_locations = item[ 'entry_subset' ][ k ][ 'entry_protein_locations' ]
                
                for entry_location in entry_locations:
                    
                    # Only extremal locations are kept
                    fragments = entry_location[ 'fragments' ]
                    
                    fragments_count = len( fragments )
                    if ( fragments_count > 1 ):
                        entry_fragmented = 'True'
                    else:
                        entry_fragmented = 'False'
                    
                    start = min( [ fragment[ 'start' ] for fragment in fragments ] )
                    end = max( [ fragment[ 'end' ] for fragment in fragments ] )
                
                    # Add a new line to the file
                    line = [ protein_accession,
                             protein_name,
                             str( protein_length) ,
                             entry_accession,
                             entry_type,
                             str( start ),
                             str( end ),
                             entry_fragmented ]
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
    
    ## Command-line arguments are parsed.
    # Store the various option values into a dictionary
    optionParser = OptionParser()    
    for current_opt in OPTION_LIST:
        optionParser.add_option( current_opt[0],
                                 current_opt[1],
                                 action = current_opt[2],
                                 type = current_opt[3],
                                 dest = current_opt[4],
                                 default = current_opt[5],
                                 help = current_opt[6] )
    (opts, args) = optionParser.parse_args()
    option_dict = vars(opts)
    
    # Get the proteome identifier to use
    proteome_id = option_dict.get( PROTEOME_IDENTIFIER_OPTION )
    
    # Download the InterPro entries
    download_interpro_entries( proteome_id = proteome_id )
    