#!/bin/bash
# For running on the web server system from cron
cd /home/ubuntu/gen-thought
# Set OPENAI_API_KEY and OPENAI_API_ORG
source env.sh
# Generate new thought.html in /var/www/html
/usr/bin/python3 genthought.py /var/www/html > output.txt




