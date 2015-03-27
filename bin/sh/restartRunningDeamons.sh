#!/bin/bash


cd /tmp
wget localhost?l=restartRunningDeamons

# HOUSKEEPING
find /var/www/logs/*.log -type f -mtime +2 -exec rm {} \;
