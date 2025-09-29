#! /usr/bin/env bash

CURDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/"

curl -L -o reuter50_50.zip "https://archive.ics.uci.edu/static/public/217/reuter+50+50.zip"
unzip reuter50_50.zip 