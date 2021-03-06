# QC'd - Quality control and Contamination Detection 


## Synopsis
 
- Calculate Raw sequencing coverage from Fastq reads, 
- Assess read quality and generate aggregated multiqc report from FastQC results, 
- Downsamples fastq reads to 100X and screen downsampled reads for possible contamination using Kraken,
- Estimates read depth from mapped read alignments - uses bwa, samtools and GATK,
- Estimate MLST using Ariba,

## Input

- A file containing sample names of forward paired/single-end reads. One sample per line.
- Set path to Minikraken or custom pre-built Kraken database in config file.
- Set Ariba MLST database path in config file.
- Type of analysis to run. Options: coverage,quality,kraken_contamination,coverage_depth,mlst

## Analysis options:


**coverage:** calculate raw sequencing coverage given a genome size; Assumes all filename/samples belong to one species type.

**quality:** run FastQC and generate quality reports. Also, merge multiple fastqc reports to generate MultiQC reports. 

**kraken_contamination:** Scan reads against a minikraken or pre-built custom Kraken database to estimate species abundance.

**coverage_depth:** calculate read depth using GATK DepthofCoverage tool. Requires a reference genome for read mapping.

**mlst:** estimates ST by screening against MLST database using Ariba

**summary:** Summarizes results from all the above analysis into a single summary report - summary.tsv

```

usage: qc.py [-h] [-samples SAMPLES] [-config CONFIG] [-dir DIRECTORY]
             [-analysis ANALYSIS_NAMES] [-o OUTPUT_FOLDER] [-type TYPE]
             [-cluster CLUSTER] [-genome_size SIZE] [-prefix PREFIX]
             [-reference REFERENCE] [-downsample DOWNSAMPLE]
             [-scheduler SCHEDULER] [-dryrun] [-mlst_db MLST_DB]

QC'd - Quality control and Contamination Detection Workflow

optional arguments:
  -h, --help            show this help message and exit

Required arguments:
  -samples SAMPLES      A file containing filenames of forward-paired end or single-end reads. One Sample per line
  -dir DIRECTORY        Path to Sequencing Reads Data directory. NOTE: Provide full/absolute path.
  -analysis ANALYSIS_NAMES
                        comma-seperated analysis names to run
                        [Options: coverage,quality,kraken_contamination,kraken_report,coverage_depth].
                        Example: "-analysis coverage,quality" - This will estimate coverage and quality for the samples given in -samples
  -o OUTPUT_FOLDER      Output Folder Path ending with output directory name to save the results.
                        Creates a new output directory path if it doesn't exist.
  -type TYPE            Type of analysis: SE or PE
  -genome_size SIZE     Estimated Genome Size - to be used for estimating coverage in downsampling steps
  -prefix PREFIX        Use this prefix to save the results files

Optional arguments:
  -config CONFIG        Path to Config file, Make sure to check config settings before running pipeline.
                        Note: Set Kraken database path under [kraken] config section
  -cluster CLUSTER      Run in one of the two modes. 
                        Default is local for coverage and fastqc analysis.
                        For all the other analysis Default is cluster. The pipeline prefers cluster mode to generate SLURM/PBS jobs.
                        Modes: local or cluster
  -reference REFERENCE  Reference genome to use for calculating GATK Depth of coverage.
  -downsample DOWNSAMPLE
                        yes/no: Downsample Reads data to default depth of 100X
  -scheduler SCHEDULER  
                        Type of Scheduler for generating Kraken cluster jobs: PBS, SLURM, LOCAL
  -dryrun               Perform a trial run without submitting cluster jobs
  -mlst_db MLST_DB      Ariba MLST database path

```

## Results:

**coverage:** tab-seperated prefix_Final_Coverage.txt report.

**quality:** FastQC/MultiQC html reports will be generated under prefix_Fastqc

**multiqc:** a multiqc html report aggregated from each fastqc results generated in prefix_Multiqc_reports

**kraken_contamination:** Results generated by Kraken will be saved under prefix_Kraken_results.  

**coverage_depth:** GATK depth_of_coverage statistics for each sample against the reference genome generated in prefix_Coverage_depth .

**mlst:** Ariba MLST report for each sample generated in prefix_MLST_results

## Installation

The pipeline can be set up in two easy steps:

> 1. Clone the github directory onto your system.

```
git clone https://github.com/alipirani88/QC-d.git

```

> 2. Use QC-d/QC_env.yml and QC-d/aribamlst_env.yml files to create conda environment for qc pipeline and ariba MLST calling.

Create two new environments - varcall and varcall_gubbins
```
conda env create -f QC-d/QC_env.yml -n qc_env
conda env create -f QC-d/aribamlst_env.yml -n ariba_env
```

Check installation

```
conda activate qc_env

python QC-d/qc.py -h
```

## Quickstart

Run QC'd pipeline on samples in test_readsdir. 

```

python QC-d/qc.py \
-samples filenames \
-dir /Path-To-Your/test_readsdir/ \
-analysis coverage,quality,kraken_contamination,coverage_depth,mlst \
-o /Path-To-Your/output-folder/ \
-type PE \
-genome_size 5000000 \
-prefix Test \
-cluster cluster \
-config QC-d/config \
-scheduler SLURM \
-downsample yes \
-reference KPNIH1
-dryrun

```

The above command will calculate the raw coverage and fastq statistics, generate fastqc report, gather fastqc reports to generate a multiqc report. It will however not run kraken/gatk/ariba but instead generate slurm jobs for each analysis without submitting it to cluster. User can submit the later after verifying that all the SLURM/PBS arguments are set properly.

The kraken jobs will be generated in prefix_Kraken_results folder. The jobs will downsample the fastqc reads if they are greater than 100X, scans downsampled reads against Kraken database(path should be provided in config file) and generate a kraken report.

The coverage depth jobs will be generated in prefix_Coverage_depth folder. The jobs will map reads against the reference genome(-reference), converts and sorts the BAM files and calculate reads depth with GATK.

The ariba mlst jobs will be generated in prefix_MLST_results folder. In order to run ARIBA MLST, you will need to activate the ariba environment (shown above - Installation step 2) and submit the jobs. Make sure to set the Ariba MLST database in config file.

Once all the analysis jobs are completed, run the summary analysis to generate a summary report. This analysis will summarize the results of each individual analysis into a single summary report - summary.tsv


```

python QC-d/qc.py \
-samples filenames \
-dir /Path-To-Your/test_readsdir/ \
-analysis summary \
-o /Path-To-Your/output-folder/ \
-type PE \
-genome_size 5000000 \
-prefix Test \
-cluster cluster \
-config QC-d/config \
-scheduler SLURM \
-downsample yes \
-reference KPNIH1
-dryrun

```