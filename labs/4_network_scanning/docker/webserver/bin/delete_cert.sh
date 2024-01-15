name=$1

docker compose run --rm vpn ovpn_revokeclient "$name" remove