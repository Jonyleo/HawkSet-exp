ARG HAWKSET_VERSION=latest

FROM hawkset:${HAWKSET_VERSION}

RUN apt install pip -y

RUN python3 -m pip install matplotlib

COPY patches ${TOOL_ROOT}/patches
COPY workloads ${TOOL_ROOT}/workloads
COPY runners ${TOOL_ROOT}/runners
COPY config ${TOOL_ROOT}/config
COPY artifact_evaluation ${TOOL_ROOT}/artifact_evaluation

RUN git clone https://github.com/yhuacode/pmrace