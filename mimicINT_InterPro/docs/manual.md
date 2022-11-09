
# mimicINT_InterPro user's manual

This version of the worflow replaces the original version of mimicINT and uses InterPro accessions instead of Pfam accessions to infer the interactions.



## Main steps

The mimicINT_InterPro pipeline performs the following steps:

1. The 3did flat file is parsed in order to get the Pfam accession names and domain labels interacting together.

2. The Pfam accessions in the file created from the parsing of the 3did flat file are converted into InterPro identifiers using the cross-references provided.

3. The ELM files are parsed in order to keep the ELMs which have been actually found in H. sapiens.

3b. *Optional step*: ELM motifs are selected according to p-values computed using the `compute_slim_probability_v2` worflow provided with mimicINT.

4. All Pfam accessions used in the ELM interactions file are converted into InterPro accessions using the cross-references provided as input.

5. InterProScan is used to identify the domains contained in the "query" sequences and the output is parsed in order to filter out useful information. The domains harbored by the "target" sequences are provided as an input that must be downloaded from UniProt.

6. SLiMProb is used to identify the SLiMs contained in the "query" sequences, and eventually performs a conservation analysis using the database of orthologs (*beta version*). The output is then parsed in order to filter out useful information. If the query contains too many sequences, the input fasta file is first splitted in many smaller files to be processed in parallel and the results are aggregated.

7. SLiM (query) - domain (target) and domain (query) - domain (target) interactions are finally inferred using information related to SLiM and domains identified in the provided sequences and templates of interactions known from ELM.

7b. *Optional step*: SLiM - domain interactions are filtered based on domain scores. 

8. Additional steps are performed in order to generate several files useful for visualization and/or further analysis (such as Cytoscape-friendly formated files) and gene ontology enrichment analysis.

9. Optional: Query sequence names are simplified in order to use the sequence name instead of the full fasta header.



## Configuration files

The `config.yaml` file allows to define options such as path and filenames, whilst the `config_cluster.json` file may be edited to run mimicINT on clusters.


### `config.yaml` parameters

All parameters have to be provided using the syntax `option_name: value`. 
All paths provided in this file have to be **relative** to the run directory.


#### Mandatory parameters

The following options **have** to be provided (mandatory):

- **3did file**
    - `3did_flat_file`: Path to the 3did flat file.
    

- **ELM files**
    - `elm_classes_file`: Path to the ELM classes file. 
    - `elm_instances_file`: Path to the ELM instances file.
    - `elm_interaction_domains_file`: Path to the binding domains file.
    

- **Query sequences**
    - `query_fasta_file`: Either the path to a unique *query* sequences fasta file or the path of several files containing the `{query_names}` wildcard in their name. In such case, the values that could be taken by `query_names` have to be provided using the `query_names` options.
    
    
- **InterPro files**
    - `target_interpro_annotations_file`: Path to the file containing all the annotated domains in InterPro for the target sequences. The script `common/script/prepare_input/download_interpro_annotations_for_proteome.py` may be used to download this file from InterPro. See the documentation of the 'common' folder for more information.
    - `pfam_interpro_mapping_file`: Path to the file containing for all the Pfam accessions the InterPro accession in which they have been integrated. The script `common/script/prepare_input/download_pfam_interpro_mapping.py` may be used to download this file from InterPro. See the documentation of the 'common' folder for more information. 



#### Optional parameters

The following options may be provided (optional):
        
- **General parameters**
    - `run_id`: An ID can be set for the run (`MimicInt` by default).

    - `simplify_seq_names`: Should the pipeline try to simplify to use the unique sequence identifiers provided in the fasta headers instead of the full header (`False` by default). If set to `True`, the sequence names used in the output file will be simplified for both query and target sequences, such as the fasta header `>tr|A0A024A2C9|A0A024A2C9_HAEIF ` usually used as sequence name in the outputs will be simplified as `A0A024A2C9` for instance. Ideally, the fasta headers should be formated using the [UniProt recommendations](https://www.uniprot.org/help/fasta-headers). Nevertheless, some other formats of headers are accepted (see below). To ensure the correct execution of the pipeline using this option, you need to ensure that (i) there is **not** any space prior the identifier of the sequence, (ii) the elements of the first part of the header are pipe (`|`)-separated, (iii) the identifier of the sequence is located in second position in case several values are provided. When this option is selected, a new folder `7_renamed_sequences` will be created in the output folder. This folder contains all the outputs of the pipelines for which the sequence names have been replaced by the unique identifiers. In order to minimize the risks of interruption of the pipeline related to badly-formated input fasta files, this replacement of sequence names by unique identifiers is performed as a last step. Hence all the files generated using the usual sequence names remains accessible is in the other folders.

Examples of accepted fasta headers:

```
>tr|A0A024A2C9|A0A024A2C9_HAEIF Lipoprotein binding FH OS=Haemophilus influenzae OX=727 GN=lph PE=1 SV=1
>tr|A0A024A2C9|A0A024A2C9_HAEIF
>tr|A0A024A2C9
>A0A024A2C9
>A0A024A2C9|A0A024A2C9_HAEIF Lipoprotein binding FH OS=Haemophilus influenzae OX=727 GN=lph PE=1 SV=1
```


- **Query sequences**
    - `max_seq_per_fasta`: MimicInt split large query datasets into multiple fasta files, run concurrently SLiMProb on these files (when several threads are available) and aggregate the output into unique files. This option allows to set the maximum number of sequences that can be stored in one single fasta file (`2500` by default).


- **Log files**
    - `log_parameters_file`: Path to the file logging the parameters provided by the user or automatically set by the pipeline (`log/parameters.tsv` by default).
    - `job_status_folder`: Path of the folder aiming to receive place holders for the job status (`run_status` by default). Each time a job starts and ends, a place holder file is created. These files are not necessary to the execution of the pipeline itself and usually not useful for the user neither, but they may be useful for its integration in other programs. Each file is named using the format `{step}_{rule}_{parameters}` with `{step}` equals to start or end, `{rule}` the name of the rule and `{parameters}` a string combining the value of all the parameters conditioning the output of the rule. Each file contains one single line with the date at which it has been created (at format `YYYY-MM-DD HH:MM:SS`). The name of these files cannot be set by the user.

    
- Options related to the **domain detection**
    - `score_threshold_interpro_query`: Filter out all domains detected in the query sequences that have a score (e-value) higher or equal to this value. Several values allowed.


- Options related to the detection of **short linear motifs (SLiMs)** 
    - **ELM parsing options**
        - `pval_threshold_elm_parser`: Cut-off to use to filter the ELM classes based on their probability of occurrence (according to ELM files, `0.01` by default). Several values allowed.
    - `slim_pvalues_v2_file`: Path to the file containing the SLiM p-values computed with the `compute_slim_probability_v2` workflow. This option must be used in combination with the `pval_threshold_elm_filter` option that set the threshold (default: 0.05).
    - Options for **SLiMProb** (`detect_slim_query` rule, please see SLiMProb documentation for more information)
      - `maxsize`: Maximum dataset size to process in amino acids (`1000000000` by default).
      - `maxseq`: Maximum number of sequences to process (`10000` by default).
      - `minregion`: Minimum number of consecutive residues that must have the same disorder state (`10` by default). Several values allowed.
      - `iumethod`: IUPred method to use (`short`/`long`, `short` by default). Several values allowed.
      - `iucut`: Cut-off for IUPred results (`0.2` by default). Several values allowed.


- Options for **conservation analysis** (with SLiMProb). **Beta version** (using these options may result in unexpected errors).
    - `conservation_analysis`: Should a conservation analysis be perform with SLiMProb when identifying the SLiMs in the query sequences? (`True`/`False`, `False` by default)
    - `orthodb_fasta_file`: Path to the ortholog database file.


- Options related to the **domain scores**
    - `domain_score_file`: The path to the file of domain scores.
    - `domain_score_filter`: The type of domain score filter to use (either `A` or `D`, default: `A`). `A` filter is based on the annotation: only interactions involving domains that are annotated are selected. `D` filter is based on the domain score: only interactions involving domains with a score greater than a threshold are selected. When `D` is selected, `domain_score_threshold` allows to set that threshold (0.4 by default). 
    - `domain_score_position`: When set to `True` (default: `False), an additional filter may be applied on the position. Several instances of the same domain could exist on the same protein. If this filter is selected, the position of the domain will be considered in order to select only the domain for which the domain score has been computed as respect the filter as described above. Because the position of a given domain may slightly differs (notably due to difference between the InterPro version used to generate the domain scores file and the one used in mimicINT), an overlap lower than 100 % may be accepted to select the interaction. The `domain_score_overlap_dscore_to_dmi` (0.8 by default) and `domain_score_overlap_dmi_to_dscore` (0.8 by default) options allow to set these overlaps.
    
    
- Options related to the **enrichment analysis performed with gProfiler**
    - `gprofiler_url`: The URL to the gProfiler version to use. By default, mimicINT uses the last version of gProfiler (http://biit.cs.ut.ee/gprofiler).
    - `gprofiler_sources`: A **comma**-separated list of ontologies to use for the enrichment analysis (default: `GO`, must be among: `GO`, `GO:BP`, `GO:MF`, `GO:CC`, `KEGG`, `REAC`, `TF`, `MIRNA`, `CORUM`, `HP`, `HPA`, `WP`). See the R gProfiler2 documentation for more information.
    - `gprofiler_correction_method`: A semi-column-separated list of correction method to use for the enrichment analysis (default: `fdr`, must be among: `gSCS`, `fdr`, `bonferroni`). See the R gProfiler2 documentation for more information.
    - `gprofiler_signif_threshold`: A semi-column-separated list of FDR thresholds.


- **Output folders**. **NB: We strongly advice not to set these parameters in the config file**.
    - `output_folder`: Path to the common output folder for all rules (`output` by default).
    - `output_folder_3did`: Path to the folder containing 3did parsed file (intermediate output, `output/0_parse_3did` by default).
    - `output_folder_elm`: Path to the folder containing ELM parsed files (intermediate outputs, `output/1_parse_elm` by default).
    - `output_folder_domain_query`: Path to the folder containing files that describe the domains identified in the query sequences (InterProScan results, intermediate outputs, `output/3_detect_domain_query` by default).
    - `splitted_query`: Path to the folder containing the fasta files generated by splitting the input query fasta files (when number of sequences is over the `max_seq_per_fasta` threshold. See the documentation of the `max_seq_per_fasta` option for more information, `output/4_splitted_query` by default).
    - `output_folder_slim_query`: Path to the folder containing files that describe the motifs identified in the query sequences (SLiMProb results, intermediate outputs, `output/4_slim_detect` by default).
    - `output_folder_interaction_inference`: Path to the folder containing files that describe the inferred interactions (final outputs, `output/5_interactions` by default).
    - `output_folder_summary`: Path to the folder containing files that summarize information about the query and target sequences (final outputs, `output/6_summary` by default).
    - `output_folder_renamed_sequences`: Path to the folder containing files for which the sequence names have been replaced by unique identifiers (intermediates and final outputs, `output/7_renamed_sequences` by default).
    - `output_folder_gprofiler`: Path to the folder containing files generated by the gprofiler enrichment analysis (`output/8_gprofiler` by default).


- **WARNING**
    - **Parameters with several values** have to be provided as a semi-coma (`;`) separated list (without any space between each value of the list).
    - **Output folders** If one single query sequences fasta file has been provided an one single value is provided for each parameter set, then the output folder paths could be provided as actual paths. Otherwise, 
        - If multiple query sequences fasta files are used, then the `output_folder_domain_query`, `output_folder_slim_query` and `output_folder_interaction_inference` paths **must** contain the `{query_names}` wildcard.
        - If multiples values are provided for a parameter, then all the paths of the rule using it and downstream rules **must** contain the appropriate `{option}` wilcard in their path. *E.g.* If the parameter `iucut` has been set to `0.2;0.4` in the config file, then the `output_folder_slim_query`, `output_folder_interaction_inference` **must** contain the `{iucut}` wildcard in their paths (*e.g.*  `output_folder_slim_query: output/4_slim_detect/iucut_{iucut}` and `output_folder_interaction_inference: output/5_interactions/iucut_{iucut}`). 
        - If you do not ensure this output folder nomenclature, then the execution of the program will fail due to possible confusion of the output.
        - If the output folder of a rule has been set in the config file but not the output of a "downstream" rule, then the default folder will be used by the program.



## Use mimicINT_InterPro

To use mimicINT_InterPro:

1. Create a run directory, copy all files provided with this pipeline and move to this directory. The content from the following folders is mandatory: `common` and `mimicINT_InterPro`.

2. Add the appropriate input files to the run directory.
   
3. Edit the config files.

4. Start the **mimicINT_InterPro** workflow, by using `bash mimicINT_InterPro/workflow/run_mimicINT_InterPro.sh`. 
    NB: You need to **make sure** you are in the Run directory prior to run this command.
    NB: Config file options could be overridden when starting the workflow by using the argument `--config option_name=value` at the end of the command. As many options as needed could be added using this syntax. Any additional arguments will be interpreted as a snakemake argument.
    *E.g.* You can hence perform a dry run using `bash mimicINT/workflow/run_mimicint.sh --dryrun`.  



## Useful information

Useful Snakemake options:
    - `--dryrun` (or `-n`): Perform a dry-run. This will simulate the run of the pipeline and build the DAG of jobs.
    - `--summary`: Prints a table associating each output file with the rule that generated it and its creation, the log file and some other information.
    - `--report report.html`: Print an HTML report including useful information, such as figure with the date at which rules have been run, a list of output files for each rule etc.



## Optional steps

### Rename fasta headers

In order to work properly, SLiMProb expect the fasta file headers to contain unique ACs. The script `common/script/prepare_input/rm_fasta_header_duplicates.py` allows to scan a fasta file in order to rename all the AC to get unique IDs.
To do this, from the run directory, you may use the following command line:

```
singularity exec -B $(pwd):$(pwd) \
  common/Docker/data_parse/tagc-mimicint-data-parse.img \
  python3 common/script/prepare_input/rm_fasta_header_duplicates.py \
    -i input/sequences/sequence.fasta \
    -o output/sequences/sequence.fasta
```


### Plot the rule graph and DAG of job

The rule graph of the pipeline could be plotted running the following command: 

```
bash common/script/miscellaneous/plot_rulegraph.sh $SNAKEFILE $IMAGE_NAME
```

The directed acyclic graph (DAG) of the jobs run by the pipeline could be plotted running the following command: 

```
bash common/script/miscellaneous/plot_dag.sh $SNAKEFILE $IMAGE_NAME
```

with `$SNAKEFILE` the relative path to the snakefile and `$IMAGE_NAME` the relative path to the image that you want to create (NB: the image **has** to finished with the `.png` extension).



### Preparing the Snakemake environment and the tools folder

The following operation should automatically be performed when running `bash mimicINT/workflow/run_mimicint.sh` for the first time and hence you should **not** use these scripts. Nevertheless, if an error reporting that Snakemake is not available in the environment or the `tools` folder is missing, then the following operation could eventually solve your problem:

- The tools folder may be automatically created by using the `bash common/script/prepare_run/prepare_tool_folder.sh` command. This command will allow to copy the some executables (IUpred) that are present in the Singularity images (`tagc-mimicint-slim-detect.img`) in a folder where the user has the writing right. To ensure it is working properly, just check there are files in the `tool/iupred` folder. 
