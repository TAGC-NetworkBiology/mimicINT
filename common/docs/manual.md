
# User's manual for accessory scripts

## Prepare the runs

### Preparing the Snakemake environment and the tools folder

The following operations should automatically be performed when running the script necessary to run the workflow for the first time and hence you should theoretically **never** use this scripts. 
Nevertheless, if an error reporting that the `tools` folder is missing, then this folder may be automatically created by using the `bash common/script/prepare_run/prepare_tool_folder.sh` command. This command will allow to copy the some executables (IUpred) that are present in the Singularity images (`tagc-mimicint-slim-detect.img`) in a folder where the user has the writing right. To ensure it is working properly, just check the `tool/iupred` folder exists and contains files. 



## Prepare the inputs

### Rename fasta headers

It is better for mimicINT to provide fasta file containing headers with unique accessions.

The script `common/script/prepare_input/rm_fasta_header_duplicates.py` allows to scan a fasta file in order to rename all the AC to get unique IDs.
To do this, from the run directory, you may use a command line like the following:

```
singularity exec -B $(pwd):$(pwd) \
  common/Docker/data_parse/tagc-mimicint-data-parse.img \
  python3 common/script/prepare_input/rm_fasta_header_duplicates.py \
    -i input/sequences/sequence.fasta \
    -o output/sequences/sequence.fasta
```


### Download mimicINT inputs

The script `common/script/prepare_input/download_input_files.sh` allows to automatically download some of the input files necessary to run SLiMProb, and echo some URLs that may be used to manually download some other input files.

It downloads:

- From the Eukaryotic Linear Motif (ELM) resource,
    - The ELM classes (from http://elm.eu.org/elms/elms_index.tsv).
    - The ELM interaction domains (from http://elm.eu.org/infos/browse_elm_interactiondomains.tsv).
    - The ELM instances have to be downloaded manually using the web interface.
    
- From the database of three-dimensional interacting domains (3did), the 3did flat file that contains interacting domain pairs (ID) and instances of these interactions in PDB structures along with InterPreTS scores (from https://3did.irbbarcelona.org/download/current/3did_flat.gz).

- The target sequences have to be manually downloaded from UniProtKB.

All those files are necessary for mimicINT, whilst only the ELM classes and instances are required to run the computation of the SLiM occurrence probabilities.


### Download InterPro annotations

All InterPro annotations for a reference proteome may be downloaded from the EBI, using the script `common/script/prepare_input/download_interpro_annotations_for_proteome.py`.

This script display on standard output all the reviewed proteins of a proteome along with all the InterPro entries detected on them.

A command line like the following may be used to save these information in a tsv file:

```
singularity exec -B $(pwd):$(pwd) \
  common/Docker/data_parse/tagc-mimicint-data-parse.img \
  python3 common/script/prepare_input/download_interpro_annotations_for_proteome.py \
    -p UP000005640 \
    1> input/InterPro/UP000005640_InterPro_annotations.tsv
```

The `-p` option may be used to provide a different UniProt proteome identifier (the identifiers may be found at https://www.uniprot.org/proteomes/). When not provided, the identifier UP000005640 is used by default (*Homo sapiens* proteome).


### InterPro - Pfam cross-references

All cross-references of Pfam to InterPro entries may be downloaded from the EBI, using the script `common/script/prepare_input/download_pfam_interpro_mapping.py`.

This script display on standard output all the Pfam entries that have been integrated into InterPro entries.

A command line like the following may be used to save these information in a tsv file:

```
singularity exec -B $(pwd):$(pwd) \
  common/Docker/data_parse/tagc-mimicint-data-parse.img \
  python3 common/script/prepare_input/download_pfam_interpro_mapping.py \
    1> input/InterPro/Pfam_InterPro_mapping.tsv
```



## Plot the rule graphs and DAG of jobs

For all Snakemake workflow provided in the current repository, a rule graph and a directed acyclic graph (DAG) may be plotted.


The rule graph of the pipeline could be plotted running the following command:

```
bash common/script/miscellaneous/plot_rulegraph.sh $SNAKEFILE $PICTURE
```


The DAG of the jobs run by the pipeline could be plotted running the following command: 

```
bash common/script/miscellaneous/plot_dag.sh $SNAKEFILE $PICTURE
```

with `$SNAKEFILE` the relative path to the snakefile and `$PICTURE` the relative path to the image that you want to create (NB: the image **must** end with the `.png` extension).

NB: Some of the rules may not appear on the rulegraph as the workflow contains checkpoints.
