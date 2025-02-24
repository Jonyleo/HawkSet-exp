# HawkSet Artifact Evaluation

This document describes the content of this repo, which contains all materials need to build and execute all experiments in the paper "HawkSet: Automatic, Application-Agnostic, and Efficient Concurrent PM Bug Detection", submitted to Eurosys 2025.
DOI: https://doi.org/10.5281/zenodo.14917473.

*Note*: If you are looking for HawkSet itself, as a standalone tool, you can ignore this section of the artifact, and move on to `HawkSet/README.md`

# Overview

```
HawkSet-exp
│   config.sh            - Configuration for experiments
│   launch.sh            - Launches docker containers
│   build_hawkset.sh     - Builds HawkSet and evaluation requirements
│   build_pmrace.sh      - Builds PMRace
│
└─── applications        - Docker instances for each applications under test
└─── patches             - Patch files for some applications
└─── config              - Configuration files for the synchronization primitives
└─── artifact_evaluation - Scripts and guide for the artifact_evaluation
└─── HawkSet             - HawkSet source code submodule
└─── pmrace-vagrant      - PMRace source code and evaluation submodule
```

Each application tested by HawkSet is packaged as a Docker container for ease of use.
All containers inherit from the main HawkSet container.

As stated in the paper, applications which do not employ standard synchronization primitives (such as pthread or libpmemobj's mutexes), require a configuration file with information regarding each primitive.

As described in the paper, some application require modification to their source code for analysis, when the synchronization primitives cannot be easily abstracted from the rest of the code.
Furthermore, to normalize the evaluation between all applications, we implemented a YCSB parser that maps each operation to the application under test. 

Each application requires slightly different parameters to execute, the runner scripts abstract that process away, and are used in the experiments.

See "Efficiently detecting concurrency bugs in persistent memory programs" for further details regarding PMRace

# Requirements

HawkSet was built and tested in Ubuntu 22.04.5 LTS and requires Docker (tested for version 27.5.0, but any modern version should suffice), if you are using a provided machine, the environment has been setup already.

The applications evaluated by HawkSet require specific CPU instructions, therefore your machine must support the following CPU feature flags:

- avx512vl 
- avx512bw 
- clwb 
- clflushopt 
- clflush 
- sse

Furthermore, the PMRace comparison requires Vagrant and Virtualbox, as well as the following hardware requirements:

- CPU: >= 16 threads
- DRAM: >= 32 GB
- DISK: ~100 GB

The script `requirements.sh` will check for suitability and install the requirements (except for docker which is not easily automated). Check out the official docker documentation for a step by step guide, found here https://docs.docker.com/engine/install/ubuntu/.

# Setup

Before starting the evaluation:

- Clone the repository https://github.com/Jonyleo/HawkSet-exp

```
~/$ git clone https://github.com/Jonyleo/HawkSet-exp 
```

- Initialize submodules

```
~/$ cd HawkSet-exp 
~/HawkSet-exp/$ git submodule update --init
```

- [OPTIONAL] Setting up PM.

HawkSet is able to analyse applications without using real or emulated PM, and we have found that this has a negligible impact in the results outlined in the paper.
**This is not required**, however, to run HawkSet on real PM, or emulated PM, follow these instructions.

*Note*: Whichever option is used, be sure to edit the HawkSet-exp/config.sh file, setting the PM_PATH environment variable to `/mnt/pmem0`

#### Setting up Persistent Memory

Assuming the device's name is `/dev/pmem0`:

```
sudo mkdir /mnt/pmem0
sudo mkfs.ext4 /dev/pmem0
sudo mount -t ext4 -o dax /dev/pmem0 /mnt/pmem0
sudo chmod -R 777 /mnt/pmem0
``` 

#### Emulating Persistent Memory using tmpfs

```
sudo mkdir /mnt/pmem0
sudo mount -t tmpfs -o rw,size=50G tmpfs /mnt/pmem0
sudo chmod -R 777 /mnt/pmem0
```

# Building HawkSet, Workloads and PMRace

The following commands builds every necessary artifact required for the evaluation. See below for time estimations.

### Build HawkSet and it's Workloads

```
~/HawkSet-exp/$ ./build_hawkset.sh 
```

Breakdown of building time (assuming a fresh start)

- Building HawkSet (~6 minutes)
- Building the Workloads (~15 minutes)

### Build PMRace

```
~/HawkSet-exp/$ ./build_pmrace.sh
```

This should take arround 1 hour

# Kick-the-tires Evaluation - Analysing Fast-Fair

To ensure everything is working properly, without waiting for long experiments, follow these steps to perform the analysis for one of the target applications - Fast-Fair.

### Analysing Fast-Fair under HawkSet (~5 minutes)

```
~/HawkSet-exp/$ mkdir output
~/HawkSet-exp/$ cd artifact_evaluation
~/HawkSet-exp/artifact_evaluation/$ ./analyze_application.sh ../output/kickthetires ffair
```

### Generating Figures and Tables

- Launch the hawkset-exp docker container which is ready for generating figures and tables

```
~/HawkSet-exp/artifact_evaluation/$ cd ..
~/HawkSet-exp/ ./launch.sh hawkset-exp
root@hawkset-exp:~# cd artifact_evaluation
```

- (Table 2): Persistency-induced Races  

```
root@hawkset-exp:~/artifact_evaluation# python3 disp_bug_table.py ../output/kickthetires
```

- (Figure 6) HawkSet's Metrics (memory and time elapsed)

```
root@hawkset-exp:~/artifact_evaluation# python3 gen_graphs.py ../output/kickthetires ../output/graphs
```

Note: If you are using a remote machine provided by us, you can extract the images for vieweing via scp, or mount the machine via sftp.

- (Table 4) Initialization Removal Heuristic

```
root@hawkset-exp:~/artifact_evaluation# python3 disp_irh_comparison.py ../output/kickthetires
```

- Exit the container and proceed to the full evaluation

### Simplified PMRace Comparison

Experiment 4 lastes for approximatelly 40 hours, to ensure everything is working properly, follow these steps to replicate a reduce version of the experiment.

**Note**: The results of this experiment should be ignored, they do not reflect the actual performance of PMRace nor HawkSet.

**Note**: If you are running the experiments docker container, exit and return to the host machine.

```
~/HawkSet-exp/artifact_evaluation/$ ./exp_pmrace_comparison.sh KTT
```

To generate a figure similar to Table 3, run the following command (disreguard the actual results, including NaNs and infs):

```
~/HawkSet-exp/artifact_evaluation/$ cd ..
~/HawkSet-exp/ ./launch.sh hawkset-exp
root@hawkset-exp:~# cd artifact_evaluation
root@hawkset-exp:~/artifact_evaluation# python3 disp_pmrace_comparison.py ffair ../pmrace_results ../output/pmrace_seeds/
```
