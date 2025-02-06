This document describes the content of this repo, which contains all materials need to build and execute all experiments in the paper "HawkSet: Automatic, Application-Agnostic, and Efficient Concurrent PM Bug Detection", submitted to Eurosys 2025.

# Overview

HawkSet-exp/ - Root folder 
HawkSet-exp/applications/ - Docker instances for each applications under test
HawkSet-exp/artifact_evaluation/ - Scripts and guide for the artifact_evaluation
HawkSet-exp/config/ - Configuration files for the synchronization primitives
HawkSet-exp/HawkSet/ - HawkSet source code submodule
HawkSet-exp/patches/ - Patch files for some applications
HawkSet-exp/pmrace-vagrant/ - PMRace source code and evaluation submodule
HawkSet-exp/runners/ - Helper scripts to analyze each application
HawkSet-exp/build_hawkset.sh - Builds HawkSet and evaluation requirements
HawkSet-exp/build_pmrace.sh - Builds PMRace
HawkSet-exp/config.sh - Contains environment variables used in other scripts
HawkSet-exp/launch.sh - Launches a specific application container

**Navigate to HawkSet-exp/artifact_evaluation/README.md for "kick-the-tires" steps, and a the full evaluation**

# HawkSet-exp/applications/

Each application tested by HawkSet is packaged as a Docker container for ease of use.
All containers inherit from the main HawkSet container.

# HawkSet-exp/config/

As stated in the paper, applications which do not employ standard synchronization primitives (such as pthread or libpmemobj's mutexes), require a configuration file with information regarding each primitive.

**HawkSet-exp/config/pthread.cfg can be used as a template to create other configuration files**

# HawkSet-exp/HawkSet/

See HawkSet-exp/HawkSet/README.md for further discussion of HawkSet's source code

# HawkSet-exp/patches/

As described in the paper, some application require modification to their source code for analysis, when the synchronization primitives cannot be easily abstracted from the rest of the code.
Furthermore, to normalize the evaluation between all applications, we had to implemented a YCSB parser that calls each operation in the application under test. 

# HawkSet-exp/runners/

Each application requires slightly different parameters to execute, the runner scripts abstract that process away, and are used in the experiments.
