#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 2020/02/18 -- SC

from os.path import sys
from optparse import OptionParser


# The functions of this module help to parse and access the options 
# provided in a command line.

## parse_arguments
#  ---------------
#
# This is a static method that helps to parse the options
# provided with the command line.
# 
# @param option_list: List - The list of options.
#                            NB: The options of the list have to be written 
#                                as lists themselves according to this model:
#                                [ '-ShortTag', '--LongTag', action, type, dest, default, help ]
#
# @return option_dict: Dictionary - The dictionary that associates to each 
#                                   option its value.
#
def parse_arguments( option_list ):
        
    # Build an option parser to collect the option values
    optionParser = OptionParser()
    
    for current_prop_list in option_list:
        if ( current_prop_list[3] == 'choice' ):
            optionParser.add_option( current_prop_list[ 0 ],
                                     current_prop_list[ 1 ],
                                     action = current_prop_list[ 2 ],
                                     type = current_prop_list[ 3 ],
                                     dest = current_prop_list[ 4 ],
                                     choices = current_prop_list[ 5 ],
                                     default = current_prop_list[ 6 ],
                                     help = current_prop_list[ 7 ] )
        else:
            optionParser.add_option( current_prop_list[ 0 ],
                                     current_prop_list[ 1 ],
                                     action = current_prop_list[ 2 ],
                                     type = current_prop_list[ 3 ],
                                     dest = current_prop_list[ 4 ],
                                     default = current_prop_list[ 5 ],
                                     help = current_prop_list[ 6 ] )
    

    # Get the various option values into a dictionary
    ( opts, args ) = optionParser.parse_args()
    option_dict = vars( opts )
    
    return option_dict



## get_option
#  ----------
#
# This is a static method that allows to get the value of an option 
# using the option dictionary and the name of the option.
# If the option is not available, it returns None.
#
# @param option_dict: String - The option dictionary.
# @param option_name: String - The name of the option to get.
# @param not_none: Boolean - Is the option mandatory? If True, an exception
#                            is raised if it cannot be found in the option 
#                            dictionary. False by default.
#
# @return The value of option if available. None otherwise.
#
# @raise Exception - When the option cannot be found in the dictionary and the
#                    not_none argument has been set to True.
#
def get_option( option_dict, option_name, not_none=False ):
    
    return option_dict.get( option_name, None )
