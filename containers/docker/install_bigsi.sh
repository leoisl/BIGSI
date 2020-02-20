#!/usr/bin/env bash
cd /
git clone https://github.com/leoisl/BIGSI
cd BIGSI
git checkout adding_search_several
pip3 install -r requirements.txt
pip3 install -r optional-requirements.txt
pip3 install .
