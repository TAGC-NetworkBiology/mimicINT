
# mimicINT: a workflow for microbe-host protein interaction inference


Choteau SA, Cristianini M, Maldonado K, Drets L, Boujeant M, Brun C, Spinelli L, Zanzoni A. mimicINT: a workflow for microbe-host protein interaction inference. bioRxiv 2022. [https://doi.org/10.1101/2022.11.04.515250](https://doi.org/10.1101/2022.11.04.515250)
 



## Goal of the repository

This GitHub repository provides an implementation of the mimicINT workflow. It contains the instructions and materials to run it.

Documentation, source code, scripts and containers are available in this repository. Instructions necessary to install mimicINT and run an analysis with it are provided below.



## Information about the mimicINT workflow

The mimicINT workflow is actually constituted of two workflows. Both of them can be run in an independent manner:

- The mimicINT main workflow (or `mimicINT_InterPro` workflow) allows to infer a protein-protein interactions network. It notably requires as input the domain annotations from the [InterPro database](https://www.ebi.ac.uk/interpro/) for the target as well as a fasta file of amino acid sequences for the query.

- The mimicINT randomization workflow (or `compute_slim_probability` workflow) allows to compute probabilities of functionality of the short linear motifs (SLiMs) on the query sequences, based on Monte-Carlo simulations. It notably requires as input a fasta file of amino acid sequences.



## System requirement and dependencies

### Hardware requirements

The hardware necessary to run mimicINT is highly dependent on the inputs and particularly on the number and length of sequences provided to mimicINT. Both workflows are compatible with the use of high performance computing (HPC) clusters. Because the mimicINT randomization workflow is based on Monte-Carlo simulations, it may require much more computational resources when submitting a large set of sequence. Hence, we advice to run it preferentially on HPC clusters.

Here are some example of resources required to run mimicINT:

TODO


### Operating systems

mimicINT has been successfully used on [Ubuntu](https://ubuntu.com/) (16.04 and higher) and [CentOS](https://www.centos.org/) (7.4) operating systems (OS). Despite being theoretically compatible with other operating systems, we do not ensure the compatibility with other OS and strongly advice to run mimicINT on Linux systems.


### Third-party softwares

Use of the third-party software, libraries or code referred to in the current documentation may be governed by separate terms and conditions or license provisions. Your use of the third-party software, libraries or code is subject to any such terms and you should check that you can comply with any applicable restrictions or terms and conditions before use.


### Software requirements

mimicINT requires [Python](https://www.python.org/) 3.6 and [Snakemake](https://snakemake.readthedocs.io/) 6.5 to be installed. Please, read the official documentation of [Python](https://docs.python.org/3.6/using/index.html) and [Snakemake](https://snakemake.readthedocs.io/en/v6.5.0/getting_started/installation.html) for more information about their installation. Note that mimicINT may be run in a Python [virtual environment](https://docs.python.org/3.6/tutorial/venv.html).

We strongly advice to use mimicINT with [Singularity](https://sylabs.io/guides/3.0/user-guide/quick_start.html) 2.5 or higher, in particular when using mimicINT on HPC clusters. The Singularity images may be build from the dockerfiles provided in the `common/Docker` folder. Nonetheless, you may also run mimicINT without using Singularity. In such cases, please make sure to ensure the installation of all dependencies prior to use mimicINT.


### Clone the GitHub repository

First, you need to clone the current repository. Please read the [GitHub documentation](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository) for extensive details about how to clone a repository. This will create a folder called `mimicINT` containing all the code and documentation.

The current documentation assumes you set up an environment variable called `WORKING_DIR` with its value set to the path of the `mimicINT` folder.



### Prepare the Singularity images

In order to prepare the Singularity images required by mimicINT, you need to:

1. Install [Docker](https://www.docker.com/) and [Singularity](https://singularity.lbl.gov/)
2. Build the Docker images
3. Generate the Singularity images files

This section provides additional information for each of these steps.


#### Install Docker and Singularity

You need to install [Docker](https://www.docker.com/) (18.09 or higher) and [Singularity](https://sylabs.io/guides/3.0/user-guide/index.html) (2.5 or higher) on your system. Please, read their official documentation for more information.

- To install Docker, follow the instructions provided at [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/) and [https://docs.docker.com/engine/install/linux-postinstall/](https://docs.docker.com/engine/install/linux-postinstall/).

- To install Singularity, follow the instructions provided at [https://sylabs.io/guides/2.5/admin-guide/](https://sylabs.io/guides/2.5/admin-guide/) (v 2.5) or at [https://sylabs.io/guides/3.0/user-guide/installation.html](https://sylabs.io/guides/3.0/user-guide/installation.html) (v 3.0)


#### Download third-party softwares

The build of one of the container requires third-party softwares that you first need to download. First check that you can comply with any applicable restrictions or terms and conditions before use and then download the following softwares:

- Blast (2.7.1): [https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.7.1/ncbi-blast-2.7.1+-x64-linux.tar.gz](https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.7.1/ncbi-blast-2.7.1+-x64-linux.tar.gz)

- IUPred (1.0): [https://iupred2a.elte.hu/](https://iupred2a.elte.hu/)

Once these files have been download, move them into the `$WORKING_DIR/common/Docker/slim_detect/` folder.


#### Build the Singularity images

The Docker images must first be build and then exported as Singularity image files (`.img` or `.sif`). Both steps could be performed at once running the script `create_all_singularity2.5.sh` or `create_all_singularity3.sh` from a computer where Docker has been installed and has been granted root privileges (see [https://docs.docker.com/engine/install/linux-postinstall/](https://docs.docker.com/engine/install/linux-postinstall/)).

Run the following command line depending on your Singularity version (you may check the version installed using `singularity --version`):

**Singularity 2 (2.5 or higher)**

```
cd $WORKING_DIR
bash common/Docker/create_all_singularity2.sh
```

This script is an interactive script. At the end of the creation of each Docker images, the user will be prompted to select the size of the Singularity image to create. You need to get the size of the Docker and enter a slightly higher size (in Mo), then press enter.


**Singularity 3 (3.0 or higher)**

```
cd $WORKING_DIR
bash common/Docker/create_all_singularity3.sh
```

This script is an interactive script. At the end of the creation of all Singularity images, you will be prompted your password to move the ownership of the images (`.sif` files) from the root to your user.

**Caution:** The build of the Docker images and Singularity image files may require up to one hour.


#### Container tree view

Once the Singularity images have been successfully generated, you should get the following tree view for the `common/Docker/` folder:

```
├── create_all_singularity.sh
├── docker_to_singularity.sh
├── data_parse
│   ├── dockerfile
│   ├── readme.txt
│   ├── tagc-mimicint-data-parse.img    [Singularity 2]
│   └── tagc-mimicint-data-parse.sif    [Singularity 3]
├── domain_detect
│   ├── dockerfile
│   ├── readme.txt
│   ├── tagc-mimicint-domain-detect.img    [Singularity 2]
│   └── tagc-mimicint-domain-detect.sif    [Singularity 3]
├── miscellaneous
│   └── graphviz
│       ├── dockerfile
│       ├── readme.txt
│       ├── tagc-mimicint-misc-graphviz.img    [Singularity 2]
│       └── tagc-mimicint-misc-graphviz.sif    [Singularity 3]
├── R
│   ├── dockerfile
│   ├── readme.txt
│   ├── tagc-mimicint-r.img    [Singularity 2]
│   └── tagc-mimicint-r.sif    [Singularity 3]
├── Rstudio
│   ├── dockerfile
│   ├── userconf.sh
│   ├── readme.txt
│   ├── tagc-mimicint-rstudio.img    [Singularity 2]
│   └── tagc-mimicint-rstudio.sif    [Singularity 3]
└── slim_detect
    ├── dockerfile
    ├── iupred.tar.gz
    ├── ncbi-blast-2.7.1+-x64-linux.tar.gz
    ├── readme.txt
    ├── tagc-mimicint-slim-detect.img    [Singularity 2]
    └── tagc-mimicint-slim-detect.sif    [Singularity 3]
```

*NB:* The extension of the image files generated depends on the Singularity version used (`.img` for Singularity 2 and `.sif` for Singularity 3). 

 

### Run mimicINT without Singularity

We strongly encourage the use of Singularity to run mimicINT, as this allows running the rules of the workflow in separate environments and helps ensuring reproducibility of the results.

Nonetheless, you may be willing to consider the following alternatives:

- Using Docker instead of Singularity. In such case you need to modify the Snakefiles (`compute_slim_probability/workflow/comp_slim_proba_snakefile` and `mimicINT_InterPro/workflow/mimicint_interpro_snakefile`) to replace the `singularity` statements in the rules by `container` statements. As an example, the line 612 of the file `mimicINT_InterPro/workflow/mimicint_interpro_snakefile` (`singularity: "common/Docker/data_parse/tagc-mimicint-data-parse.img"`) should be modified by `container: "docker://tagc-mimicint-data-parse"`.

- Not using Docker nor Singularity. In such case, you need to ensure the installation of all the dependencies on your system. See the dockerfiles and their documentation for more information to get the list of dependencies and check the official documentation of these softwares for more information regarding their installation. In such case, you need to run Snakemake without the `--use-singularity` option. It may also require to update the path to the executables in the Snakemake rules. Finally, be aware that this option is highly susceptible to result in many errors!

Please note that we do **not** ensure the successful execution of mimicINT when using of of these two method, neither when modifying the source code!


### Dependencies

mimicINT communicates with, references and/or uses the following third-party softwares:

- Docker
- Singularity
- [Python](https://www.python.org/) with packages:
    - click
    - pandas
    - scipy 
- [Snakemake](https://snakemake.readthedocs.io/en/stable/)
- [IUPred](https://iupred2a.elte.hu/)
- [ClustalW](https://www.genome.jp/tools-bin/clustalw)
- [ClustalO](https://www.ebi.ac.uk/Tools/msa/clustalo/)
- [MUSCLE](https://www.ebi.ac.uk/Tools/msa/muscle/)
- [Blast](https://blast.ncbi.nlm.nih.gov/Blast.cgi)
- [SLiMSuite](https://github.com/slimsuite)
- [InterProScan](https://www.ebi.ac.uk/interpro/search/sequence/)
- [R](https://www.r-project.org/) and [Rstudio](https://www.rstudio.com/) with packages:
    - BiocManager
    - ggplot2
    - plotly
    - ggalluvial
    - gridExtra
    - ggpubr
    - getopt
    - knitr
    - kableExtra
    - formatR
    - xtable
    - devtools
    - ramnathv/htmlwidgets
    - rstudio/DT
    - htmltools
    - davidgohel/ggiraph
    - getopt
    - ggplot2
    - plotly
    - data.table
    - gprofiler2
- [Pandoc](https://pandoc.org/)
- [Graphviz](https://graphviz.org/)
- [Oracle OpenJDK 11](https://openjdk.java.net/)




## Use mimicINT - Quick start

The current documentation provides an example of use of mimicINT (main workflow) to predict interactions between Lake Victoria Marburg Virus (MARV) sequences and the human proteins. For convenience of use, this example can be run on a workstation (16 Go RAM, 6 CPUs).


### mimicINT manuals

A manual is available for each workflow:
 
- [Read the mimicINT main workflow manual](mimicINT_InterPro/docs/manual.md)
 
- [Read the mimicINT randomization workflow manual](compute_slim_probability/docs/manual.md)

Please check these manuals as they provide extensive information about each workflow, notably about the available options.



### Install mimicINT

Check the **System requirement and dependencies** section.



### Prepare the inputs

#### Inputs required

The mimicINT main workflow requires the following inputs:

- **3did:** A `3did_flat` file provided by [the database of three-dimensional interacting domains (3did)](https://3did.irbbarcelona.org/). The current version of this file can be download at [https://3did.irbbarcelona.org/download/current/3did_flat.gz](https://3did.irbbarcelona.org/download/current/3did_flat.gz).

- **ELM classes:** A file ELM classes provided by the [Eukaryotic Linear Motif (ELM) resource](http://elm.eu.org/index.html). You can download a list of ELM classes at [http://elm.eu.org/downloads.html#classes](http://elm.eu.org/downloads.html#classes) or get the current version at [http://elm.eu.org/elms/elms_index.tsv](http://elm.eu.org/elms/elms_index.tsv).

- **ELM instances:** A file of ELM instances provided by the [Eukaryotic Linear Motif (ELM) resource](http://elm.eu.org/index.html). You can download a list of ELM instances at [http://elm.eu.org/downloads.html#instances](http://elm.eu.org/downloads.html#instances). You can download the current list of true positive instances for *H. sapiens* at [elm.eu.org/instances.tsv?q=None&taxon=Homo%20sapiens&instance_logic=true%20positive](elm.eu.org/instances.tsv?q=None&taxon=Homo%20sapiens&instance_logic=true%20positive).

- **ELM - domains interactions:** A file of ELM instances provided by the [Eukaryotic Linear Motif (ELM) resource](http://elm.eu.org/index.html). You can download a list of ELM - domain interactions [http://elm.eu.org/downloads.html#interactions](http://elm.eu.org/downloads.html#interactions) or get the current version at [http://elm.eu.org/infos/browse_elm_interactiondomains.tsv](http://elm.eu.org/infos/browse_elm_interactiondomains.tsv).

For additional information regarding the content and format of the 3did, ELM classes, ELM instances and ELM - domains interactions files, please check the [3did](https://3did.irbbarcelona.org/) and [ELM](http://elm.eu.org/index.html) documentations.


- **Target InterPro annotations:** A file containing all the InterPro annotations for the reviewed proteins of the target species. This file may be generated using the REST API of the [European Bioinformatics Institute (EMBL-EBI)](https://www.ebi.ac.uk/). You may check the official documentation of this API at [https://www.ebi.ac.uk/ena/xref/rest/](https://www.ebi.ac.uk/ena/xref/rest/) as well as the documentation of the script `common/script/prepare_input/download_interpro_annotations_for_proteome.py` file for more information about its content and format.

- **Pfam - InterPro mapping:** A file containing the mapping of the Pfam entries onto InterPro. This file may be generated using the REST API of the [European Bioinformatics Institute (EMBL-EBI)](https://www.ebi.ac.uk/). You may check the official documentation of this API at [https://www.ebi.ac.uk/ena/xref/rest/](https://www.ebi.ac.uk/ena/xref/rest/) as well as the documentation of the script `common/script/prepare_input/download_pfam_interpro_mapping.py` file for more information about its content and format.

- **Query sequences:** The amino acid sequences of the query species as a fasta file. Several header formats are supported by mimicINT (see [mimicINT main workflow manual](mimicINT_InterPro/docs/manual.md) for more information) but we suggest to use fasta headers following the [UniProt conventions](https://www.uniprot.org/help/fasta-headers).



#### Get the inputs

For this demo, you can:

1. Download a copy of the demo files from Zenodo ([![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7307993.svg)](https://doi.org/10.5281/zenodo.7307993)) as a `.tar.gz` archive.

2. Download or generate the inputs by your own, notably using the web interfaces of the various databases previously described.

3. Download the inputs by executing the following steps:

```
# Get the 3did and ELM files
bash common/script/prepare_input/download_input_files.sh

# Get the target - InterPro annotations
python3.5 common/script/prepare_input/download_interpro_annotations_for_proteome.py --proteomeID UP000005640 > input/hsapiens_interpro_annotations.tsv

# Get the Pfam - InterPro mapping file
python3.5 common/script/prepare_input/download_pfam_interpro_mapping.py > input/pfam_interpro_mapping.tsv
```

The query sequence file must be downloaded from UniProtKB web interace [https://www.uniprot.org/uniprot/?query=reviewed%3Ayes%20taxonomy%3A33727&columns=id%2Centry%20name%2Creviewed%2Cprotein%20names%2Cgenes%2Corganism%2Clength](https://www.uniprot.org/uniprot/?query=reviewed%3Ayes%20taxonomy%3A33727&columns=id%2Centry%20name%2Creviewed%2Cprotein%20names%2Cgenes%2Corganism%2Clength) as fasta format.

**Caution**:
    - You need Python3.5 to be installed to run these scripts. 
    - The ELM instances file contains the true positive instances for *H. sapiens*. For other runs, you may be willing to download other instances files from ELM.
    - The target InterPro annotations downloads file for *H. sapiens* proteome. The `--proteomeID` option may be used to download annotation for another species.
    - Depending on the query and target species you are studying, you may be willing to use your own ELM instances, target InterPro annotations and query sequences files. The 3did, ELM classes, ELM - domains interactions and Pfam - InterPro mapping files download using the scripts provided with mimicINT can be used in most cases.


You should get the following files:

```
input
├── 3did_flat
├── domain_scores.tsv
├── elm_classes.tsv
├── elm_instances.tsv
├── elm_interaction_domains.tsv
├── hsapiens_interpro_annotations.tsv
├── MARV.fasta
└── pfam_interpro_mapping.tsv
```

*NB:* The names of these files can be modified, as they are set in the config file of the mimicINT workflows.

*NB:* The (optional) file `domain_scores.tsv` must be downloaded from the Zenodo archive.



### Prepare the configuration file

The parameters and options accepted by mimicINT need to be set in the config file. Read the [mimicINT main workflow manual](mimicINT_InterPro/docs/manual.md) for extensive information about the parameter and options. 

Examples of config files are available for each workflow at `mimicINT_InterPro/config/config.yaml` and `compute_slim_probability/config/config.yaml`. The demo files from Zenodo([![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7307993.svg)](https://doi.org/10.5281/zenodo.7307993)) includes an example of config file for the mimicINT main workflow.

**Caution:** The config file needs to be adapted to your personal case of use.



### Prepare the configuration file for clusters

When considering to run mimicINT on cluster, an additional config file as `.json` format must be edited. Please check the [Snakemake documentation about cluster execution](https://snakemake.readthedocs.io/en/stable/executing/cluster.html) for more information regarding the options and configuration to run mimicINT on HPC clusters.

Examples of config files are available for each workflow at `mimicINT_InterPro/config/config_cluster.json` and `compute_slim_probability/config/config_cluster.json`. 

**Caution:** The cluster config file needs to be adapted to your personal case of use. The cluster config file format may vary depending on the configuration of the cluster you are using (batcher etc.). Check the documentation provided by the computing centre or contact the administrator of your cluster for more information.


### Start mimicINT

As mimicINT workflows are based on Snakemake, all Snakemake options can be used with mimicINT.

To start the demo run, you may run the following command lines:

```
bash mimicINT_InterPro/workflow/run_mimicINT_InterPro.sh
```



## Additional information

### Tree view

At the end of the procedure, *i.e.* after having successfully: 

- Clone the GitHub repository
- Download the data sources and cross-references
- Download the Dockers and Singularity images
- Install Docker, Docker-compose and Singularity
- Load the Docker images on your system and start the containers
- Run the source code to build the databases for one species (either for *H.sapiens* or *M.musculus*)

the tree folder should look like the following one:

```
.
├── common
│   ├── Docker
│   │   ├── create_all_singularity2.sh
│   │   ├── create_all_singularity3.sh
│   │   ├── data_parse
│   │   │   ├── dockerfile
│   │   │   ├── readme.txt
│   │   │   └── tagc-mimicint-data-parse.img
│   │   ├── docker_to_singularity.sh
│   │   ├── domain_detect
│   │   │   ├── dockerfile
│   │   │   ├── readme.txt
│   │   │   └── tagc-mimicint-domain-detect.img
│   │   ├── miscellaneous
│   │   │   └── graphviz
│   │   │       ├── dockerfile
│   │   │       ├── readme.txt
│   │   │       └── tagc-mimicint-misc-graphviz.img
│   │   ├── R
│   │   │   ├── dockerfile
│   │   │   ├── readme.txt
│   │   │   └── tagc-mimicint-r.img
│   │   ├── Rstudio
│   │   │   ├── dockerfile
│   │   │   ├── readme.txt
│   │   │   ├── tagc-mimicint-rstudio.img
│   │   │   └── userconf.sh
│   │   └── slim_detect
│   │       ├── dockerfile
│   │       ├── iupred.tar.gz
│   │       ├── ncbi-blast-2.7.1+-x64-linux.tar.gz
│   │       ├── readme.txt
│   │       └── tagc-mimicint-slim-detect.img
│   ├── docs
│   │   ├── folder.txt
│   │   └── manual.md
│   └── script
│       ├── miscellaneous
│       │   ├── plot_dag.sh
│       │   └── plot_rulegraph.sh
│       ├── prepare_input
│       │   ├── download_input_files.sh
│       │   ├── download_interpro_annotations_for_proteome.py
│       │   ├── download_pfam_interpro_mapping.py
│       │   └── rm_fasta_header_duplicates.py
│       └── prepare_run
│           └── prepare_tool_folder.sh
├── input
│   ├── 3did_flat
│   ├── domain_scores.txt
│   ├── elm_classes.tsv
│   ├── elm_instances.tsv
│   ├── elm_interaction_domains.tsv
│   ├── hsapiens_interpro_annotations.tsv
│   ├── MARV.fasta
│   ├── pfam_interpro_mapping.tsv
│   └── README.md
├── job_status
│   ├── end_aggregate_detect_slim_query_output
│   ├── end_compute_query_disorder_propensity
│   ├── end_ddi_template_pfam_to_interpro
│   ├── end_detect_domain_query
│   ├── end_detect_slim_query_MARV_0
│   ├── end_elm_domain_interactions_to_interpro
│   ├── end_extract_binary_interactions
│   ├── end_filter_dmi_on_domain_score
│   ├── end_generate_json_interaction_inference
│   ├── end_generate_json_query_features
│   ├── end_get_target_prot_with_potential_interactions
│   ├── end_interaction_inference
│   ├── end_match_query_sqce_names
│   ├── end_parse_3did
│   ├── end_parse_domain_query
│   ├── end_parse_elm
│   ├── end_parse_slim_query
│   ├── end_simplify_sequence_names
│   ├── end_split_query_dataset
│   ├── end_target_enrichment_gprofiler
│   ├── END_WORKFLOW
│   ├── start_aggregate_detect_slim_query_output
│   ├── start_compute_query_disorder_propensity
│   ├── start_ddi_template_pfam_to_interpro
│   ├── start_detect_domain_query
│   ├── start_detect_slim_query_MARV_0
│   ├── start_elm_domain_interactions_to_interpro
│   ├── start_extract_binary_interactions
│   ├── start_filter_dmi_on_domain_score
│   ├── start_generate_json_interaction_inference
│   ├── start_generate_json_query_features
│   ├── start_get_target_prot_with_potential_interactions
│   ├── start_interaction_inference
│   ├── start_match_query_sqce_names
│   ├── start_parse_3did
│   ├── start_parse_domain_query
│   ├── start_parse_elm
│   ├── start_parse_slim_query
│   ├── start_simplify_sequence_names
│   ├── start_split_query_dataset
│   └── start_target_enrichment_gprofiler
├── log
│   └── parameters.tsv
├── mimicINT_InterPro
│   ├── config
│   │   └── config.yaml
│   ├── docs
│   │   ├── manual.md
│   │   ├── mimicint_snakefile.png
│   │   ├── mimicint_snakefile_dag.png
│   │   ├── mimicint_snakefile_rulegraph.png
│   │   └── run_folder.txt
│   ├── script
│   │   └── run_slimprob.sh
│   ├── src
│   │   └── fr
│   │       └── tagc
│   │           └── mimicint
│   │               ├── compute_query_disorder.py
│   │               ├── ddi_pfam_to_interpro.py
│   │               ├── elm_domain_interactions_to_interpro.py
│   │               ├── enrichment_gprofiler.R
│   │               ├── get_target_prot_with_potential_interactions.py
│   │               ├── interaction_inference.py
│   │               ├── match_query_sqce_names.py
│   │               ├── parsing_scripts
│   │               │   ├── aggregate_slimprob_list.py
│   │               │   ├── aggregate_slimprob_res.py
│   │               │   ├── extract_binary_interactions.sh
│   │               │   ├── filter_dmi_on_domain_score.py
│   │               │   ├── filter_parsed_elm_on_slim_pval_v2.py
│   │               │   ├── interaction_all_to_json.py
│   │               │   ├── parser3did.py
│   │               │   ├── parserELM.py
│   │               │   ├── parser_res_interproscan.py
│   │               │   ├── parser_res_slimprob.py
│   │               │   ├── query_proteins_features_to_json.py
│   │               │   └── split_fasta_file.py
│   │               ├── simplify_sqce_names.py
│   │               └── util
│   │                   └── option
│   │                       └── OptionManager.py
│   └── workflow
│       ├── mimicint_interpro_snakefile
│       └── run_mimicint_InterPro.sh
├── output
│   └── mimicINT_InterPro
│       ├── 0_parse_3did
│       │   ├── parsed_3did_interpro.txt
│       │   └── parsed_3did.txt
│       ├── 1_parse_elm
│       │   ├── elm_domain_interactions_interpro.tsv
│       │   ├── parsed_elm_classes.split.motifs
│       │   ├── parsed_elm_classes.txt
│       │   └── parsed_elm_summary.tsv
│       ├── 2_target_with_dom_in_templates
│       │   └── target_with_domains_with_templates_of_inter.tsv
│       ├── 3_detect_domain_query
│       │   ├── parsed_query_domain_interpro.tsv
│       │   └── query_domain_interpro.tsv
│       ├── 4_slim_detect
│       │   ├── aggregate_slimprob_iuscores.log
│       │   ├── aggregate_slimprob_list.log
│       │   ├── aggregate_slimprob_res.log
│       │   ├── disorder_propensities.tsv
│       │   ├── iuscore
│       │   │   ├── P27588.iupred.txt
│       │   │   ├── P31352.iupred.txt
│       │   │   ├── P35253.iupred.txt
│       │   │   ├── P35256.iupred.txt
│       │   │   ├── P35258.iupred.txt
│       │   │   ├── P35259.iupred.txt
│       │   │   └── P35260.iupred.txt
│       │   ├── MARV_0
│       │   │   ├── query_MARV_0_slimprob.log
│       │   │   ├── query_MARV_0_slim_slimprob.occ.split.tsv
│       │   │   ├── query_MARV_0_slim_slimprob.occ.tsv
│       │   │   ├── query_MARV_0_slim_slimprob.split.tsv
│       │   │   ├── query_MARV_0_slim_slimprob.tsv
│       │   │   └── SLiMProb_MARV_0
│       │   │       ├── MARV_0.dis.tdt
│       │   │       ├── MARV_0.FreqDis.masked.fas
│       │   │       ├── MARV_0.iupred.txt
│       │   │       ├── MARV_0.parsed_elm_classes.FreqDis.pickle.gz
│       │   │       ├── MARV_0.self.blast
│       │   │       ├── MARV_0.slimdb
│       │   │       └── MARV_0.upc
│       │   ├── parsed_query_slim_slimprob.tsv
│       │   ├── query_seqnames_match.tsv
│       │   ├── query_slim_slimprob.occ.tsv
│       │   └── query_slim_slimprob.tsv
│       ├── 4_splitted_query
│       │   └── MARV_0.fasta
│       ├── 5_interactions
│       │   ├── all_interactions.json
│       │   ├── filtered_dmi_interactions.tsv
│       │   ├── filtered_domain_score.tsv
│       │   ├── inferred_all_interactions.tsv
│       │   ├── inferred_binary_interactions.ncol
│       │   ├── inferred_ddi_interactions.tsv
│       │   └── inferred_dmi_interactions.tsv
│       ├── 6_summary
│       │   └── query_proteins_features.json
│       ├── 7_renamed_sequences
│       │   ├── all_interactions.json
│       │   ├── all_interactions.tsv
│       │   ├── binary_interactions.ncol
│       │   ├── dd_interactions.tsv
│       │   ├── dm_interactions.tsv
│       │   ├── query_disorder_prop.tsv
│       │   ├── query_domains.tsv
│       │   ├── query_features.json
│       │   ├── query_slims.tsv
│       │   └── sequence_names.tsv
│       └── 8_gprofiler
│           ├── gprofiler_result.tsv
│           ├── index_files
│           │   ├── crosstalk-1.1.0.1
│           │   │   ├── css
│           │   │   │   └── crosstalk.css
│           │   │   └── js
│           │   │       ├── crosstalk.js
│           │   │       ├── crosstalk.js.map
│           │   │       ├── crosstalk.min.js
│           │   │       └── crosstalk.min.js.map
│           │   ├── htmlwidgets-1.5.1
│           │   │   └── htmlwidgets.js
│           │   ├── jquery-1.11.3
│           │   │   ├── jquery-AUTHORS.txt
│           │   │   ├── jquery.js
│           │   │   ├── jquery.min.js
│           │   │   └── jquery.min.map
│           │   ├── plotly-binding-4.9.2.1
│           │   │   └── plotly.js
│           │   ├── plotly-htmlwidgets-css-1.52.2
│           │   │   └── plotly-htmlwidgets.css
│           │   ├── plotly-main-1.52.2
│           │   │   └── plotly-latest.min.js
│           │   └── typedarray-0.1
│           │       └── typedarray.min.js
│           ├── index.html
│           └── unique_target_interactors.txt
├── temp
└── tools
    └── iupred
        ├── histo
        ├── histo_casp
        ├── histo_sum
        ├── iupred
        ├── iupred.c
        ├── LICENSE
        ├── P53_HUMAN.seq
        ├── README
        ├── ss
        └── ss_casp
```
