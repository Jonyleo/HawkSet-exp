FEATURE_FLAGS=$(awk -F': ' '/flags/{gsub(" ", "\n", $2);print $2;exit}' /proc/cpuinfo)

contains() {
    [[ $1 =~ (^|[[:space:]])$2($|[[:space:]]) ]] && return 0 || return 1
}

SUITABLE=0

for FLAG in avx512vl avx512bw clwb clflushopt clflush sse ; do
	if contains "$FEATURE_FLAGS" $FLAG ; then
		continue
	else
		echo Missing CPU feature flag \"$FLAG\". 
		SUITABLE=1
	fi
done


if [[ `nproc` -lt 16 ]] ; then 
	echo Missing minimum required number of CPUs \(16\)
fi

MEM_TOTAL=`awk '/MemTotal/ {print $2}' /proc/meminfo`
MEM_REQ=`expr 32 \* 1024 \* 1024`

if [[ $MEM_TOTAL -lt $MEM_REQ ]] ; then
	echo Missing minimum required RAM \(32G\)
fi

STORAGE_TOTAL=`df -P . | tail -1 | awk '{print $4}'`
STORAGE_REQ=`expr 100 \* 1024 \* 1024`

echo $STORAGE_TOTAL $STORAGE_REQ

if [[ $STORAGE_TOTAL -lt $STORAGE_REQ ]] ; then
	echo Missing minimum required storage space \(100G\)
fi

if [[ $SUITABLE -eq 1 ]] ; then
	echo Your machine is not suitable for this evaluation. 
	exit
fi

echo Installing Vagrant (Requires sudo)

wget -O - https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install vagrant


echo Installing virtualbox

sudo apt install virtualbox
