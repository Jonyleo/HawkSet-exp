#!/usr/bin/bash

if [ -z $WORKLOAD  ] ; then
	WORKLOAD=100
fi

PM_FILE=${PM_MOUNT}pmemcached
rm ${PM_MOUNT}/pmemcached -f

rm /tmp/m_sock -f

${TOOL_ROOT}/scripts/HawkSet \
 	${@:1} \
  	-- \
	memcached \
	-A \
	-t 8 \
	-o pslab_force,pslab_file=${PM_FILE},pslab_policy=pmem \
	-u root \
	-p 1234 \
	-s /tmp/m_sock &

until [ -e /tmp/m_sock ] ; do
	sleep 1
done

echo Starting

python3 pmemcached_client.py /tmp/m_sock 8 $WORKLOAD --zipf


