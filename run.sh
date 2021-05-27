#!/usr/bin/env bash
cd "$(dirname "$(realpath "$0")")"
source ./venv/bin/activate
./circles.py $*
