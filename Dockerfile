ARG HAWKSET_VERSION=latest

FROM hawkset:${HAWKSET_VERSION}
COPY patches ${TOOL_ROOT}/patches


