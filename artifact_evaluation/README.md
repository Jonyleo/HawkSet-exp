This document outlines the steps necessary to replicate the experiments present in the paper "HawkSet: Automatic, Application-Agnostic, and Efficient Concurrent PM Bug Detection", submitted to Eurosys 2025.

# Overview

- Experiment 1 (Table 2): Detecting Persistency-induced Races
- Experiment 2 (Figure 6): Breakdown of HawkSet's metrics
- Experiment 3 (Table 4): Breakdown of all reports 
- Experiment 4 (Table 3): Comparison with PMRace

# Experiment 1 (Table 2): Detecting Persistency-induced Races (~2.5 Hours)

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

# Experiment 2 (Figure 6): Breakdown of HawkSet's metrics

To generate the graphics seen in Figure 6, run the following command:

```
root@hawkset-exp:~/artifact_evaluation# python3 gen_graphs.py ../output/reports/ ../output/graphs 
```

To view them, you can mount the remote machine via sftp connection, or use scp to copy the files from the remote machine to your local machine.

# Experiment 3 (Table 4): Breakdown of all reports

To generate Table 4, run the following command:

```
root@hawkset-exp:~/artifact_evaluation# python3 disp_irh_comparison.py ../output/reports/
```

Note that the "Manual" Section is not displayed. This is not trivially automated, as discussed in the paper, and as such, does not provide much value to the artifact evaluation.


# Experiment 4 (Table 3): Comparison with PMRace (~40 hours)

To replicate the comparsion betwen PMRace and HawkSet, run the following commands:

*Notes* 
- This experiment takes a long time, arround 40 hours. We suggest using tmux to leave the experiment running the background.
- Rerunning this experiment (or the Kick-the-tires version), will delete the previous results

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

