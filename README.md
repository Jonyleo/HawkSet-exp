# HawkSet Artifact Evaluation

This document describes the content of this repo, which contains all materials need to build and execute all experiments in the paper "HawkSet: Automatic, Application-Agnostic, and Efficient Concurrent PM Bug Detection", submitted to Eurosys 2025.

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

**Navigate to artifact_evaluation/README.md for "kick-the-tires" steps, and the full evaluation**

# applications

Each application tested by HawkSet is packaged as a Docker container for ease of use.
All containers inherit from the main HawkSet container.

# config

As stated in the paper, applications which do not employ standard synchronization primitives (such as pthread or libpmemobj's mutexes), require a configuration file with information regarding each primitive.

# patches

As described in the paper, some application require modification to their source code for analysis, when the synchronization primitives cannot be easily abstracted from the rest of the code.
Furthermore, to normalize the evaluation between all applications, we implemented a YCSB parser that maps each operation to the application under test. 

# runners

Each application requires slightly different parameters to execute, the runner scripts abstract that process away, and are used in the experiments.

# HawkSet

See HawkSet/README.md for further discussion of HawkSet's source code

# pmrace-vagrant

See "Efficiently detecting concurrency bugs in persistent memory programs" for further details regarding PMRace
