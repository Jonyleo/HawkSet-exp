#!/usr/bin/bash

if [ -z $WORKLOAD  ] ; then
	WORKLOAD=100
fi

rm ${PM_MOUNT}/cclbtree -rf
mkdir ${PM_MOUNT}/cclbtree -p

#${TOOL_ROOT}/scripts/HawkSet \
#	${@:1} \
#	-- \
gdb --args	./../CCL-BTree/mybin/m_normal_test_cclbtree_lb \
	-t 8 \
	-p ${PM_MOUNT}/cclbtree \
	-i ${TOOL_ROOT}/workloads/ycsb_$WORKLOAD.txt
