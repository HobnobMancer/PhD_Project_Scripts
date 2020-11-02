# pyrewton

[![DOI](https://zenodo.org/badge/243783792.svg)](https://zenodo.org/badge/latestdoi/243783792)
[![Funding](https://img.shields.io/badge/Funding-EASTBio-blue)](http://www.eastscotbiodtp.ac.uk/)
[![PhD licence](https://img.shields.io/badge/Licence-MIT-green)](https://github.com/HobnobMancer/PhD_Project_Scripts/blob/master/LICENSE)
[![CircleCI](https://circleci.com/gh/HobnobMancer/pyrewton.svg?style=shield)](https://circleci.com/gh/HobnobMancer/PhD_Project_Scripts)
[![codecov](https://codecov.io/gh/HobnobMancer/pyrewton/branch/master/graph/badge.svg)](https://codecov.io/gh/HobnobMancer/pyrewton)
[![Documentation Status](https://readthedocs.org/projects/pyrewton/badge/?version=latest)](https://pyrewton.readthedocs.io/en/latest/?badge=latest)
[![Python](https://img.shields.io/badge/Python-v3.7.---orange)](https://www.python.org/about/)
[![Research](https://img.shields.io/badge/Bioinformatics-Protein%20Engineering-ff69b4)](http://www.eastscotbiodtp.ac.uk/eastbio-student-cohort-2019)

_Please find more detailed documentation for operation and troubleshooting at [Read the Docs](https://phd-project-scripts.readthedocs.io/en/latest/)_

## Contents

1. [Overview](#Overview)
2. [Installation](#Installation)
    - [Requirements](#Requirements)
3. [Directories](#Directories)
4. [Modules](#Modules)
    - [genbank](#genbank)
    - [cazymes](#cazymes)
        - [uniprot](#uniprot)
        - [prediction](#prediction)
        
## Overview

Pyrewton is a Python3 script package for the automated identification of CAZyomes (all carbohydrates encoded within the genome of a given species). The package is run at the command line and free to use under the MIT license.

Pyrewton supports:
- Downloading of all genomic assemblies (as GenBank files .gbff) from the [NCBI Assembly database](https://www.ncbi.nlm.nih.gov/assembly)
associated with each species passed to the programme
- Retrieval of all annotated protein sequences from GenBank (.gbff) files
- Retrieve proteins entries from [UniProtKB](https://www.uniprot.org/), using a JSON file to configure the queries

Features currently in development:
- Use the 3rd-party tools [dbCAN](https://github.com/linnabrown/run_dbcan), [CUPP](https://www.bioengineering.dtu.dk/english/researchny/research-sections/section-for-protein-chemistry-and-enzyme-technology/enzyme-technology/cupp), and [eCAMI](https://github.com/zhanglabNKU/eCAMI) to predict the which query protein sequences are CAZymes and predict their CAZy family
- Evaluate the accuracy of the CAZyme prediction tools to distinguish between CAZyme and non-CAZyme protein sequences
- Evaluate the accuracy of the CAZyme prediction tools to the correct CAZy family
- Produce a report of the CAZyme prediction tool evaluation

Development plans are stored within the [Wiki](https://github.com/HobnobMancer/pyrewton/wiki).
<p>&nbsp;</p>

## Installation

1. Navigate the directory you wish to store pyrewton in, then clone this repository.
`git clone https://github.com/HobnobMancer/pyrewton.git`

1. Create a virtual environment with dependencies, then activate the environment.   
`conda create -n <venv_name> python=3.8 diamond hmmer prodigal -c conda-forge -c bioconda`   
`conda activate <venv_name>`

2. Install all requirements from requirements.txt file. The requirements.txt file is stored in the root of this repository.  
`pip3 install -r <path to requirements.txt file>`   

3. Install pyrewton.
`pip3 install -e <path to directory containing setup.py file>`   
Do not forget to use the **-e** option when install using pip3, otherwise each time pyrewton is invoked a ModuleNotFound error will be raised. Pass the path to the **directory** containign the setup.py file not the path to the setup.py file; if you are currently in the root directory of the repoistory where the file is located, simply use '.' to indicate the current working directory.

4. Install third party tools.   
Pyrewton invokves 3 third party tools: dbCAN, CUPP and eCAMI.

To install dbCAN follow the instructions within their [GitHub repository](https://github.com/linnabrown/run_dbcan), **BUT ignore** steps 1 and 2 of their installtion guide, becuase the necessary virtual environment was already created in the second step of this installation and it meets all requirements of dbCAN. Install dbCAN within **'pyrewton/cazymes/prediction/tools/dbcan'** directory within the repository, otherwise pyrewton will not be able to find the tool.  

To install eCAMI follow the instructions within their [GitHub respository](https://github.com/yinlabniu/eCAMI). eCAMI must be installed within the directory pyrewton/cazymes/prediction/tools/ecami. Following the method from the eCAMI repository will write eCAMI to 'pyrewton/cazymes/prediction/tools/ecami/**eCAMI**', to avoid this perform the installation within 'pyrewton/cazymes/prediction/tools' and rename 'eCAMI' to 'ecami', thus install eCAMI in **'pyrewton/cazymes/prediction/tools/ecami'**.   

To install CUPP download the CUPP files from the [DTU Bioengineering server](https://www.bioengineering.dtu.dk/english/ResearchNy/Research-Sections/Section-for-Protein-Chemistry-and-Enzyme-Technology/Enzyme-Technology/CUPP), and store the files in **'pyrewton/cazymes/prediction/tools/cupp'**. It is not necessary to download all the files becuase the .tar and .tar.gz directories each contain all the files, therefore, download either the .tar _or_ .tar.gz directories and unpackage them or download all the files located within 'CUPP_v1.0.14'.

<p>&nbsp;</p>

## Requirements

POISx or Mac OS, or linux emulator   
Python version 3.7+   
Miniconda3 or Anaconda managed microenvironment, incorporated code checkers are included in list form in 'requirements.txt'.   
Miniconda3 environment file is also available in the GitHub repository: 'environment.yml'.   
For all required Python libraries please read 'requirements.txt'.   

<p>&nbsp;</p>

## Directories

Below is a directory plan of this repository, followed by a brief overview of each directories role , to facilitate navigation through the repository.

### **assets**

Directory containing all files needed for the GitHub page, created for easy access to accompanying Jupyter notebooks.

### **docs**

Directory containing files to build documentation hosted at ReadTheDocs.

### **notebooks**

Directory containing all Jupyter notebooks, and html copies used for easier in-browser viewing via the GitHub pages.

### **tests**

Directory containing all `pytest` files for testing `pyrewton`, including subdirectories for test inputs and targets. Each module/submodule has its own specific test input and target subdirectory.

### **pyrewton**

Directory containing all `pyrewton` program modules (including all submodules and Python scripts).
<p>&nbsp;</p>

## Modules

_Please find more detailed documentation at for operation and troubleshooting at [Read the Docs](https://phd-project-scripts.readthedocs.io/en/latest/)_

This is an overview of the functionalities of each module within `pyrewton`, as well as basics of operation. For more detailed documentation on the operation of each module and indiviudal Python scripts please see the documentation at [Read the Docs](https://phd-project-scripts.readthedocs.io/en/latest/)

### **utilities**

Contains all functions that are called from other Python scripts for building command-line parsers and loggers.

### **file_io**

Contains functions that are called from other Python scripts for handling directories and files in `pyrewton`, including retrieving program inputs and creating output directories.

### **genbank**

Directory containing all submodules that are involved in retrieving handling GenBank files. This includes retrieval of GenBank files from GenBank, and retrieval of protein sequences from GenBank files.

#### **get_ncbi_genomes**
This submodule is for the retrieval of genomic assemblies (as .gbff files) for each species listed in a plain text file (.txt). Each line of the plain text file must contain a single, unique species, for an example see 'get_ncbi_genomes_template_input_file.txt' within the directory. The species can be specified by taxonomy ID (using the 'NCBI:txid' prefix) or scientific name. `get_ncbi_genomes` will retrieve the scientific name or taxonomy depending on which is given, and will write out a dataframe containing the scientific name, NCBI taxonomy ID and all accession numbers of all genomic assemblies retrieved from NCBI.

**Note:** What is meant by all genomic assemblies is the latest version of all genomic assemblies, taking preference for GenBank files over reference assemblies. If not GenBank (identified by the 'GCA' prefix) assembly if available then the latest version of the reference assembly (identified by the 'GCF' prefix) will be retrieved.

When invoking `get_ncbi_genomes` a user email must be provided. This is a requirements of Entrez, the search and retrieval system of NCBI, which is accessed during the retrieval of taxonomy information and genomic assemblies. 

An example of the basic operation is:
`python3 get_ncbi_genomes <user_email> <-i path_to_input_.txt> <-o directory_to_store_assemblies> <-d species_dataframe_output_path`

All command options can be viewed by using `python3 get_ncbi_genomes -h` or `python3 get_ncbi_genomes --help`, and at [ReadtheDocs](https://phd-project-scripts.readthedocs.io/en/latest/genbank.html#get-ncbi-genomes).

#### **get_genbank_proteins**
This submodule is for the retrieval of proteins sequences from GenBank (.gbff) genomic assemblies. The protein sequences are identified as 'CDS' annotated features. The locus tag, gene start/end, gene ID, annotated function and protein sequence are retrieved and written out to a dataframe, with a unique protein on each line and including a columns for the host species scientific name, NCBI taxonomy and accession number of the host genomic assembly. The protein sequences are also written out to FASTA files, with a single FASTA file containing all the protein sequences from only one genomic assembly. Therefore, each genomic assembly input results in one FASTA file output.

When invoking `get_genbank_proteins` the path to the input dataframe (which is the output from `get_ncbi_genomes`) and the directory containing the genomic assemblies must be parsed, and in this order.

An example of basic operation is:
`python3 get_genbank_proteins <path_to_input_df> <path_to_assemly_dir>`

All command options can be viewed by using `python3 get_ncbi_genomes -h` or `python3 get_genbank_proteins --help`, and at [ReadtheDocs](https://phd-project-scripts.readthedocs.io/en/latest/annotations.html).

### **cazymes**
This module is involved in the identification and prediction of CAZymes.

#### **uniprot**
This submodule retrieved protein from UniProtKB. The query criteria are configured by a YAML file. The configuration file incorporates two keys: 'tax_ids' and 'queries'. Under 'tax_ids' list the NCBI taxonomy ID of the species the search is to be restricted to. Under 'queries' list the queries to be performed (for each taxonomy ID if given) using the UniProt query [syntax](https://www.uniprot.org/help/text-search) and query [fields](https://www.uniprot.org/help/query-fields). If only the taxonomy ID is given then all proteins for that taxonomy ID will be given. For an example configuration file see 'uniprot_config.yaml' in the `uniprot` directory.

The submodule writes out a dataframe containing
- NCBI taxonomy ID of the host species
- scientific name of the host species
- UniProt entry ID
- UniProt entry name
- Protein names
- EC numbe
- Protein length in amino acids
- Protein mass (Da)
- Domains
- Protein families in external database such as its [CAZy](www.cazy.org/) family
- Gene Ontology ID, molecular function and biological process annotations
- Protein sequence

The submodule also writes out all protein sequences to FASTA files, with each query to UniProt producing a single FASTA file containing all the resulting protein sequences retrieved from the query. The FASTA file names follow the format: 'uniprot_{uniprot_query}_{time_stamp}'. If only the taxonomy ID is given then the taxonomy ID will be written in the FASTA file name in the place of 'uniprot_query'.

When invoking the submodule `uniprot`, invoke the script `get_uniprot_proteins.py` and the path to the configuration must be provided.

An example of basic operation is:
`python3 get_uniprot_proteins <path_to_config_file.yaml>`

All command options can be viewed by using `python3 get_uniprot_proteins -h` or `python3 get_uniprot_proteins --help`. 'Read the Docs' documentation coming soon!

#### **prediction**

_This module is still in early development, on the branch `new_feature_CPT_evaluation`, more detailed documentation will be added post development._

This submodule is for the prediction if a query protein sequence is a CAZyme or non-CAZyme, and the prediction of the CAZy family if the protein is predicated to be a CAZyme.
<p>&nbsp;</p>


## Repository renamed 2020-10-05
**Note:** This repository was renamed from 'PhD_project_scripts' to 'pyrewton'.
