#!/bin/bash
sudo service docserve stop
pip uninstall -y docserve
pip install docserv*.whl
sudo service docserve start
sudo service docserve status


