#!/usr/bin/sh

while true
do
    /usr/bin/expect /usr/local/automation/telnet.expect "172.16.10.4" "alice" "{flag3-Sw0rdf1sh}"
    sleep 5
    curl https://www.google.com > /dev/null
    sleep 5
    curl https://www.colorado.edu > /dev/null
    sleep 5
done    