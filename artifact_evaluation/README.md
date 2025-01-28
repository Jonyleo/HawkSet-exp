This document outlines the steps necessary to replicate the experiments present in the paper "HawkSet: Automatic, Application-Agnostic, and Efficient Concurrent PM Bug Detection", submitted to Eurosys 2025.

# Overview

- 1. Requirements and Setup
- 2. Building HawkSet, Workloads and PMRace
- 3. Kick-the-tires Evaluation
- 4. Experiment 1 (Table 2): Detecting Persistency-induced Races
- 5. Experiment 2 (Figure 6): Breakdown of HawkSet's metrics
- 6. Experiment 3 (Table 4): Breakdown of all reports 
- 7. Experiment 4 (Table 3): Comparison with PMRace

# 1. Requirements and Setup


HawkSet was built and tested in Ubuntu 22.04.5 LTS and requires Docker (tested for version 27.5.0), if you are using a provided machine, the environment has been setup already.

Before starting the evaluation:

- Connect to the remote machine provided

TODO

- Clone the repository https://github.com/Jonyleo/HawkSet-exp

```
~/$ git clone https://github.com/Jonyleo/HawkSet-exp 
```

- Initialize submodules

```
~/$ cd HawkSet-exp 
~/HawkSet-exp/$ git submodule update --init
```

# 2. Building HawkSet, Workloads and PMRace

The following command builds every necessary artifact required for the evaluation. See below for time estimations.
If you are running the artifact evaluation on the provided machine, the containers are already built, and you should skip this step.

```
~/$ ./build.sh 
```

Breakdown of building time (assuming a fresh start)

- Building HawkSet (~6 minutes)
- Building the Workloads (~15 minutes)
- Building PMRace (~30 minutes)

# 3. Kick-the-tires Evaluation - Analysing Fast-Fair

To ensure everything is working properly, without waiting for long experiments, follow these steps to perform the analysis for one of the target applications - Fast-Fair.

- Analysing Fast-Fair under HawkSet (~5 minutes)

```
~/HawkSet-exp/$ mkdir output
~/HawkSet-exp/$ cd artifact_evaluation
~/HawkSet-exp/artifact_evaluation/$ ./analyze_application.sh ../output/kickthetires ffair
```

- Displaying the bugs detected in Fast-Fair 

```
~/HawkSet-exp/artifact_evaluation/$ python3 ./disp_bug_table.py ../output/kickthetires
```

- Graphing HawkSet's metrics when evaluating Fast-Fair (memory and time elapsed)

```
~/HawkSet-exp/artifact_evaluation/$ python3 ./gen_graphs.py ../output/kickthetires ../output/graphs
```

Note: If you are using a remote machine provided by us, you can extract the images for vieweing via scp, or mount the machine via sftp.

- Displaying the impact of the Initialization Removal Heuristic

```
~/HawkSet-exp/artifact_evaluation/$ python3 disp_irh_comparison.py ../output/kickthetires
```

- TODO. Kick the tires for PMRace comparison. (This might not be possible)

# 4. Experiment 1 (Table 2): Detecting Persistency-induced Races (~2.5 Hours)

First, analyse all applications under HawkSet (this should take 2.5 hours).

```
~/HawkSet-exp/artifact_evaluation/$ ./analyze_all_applications.sh
```

To output the detected bugs, similarly to Table 2, run the following coomand:

```
~/HawkSet-exp/artifact_evaluation/$ python3 ./disp_bug_table.py ../output/reports/
```

# 5. Experiment 2 (Figure 6): Breakdown of HawkSet's metrics

To generate the graphics seen in Figure 6, run the following command:

```
~/HawkSet-exp/artifact_evaluation/$ python3 ./gen_graphs.py ../output/reports/ ../output/graphs 
```

To view them, you can mount the remote machine via sftp connection, or use scp to copy the files from the remote machine to your local machine.

# 6. Experiment 3 (Table 4): Breakdown of all reports

To generate Table 4, run the following command:

```
~/HawkSet-exp/artifact_evaluation/$ python3 disp_irh_comparison.py ../output/reports/
```

Note that the "Manual" Section is not displayed. This is not trivially automated, as discussed in the paper, and as such, does not provide much value to the artifact evaluation.


# 7. Experiment 4 (Table 3): Comparison with PMRace (~6 hours) [WIP]

To replicate the comparsion betwen PMRace and HawkSet, run the following commands:

Note: This experiment takes a long time, arround 6 hours. We suggest using tmux to leave the experiment running the background. It is already installed in the provided machine.


```
~/HawkSet-exp/artifact_evaluation/$ ./exp_pmrace_comparison.sh
```

When the experiment is completed, run the following command to display the output in a paper-like manner

```
~/HawkSet-exp/artifact_evaluation/$ python3 ./disp_pmrace_comparison.py fast_fair ../pmrace_results/ ../output/pmrace_comparison
```