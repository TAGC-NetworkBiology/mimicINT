
# MimicInt SLiM likelihood computation user's manual

## Main steps

The MimicInt SLiM likelihood computation pipeline performs the following steps:

1. The ELM files are parsed in order to keep the ELMs which have been actually found in H. sapiens.

2. SLiMProb is used to identify the SLiMs contained in the viral ("real") sequences. For convenience of use, the masked fasta file of each strain is copied in a folder that is common to all masked fasta files.

3. The masked fasta files generated during the step 2. are used to generate sequences by randomization using an "intra-strain" and an "inter-strains" background.
   
4. SLiMProb is used to identify the SLiMs contained in the shuffled sequences generated in step 3.

5. The likelihood of each SLiM in each sequence of each strain is computed based on the frequence of apparition of the SLiM in the sequence using each background.



## Configuration files

The `config.yaml` file allows to define options such as paths and filenames, whilst
the `config_cluster.json` file may be edited to run MimicInt on clusters.


### `config.yaml` options

All options have to be provided using the syntax `option_name: value`. 
All paths provided in this file have to be **relative** to the run directory.

The following options **have** to be provided (mandatory):    

- **ELM files**
    - `elm_classes_file`: Path to the ELM classes file. 
    - `elm_instances_file`: Path to the ELM instances file.
    

- **Viral sequences**
    - `viral_sequence_folder`: Path to the *folder* containing the viral fasta files.
    


The following options may be provided (optional):

- **Parameter file log**
    - `log_parameters_file`: Path to the file logging the parameters provided by the user or automatically set by the pipeline (`log/parameters_comp_slim_proba.tsv` by default).
    

- **Output folders**
    - `output_folder`: Path to the common output folder for all rules (`output` by default).
    

- **General parameters** 
    - `randomization_count`: Number of randomized sequence to generate for each strain (with each background; `10000` by default).
    - `background_flag_code`: The background code to use. When equal to `3` (default), the generation of randomized sequences will be performed using both the intra and inter-strains background. Setting this parameter to `1` allows to perform the randomization using only the intra-strain background(s) whilst setting it to `2` allows to perform the randomization using only the inter-strains background.
    - `get_distributions`: Should the number of occurrence of each motifs in each shuffled sequence be recorded in the probability files? (`True` or `False`, `False` by default).
    

- Options related to the detection of **short linear motifs (SLiMs)** 
    - **ELM parsing options**
        - `pval_threshold_elm_parser`: Cut-off to use to filter the ELM classes based on their probability of occurrence (according to ELM files, `0.01` by default).
    - Options for **SLiMProb** (`detect_slim_query` rule, please see SLiMProb documentation for more information)
      - `maxsize`: Maximum dataset size to process in amino acids (`1000000000` by default).
      - `maxseq`: Maximum number of sequences to process (`10000` by default).
      - `minregion`: Minimum number of consecutive residues that must have the same disorder state (`10` by default).
      - `iumethod`: IUPred method to use (`short`/`long`, `short` by default). Several values allowed.
      - `iucut`: Cut-off for IUPred results (`0.2` by default).



## Use MimicInt SLiM likelihood

To use MimicInt SLiM likelihood:

1. Create a run directory, copy all files provided with this pipeline **and with MimicInt** (as it uses the same Singularity images pipeline) and move to the run directory (*i.e.* the directory containing `compute_slim_probability` folder).

2. Add the appropriate input files to the run directory. 
   Default ELM input files could be download automatically to the last version using: `bash common/script/prepare_input/download_input_files.sh`. 
   Viral sequences have to be added manually **in the same folder**.
   
3. Edit the config files. If you did not use the proposed structure for the input files, want to change the output folder, some of the options and/or need to update the cluster config, then you need to edit the config files. Make sure to update at least the e-mail in the cluster config file.

4. Start MimicInt SLiM likelihood workflow, by using `bash compute_slim_probability/workflow/run_comp_slim_proba.sh`. NB: You need to **make sure** you are in the Run directory prior to run one of these commands.
   This script may require to be updated according to the workstation or HPC you are using.
   NB: Config file options could be overridden when starting the workflow by using the argument `--config option_name=value` at the end of the command. As many options as needed could be added using this syntax. Any additional arguments will be interpreted as a Snakemake argument.
   *E.g.* You can hence perform a dry run using `bash compute_slim_probability/workflow/run_comp_slim_proba_meso.sh --dryrun`.  



## Useful information and troubleshooting

### Troubleshooting 

The detection of the SLiMs in the randomized sequences (with SLiMProb) is triggered by the absence of the last file

- If for some reason the pipeline is stopped or raise an exception during the execution of the `generate_randomized_sequences` rule, then you need to enforce the re-execution of this rule using the `-R generate_randomized_sequences` Snakemake argument (*e.g.* `bash compute_slim_probability/workflow/run_comp_slim_proba_meso.sh -R generate_randomized_sequences`). Not using this argument to re-start the pipeline will necessarily result in an exception like the following one:

```
MissingInputException in line 430 of compute_slim_probability/workflow/comp_slim_proba_snakefile:
Missing input files for rule detect_slim_randomized_sqces:
output/slim_likelihoods/randomized_sequences/background_{background_flag}/{strain}/{strain}_random_{number}.fasta
```

- If an exception is raised during the detection of the SLiMs in the randomized sequences (with SLiMProb, `detect_slim_randomized_sqces`), then the error will be logged (see `log/detect_slim_randomized_sqces_background_{background_flag}_{strain}.log`) and the output files generated will be removed (except for the log file). Nevertheless, the job will not be stopped and the detection of SLiM will continue for all other randomized sequences fasta files. Such an error will result later in the interruption of the two `compute_slim_likelihood` rules (logging the message `(one of the commands exited with non-zero exit code; note that snakemake uses bash strict mode!)`). In such cases, you need to force the re-execution of the `detect_slim_randomized_sqces` rule by using the argument `-R detect_slim_randomized_sqces` in the command line used to start Snakemake (*e.g.* `bash compute_slim_probability/workflow/run_comp_slim_proba_meso.sh -R detect_slim_randomized_sqces`). The re-execution of this task will skip all the SLiMProb processes already successfully performed (and that created the expected output files) and will only force the execution of SLiMProb processes that failed. Note that if for some reason the whole pipeline failed during the execution of this rule, then the use of the `-R detect_slim_randomized_sqces` Snakemake argument is not necessary as Snakemake look for the last file to be computed by the rule to determine if it needs to be started.

- If you are willing to enforce the new computation of **all** the output of the `detect_slim_randomized_sqces`, including those for which SLiMProb did not returned a non-zero exit code, then you first need to remove all the outputs of this rule, for instance using the command `rm -R $OUTPUT/slim_detect_randomized_sequences`, with `$OUTPUT` the path to the output folder (as defined with `output_folder` in the config file, `output` by default).

- If an error happen in any other step, then the pipeline could be restarted using the usual command (*e.g.* `compute_slim_probability/workflow/run_comp_slim_proba_meso.sh`) and should resolve itself the jobs to start to generate the missing files. 


### Other information

Various useful information are also registered in the documentation of the main MimicInt pipeline may be of interest (such as about how to generate reports or summary with Snakemake).



## Optional steps

### Rename fasta headers

In order to work properly, SLiMProb expect the fasta file headers to contain unique ACs. The script `script/rm_fasta_header_duplicates.py` allows to scan a fasta file in order to rename all the AC to get unique IDs. To do this, from the run directory, you may use the following command line:

```
singularity exec -B $(pwd):$(pwd) \
  common/Docker/data_parse/tagc-mimicint-data-parse.img \
  python3 common/script/prepare_input/rm_fasta_header_duplicates.py \
    -i input/sequences/sequence.fasta \
    -o output/sequences/sequence.fasta
```
