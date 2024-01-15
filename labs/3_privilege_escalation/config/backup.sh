#!/bin/bash

####################################
# Admin backup script, do not touch!
####################################

# Back up all of our user's important files
tar -zcvpf /root/backups/backup.tar.gz /home