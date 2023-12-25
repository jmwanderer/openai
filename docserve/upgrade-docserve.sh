#!/bin/bash

# Script for upgrading pip based installs.

sudo service docserve stop
pip uninstall -y docserve
pip install docserv*.whl
sudo service docserve start
sudo service docserve status


