
library( "knitr" )
library( "getopt" )

# This script allows to generate the HTML files
# plotting the distribution of motif occurrences

# Clean workspace
rm( list = ls() )

# ===============================
# GET INPUT AND OUTPUT FILE PATHS
# ===============================

# List of available options
option_list = list(
  c( 'input', 'i', '', 'character' ),
  c( 'output', 'o', '', 'character' ),
  c( 'help', 'h', 0, 'logical' )
)

option_matrix = matrix( unlist( option_list ),
                        byrow = TRUE,
                        nrow = length( option_list) )

# Get the provided arguments
opt = getopt( option_matrix )

# Print help if necessary
if ( !is.null( opt$help ) ) {
  stop( getopt( option_matrix, usage=TRUE ) )
}

# Get the input file path
if ( ! is.null( opt$input ) ){
  input_file_path = opt$input
  if ( ! file.exists( input_file_path ) ){
    stop( paste( format(Sys.time(), "%Y-%m-%d %H:%M:%S"),
                 'CRITICAL',
                 paste0( 'No input file may be found at the path: "',
                         input_file_path, '".' ),
                 sep = ' :: ' ) )
  }
}else{
  stop( paste( format(Sys.time(), "%Y-%m-%d %H:%M:%S"),
               'CRITICAL',
               'The path to an input file needs to be provided.',
               sep = ' :: ' ) )
}

# Get the output file path
if ( ! is.null( opt$output ) ){
  output_file_path = opt$output
}else{
  stop( paste( format(Sys.time(), "%Y-%m-%d %H:%M:%S"),
               'CRITICAL',
               'The path to an output file needs to be provided.',
               sep = ' :: ' ) )
}

# As file paths are provided as relative to the run folder,
# convert these path into absolute paths
input_file_path = file.path( getwd(), input_file_path )
output_file_path = file.path( getwd(), output_file_path )



# ===============================
# COMPILE THE RMDs
# ===============================

# Compile the descriptive stat file
rmarkdown::render( input = 'compute_slim_probability/src/fr/tagc/execution/plot_distributions.Rmd',
                   output_file = output_file_path,
                   quiet = FALSE )



# ===============================
# CLEAN WORKSPACE
# ===============================

rm( list = ls() )
