ARG HAWKSET_VERSION
FROM hawkset-exp-${HAWKSET_VERSION}

RUN apt update
RUN apt install -y autoconf automake build-essential cmake \
    libnuma-dev libtbb-dev 

WORKDIR $TOOL_ROOT
RUN git clone https://github.com/baotonglu/apex

##### FAST_FAIR
WORKDIR $TOOL_ROOT/apex

# Apply patch
RUN git apply $TOOL_ROOT/patches/apex.diff
# Compile
RUN ./build.sh debug
