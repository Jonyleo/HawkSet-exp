ARG HAWKSET_VERSION=latest
FROM hawkset-exp:${HAWKSET_VERSION}

RUN apt update
RUN apt install -y autoconf automake build-essential cmake \
    libnuma-dev libtbb-dev 

RUN python3 -m pip install gdown

# Download required load
RUN gdown https://drive.google.com/uc?id=1Q89-v4FJLEwIKL3YY3oCeOEs0VUuv5bD

WORKDIR $TOOL_ROOT
RUN git clone https://github.com/baotonglu/apex

##### FAST_FAIR
WORKDIR $TOOL_ROOT/apex

# Apply patch
RUN git apply $TOOL_ROOT/patches/apex.diff
# Compile
RUN ./build.sh debug
