#!/bin/sh
URL="http://127.0.0.1:8000/api/usage"

md5()
{
    echo $(echo -n ${1} | md5sum | awk '{print $1}')
}

pair()
{
    echo "\"${1}\":\"${2}\""
}

mantid_info()
{
    if [ "${1}" == "3.2.20141211.1338" ]; then
        vers=$(pair  "mantidVersion" "${1}")
        sha1=$(pair  "mantidSha1"    "a71f37d91884ba4658a1c64a6e84c427272bdcdd")
        pvver=$(pair "ParaView"      "3.98.1")
    elif [ "${1}" == "3.2.20141220.304" ]; then
        vers=$(pair  "mantidVersion" "3.2.20141220.304")
        sha1=$(pair  "mantidSha1"    "b332d1f20ca967bbe14c04b28b01a9c67ef26781")
        pvver=$(pair "ParaView"      "0")
    else
        echo "unknown mantid version: ${1}"
        exit 1
    fi
    echo "${vers},${sha1},${pvver}"
}

host_info()
{
    if [ "${1}" == "molly.sns.gov" ]; then
        host=$(pair "host"      $(md5 "molly.sns.gov"))
        arch=$(pair  "osArch"   "x86_64")
        vers=$(pair "osVersion" "3.17.4-200.fc20.x86_64")
        name=$(pair "osName"    "Linux")
    elif [ "${1}" == "9b783e26451eb0db0e80803aea2fbec9" ]; then
        host=$(pair  "host"     "9b783e26451eb0db0e80803aea2fbec9")
        arch=$(pair  "osArch"   "x86_64")
        vers=$(pair "osVersion" "13.4.0")
        name=$(pair "osName"    "Darwin")
    else
        echo "unknown host: ${1}"
        exit 1
    fi
    echo "${host},${arch},${vers},${name}"
}

send()
{
    echo ${1} 
    curl -H "Content-Type: application/json" \
    ${URL} -d ${1}
    echo
    echo
}

# add a unix machine
user=$(pair "uid"            $(md5 "pf9"))
when=$(pair  "dateTime"      "2014-12-11T19:46:40.264Z")
mantid=$(mantid_info "3.2.20141211.1338")
host=$(host_info "molly.sns.gov")
#send "{${user},${when},${mantid},${host}}"

# add it again with now for the date/time
when=$(pair  "dateTime"      $(date -u --iso-8601=seconds | sed s/+0000/Z/))
send "{${user},${when},${mantid},${host}}"

# add a mac
user=$(pair  "uid"           "3adfa2240926ac9d2e674abb93a3759c")
when=$(pair  "dateTime"      "2014-12-23T20:29:41.134Z")
mantid=$(mantid_info "3.2.20141220.304")
host=$(host_info "9b783e26451eb0db0e80803aea2fbec9")
#send "{${user},${when},${mantid},${host}}"

# add it again with now for the date/time
when=$(pair  "dateTime"      $(date -u --iso-8601=seconds | sed s/+0000/Z/))
send "{${user},${when},${mantid},${host}}"
