This document outlines the steps necessary to replicate the experiments present in the paper "HawkSet: Automatic, Application-Agnostic, and Efficient Concurrent PM Bug Detection", submitted to Eurosys 2025.

# Overview

1. Requirements and Setup
2. Building HawkSet, Workloads and PMRace
3. Kick-the-tires Evaluation
4. Experiment 1 (Table 2): Detecting Persistency-induced Races
5. Experiment 2 (Figure 6): Breakdown of HawkSet's metrics
6. Experiment 3 (Table 4): Breakdown of all reports 
7. Experiment 4 (Table 3): Comparison with PMRace

# 1. Requirements and Setup


HawkSet was built and tested in Ubuntu 22.04.5 LTS and requires Docker (tested for version 27.5.0), if you are using a provided machine, the environment has been setup already.

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
However, to run HawkSet on real PM, or emulated PM, follow these instructions.

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

# 2. Building HawkSet, Workloads and PMRace

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

# 3. Kick-the-tires Evaluation - Analysing Fast-Fair

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

# 4. Experiment 1 (Table 2): Detecting Persistency-induced Races (~2.5 Hours)

First, analyse all applications under HawkSet (this should take 2.5 hours).

```
~/HawkSet-exp/artifact_evaluation/$ ./analyze_all_applications.sh
```

Next, launch the hawkset-exp docker container which is ready for generating figures and tables

```
~/HawkSet-exp/artifact_evaluation/$ cd ..
~/HawkSet-exp/$ ./launch.sh hawkset-exp
root@hawkset-exp:~# cd artifact_evaluation
```

To output the detected bugs, similarly to Table 2, run the following command:

```
root@hawkset-exp:~/artifact_evaluation# python3 disp_bug_table.py ../output/reports/
```

# 5. Experiment 2 (Figure 6): Breakdown of HawkSet's metrics

To generate the graphics seen in Figure 6, run the following command:

```
root@hawkset-exp:~/artifact_evaluation# python3 gen_graphs.py ../output/reports/ ../output/graphs 
```

To view them, you can mount the remote machine via sftp connection, or use scp to copy the files from the remote machine to your local machine.

# 6. Experiment 3 (Table 4): Breakdown of all reports

To generate Table 4, run the following command:

```
root@hawkset-exp:~/artifact_evaluation# python3 disp_irh_comparison.py ../output/reports/
```

Note that the "Manual" Section is not displayed. This is not trivially automated, as discussed in the paper, and as such, does not provide much value to the artifact evaluation.


# 7. Experiment 4 (Table 3): Comparison with PMRace (~40 hours)

To replicate the comparsion betwen PMRace and HawkSet, run the following commands:

**Note**: This experiment takes a long time, arround 40 hours. We suggest using tmux to leave the experiment running the background.

**Note**: If you are running the experiments docker container, exit and return to the host machine.

```
~/HawkSet-exp/artifact_evaluation/$ ./exp_pmrace_comparison.sh
```

When the experiment is completed, run the following command to display the output in a paper-like manner

```
~/HawkSet-exp/artifact_evaluation/$ cd ..
~/HawkSet-exp/$ ./launch.sh hawkset-exp
root@hawkset-exp:~# cd artifact_evaluation
root@hawkset-exp:~/artifact_evaluation# python3 disp_pmrace_comparison.py ffair ../pmrace_results ../output/pmrace_seeds/
```

**Note**: Rerunning this experiment (or the Kick-the-tires (simplified) version ), will delete the previous results
