This document outlines the steps necessary to replicate the experiments present in the paper "HawkSet: Automatic, Application-Agnostic, and Efficient Concurrent PM Bug Detection", submitted to Eurosys 2025.

# Notes: TODO


# Overview

- 0. Requirements and Setup
- 1. Building HawkSet
- 2. Building Workloads
- 3. Experiment 1 (Table 2): Detecting Persistency-induced Races
- 4. Experiment 2 (Table 3): Comparison with PMRace
- 5. Experiment 3 (Table 4): Breakdown of all reports 

# 0. Requirements and Setup

HawkSet was built and tested in Ubuntu 22.04.5 LTS and requires the following:

- Docker (tested for version 27.5.0)

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
TODO, make HawkSet repo public, fix this	

# 1. Building HawkSet

HawkSet is packaged in a docker container for ease of use, to build it run the ```build.sh``` script in the root folder of this repository.

# 2. Build Workloads

Each workload is packaged in a docker container, which builds upon the base HawkSet container, to build them run the following commands:

```
~/HawkSet-exp/$ cd applications
~/HawkSet-exp/applications/$ ./full_build.sh
```