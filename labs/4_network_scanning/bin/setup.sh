# These are the steps taken to initialize the OpenVPN volume. It is not necessary to re-run them.
# docker compose run --rm vpn ovpn_genconfig -u udp://midterm.csci3403.com
docker compose run --rm vpn ovpn_initpki