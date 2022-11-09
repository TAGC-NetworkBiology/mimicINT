
library(getopt)
library(ggplot2)
library(plotly)
library(data.table)
library(gprofiler2)


### R script that runs a gprofiler enrichment analysis


# Clean workspace
rm( list = ls() )

# ===============================
# Constants
# ===============================

# Gprofiler constants
## TODO: to be change to archive url as soon as the new gprofiler version will be released
DEFAULT_GPROFILER_URL = "http://biit.cs.ut.ee/gprofiler"
DEFAULT_GPROFILER_SOURCES = c("GO","KEGG","REAC","CORUM")
DEFAULT_GPROFILER_CORRECTION_METHOD = "gSCS"
DEFAULT_GPROFILER_SIGNIF_THRESHOLD = 0.01



# ===============================
# Parse command-line arguments
# ===============================

# List of available options
option_list = list(
		c( 'run_id', 'r', '', 'character' ),
		c( 'species', 'g', '', 'character'),
		c( 'interactor_list_path', 'l', '', 'character' ),
		c( 'background_list_path', 'b', '', 'character' ),
		c( 'output_html_file_path', 'j', '', 'character' ),
		c( 'output_result_file_path', 't', '', 'character' ),
		c( 'gprofiler_url', 'u', '', 'character'),
		c( 'gprofiler_sources', 's', '', 'character'),
		c( 'gprofiler_correction_method', 'm', '', 'character'),
		c( 'gprofiler_signif_threshold', 'c', '', 'numeric'),
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

# Get the run ID
if ( ! is.null( opt$run_id ) ){
	run_id = opt$run_id
}else{
	stop( paste( format(Sys.time(), "%Y-%m-%d %H:%M:%S"),
					'CRITICAL',
					'A run ID needs to be provided.',
					sep = ' :: ' ) )
}

# Get the species name
if ( ! is.null( opt$species ) ){
	species = opt$species
}else{
	stop( paste( format(Sys.time(), "%Y-%m-%d %H:%M:%S"),
					'CRITICAL',
					'A species name needs to be provided (see gProfiler documentation for the list of species allowed).',
					sep = ' :: ' ) )
}

# Get the interactor list file path
if ( ! is.null( opt$interactor_list_path ) ){
	interactor_list_path = opt$interactor_list_path
	if ( ! file.exists( interactor_list_path ) ){
		stop( paste( format(Sys.time(), "%Y-%m-%d %H:%M:%S"),
					 'CRITICAL', paste0( 'No input file may be found at the path: "', 
										 interactor_list_path, '".' ),
					 sep = ' :: ' ) )
	}
}else{
	stop( paste( format(Sys.time(), "%Y-%m-%d %H:%M:%S"),
			     'CRITICAL',
				 'The path to the interactor list needs to be provided.',
				 sep = ' :: ' ) )
}

# Get the background list file path
if ( ! is.null( opt$background_list_path ) ){
	background_list_path = opt$background_list_path
	if ( ! file.exists( background_list_path ) ){
		stop( paste( format(Sys.time(), "%Y-%m-%d %H:%M:%S"),
					 'CRITICAL', paste0( 'No input file may be found at the path: "', 
								         background_list_path, '".' ),
					 sep = ' :: ' ) )
	}
}else{
	stop( paste( format(Sys.time(), "%Y-%m-%d %H:%M:%S"),
				 'CRITICAL',
				 'The path to the background list needs to be provided.',
				 sep = ' :: ' ) )
}

# Get the output HTML file path
if ( ! is.null( opt$output_html_file_path ) ){
	output_html_file_path = opt$output_html_file_path
}else{
	stop( paste( format(Sys.time(), "%Y-%m-%d %H:%M:%S"),
				 'CRITICAL',
				 'The path to the output HTML file needs to be provided.',
				 sep = ' :: ' ) )
}

# Get the output result file path
if ( ! is.null( opt$output_result_file_path ) ){
	output_result_file_path = opt$output_result_file_path
}else{
	stop( paste( format(Sys.time(), "%Y-%m-%d %H:%M:%S"),
					'CRITICAL',
					'The path to the output result file needs to be provided.',
					sep = ' :: ' ) )
}

# Get the gProfiler URL
if ( ! is.null( opt$gprofiler_url ) ){
	gprofiler_url = opt$gprofiler_url
}else{
	gprofiler_url = DEFAULT_GPROFILER_URL
}

# Get the list of ontologies on which perform the enrichment
if ( ! is.null( opt$gprofiler_sources ) ){
	gprofiler_sources = opt$gprofiler_sources
	# Parse the list if necessary
	gprofiler_sources = unlist( strsplit( gprofiler_sources, split = ","))
}else{
	gprofiler_sources = DEFAULT_GPROFILER_SOURCES
}

# Get the multiple correction method
if ( ! is.null( opt$gprofiler_correction_method ) ){
	gprofiler_correction_method = opt$gprofiler_correction_method
}else{
	gprofiler_correction_method = DEFAULT_GPROFILER_CORRECTION_METHOD
}

# Get the threshold for FDR to be considered as significant
if ( ! is.null( opt$gprofiler_signif_threshold ) ){
	gprofiler_signif_threshold = opt$gprofiler_signif_threshold
}else{
	gprofiler_signif_threshold = DEFAULT_GPROFILER_SIGNIF_THRESHOLD
}

# As file paths are provided as relative to the run folder,
# convert these path into absolute paths
interactor_list_path = file.path( getwd(), interactor_list_path )
background_list_path = file.path( getwd(), background_list_path )
output_html_file_path = file.path( getwd(), output_html_file_path )
output_result_file_path = file.path( getwd(), output_result_file_path )



# ===============================
# Run script
# ===============================

## Set gprofiler URL
set_base_url(gprofiler_url)

## change file names accordingly
interactor_file = read.table(interactor_list_path,stringsAsFactors=F,header= F)
background_file = read.table(background_list_path,stringsAsFactors=F,header=F)

## named list of interactor identifiers
interactor_list = eval( parse( text= paste0( "list(", run_id, "= interactor_file[,1])")))

## in principle this is the proteome
statistical_background = background_file[,1]

## gProfiler analysis, parameters can be tuned if needed
gprofiler_results = gost(interactor_list, 
		organism = species, 
		ordered_query = FALSE,
		multi_query = FALSE, 
		significant = TRUE, 
		exclude_iea = FALSE,
		measure_underrepresentation = FALSE, 
		evcodes = TRUE,
		user_threshold = gprofiler_signif_threshold, 
		correction_method = gprofiler_correction_method,
		domain_scope = c("custom"),
		custom_bg = statistical_background,
		sources = gprofiler_sources,
		as_short_link = FALSE)

## Results are stored in a dataframe that can be exported to a text file
result_table = data.table(gprofiler_results$result)

# Export results
if ( nrow( result_table ) != 0 ){
	## Result data table is written to file
	write.table(result_table[,.(term_id,source,term_name,p_value,term_size,query_size,intersection_size,precision,recall,intersection)],file=output_result_file_path,quote = F, row.names = F, sep = "\t")
	
	## The interactive Manhattan plot is generated using plotly
	result_plot = gostplot(gprofiler_results, capped = TRUE, interactive = TRUE)
	
	## Interactive plot is saved as an HTML page. Path and file name should change accordingly
	htmlwidgets::saveWidget(result_plot, output_html_file_path, selfcontained = TRUE)
	
} else {
	## Write the empty table
	write.table(data.frame( term_id = character(0),source = character(0),term_name = character(0),p_value = character(0),term_size = character(0),query_size = character(0),intersection_size = character(0),precision = character(0),recall = character(0),intersection = character(0)),file=output_result_file_path,quote = F, row.names = F, sep = "\t")
	## Create empty HTML file
	html_file = file(output_html_file_path)
	writeLines(c("<!DOCTYPE HTML>", "<html>", "<body>", "<p>No results to display</p>", "</body>", "</html>"), html_file)
	close(html_file)
}




# ===============================
# CLEAN WORKSPACE
# ===============================

rm( list = ls() )
