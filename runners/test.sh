#!/bin/bash

make -C ../examples
make -C ${TOOL_ROOT}/src obj-intel64/test.so 

PMEM_IS_PMEM_FORCE=1 \
${PIN_ROOT}/pin -t ../src/obj-intel64/test.so \
	-pm-mount ${PM_MOUNT} \
	-- $1
