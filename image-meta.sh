#!/bin/bash

if [ "$#" -ne 1 ]; then
    printf 'ERROR! You must provide one and only one argument!\n' >&2
    exit 1
fi

image_file=$1

copyright_owner="Seth Fischer"
today=$(date +%Y-%m-%d)
current_year=$(date +%Y)
licence="MIT License"
licence_url="https://spdx.org/licenses/MIT.html"
copyright_notice="(c) ${current_year} ${copyright_owner}; Licence: ${licence}"
project_url="https://rover.fischer.nz"
description="Final assembly of sethfischer-rover, a quarter-scale Mars rover. See <${project_url}>. Based on NASA-JPL's Perseverance Mars Rover."

exiftool \
    -overwrite_original \
    -AttributionName="${copyright_owner}" \
    -AttributionURL="${project_url}" \
    -Comment="${description}" \
    -License="${licence_url}" \
    -MWG:Copyright="${copyright_notice}" \
    -MWG:CreateDate="${today}" \
    -MWG:Creator="${copyright_owner}" \
    -MWG:DateTimeOriginal="${today}" \
    -MWG:Description="${description}" \
    -Software="${project_url}" \
    -UsageTerms="${licence}" \
    "$image_file"
