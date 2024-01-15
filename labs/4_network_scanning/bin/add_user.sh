username="$1"
docker compose exec vpn easyrsa build-client-full "$username" nopass
docker compose exec vpn ovpn_getclient "$username" > "$username".ovpn