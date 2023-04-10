#!/bin/bash

if [ "$#" -ne 1 ]; then
    printf 'ERROR! You must provide one and only one argument!\n' >&2
    exit 1
fi

image_file=$1

copyright_owner="Seth Fischer"
current_year=$(date +%Y)
copyright_notice="(c) ${current_year} ${copyright_owner}; Licence: MIT License"
project_url="https://rover.fischer.nz"
description="Final assembly of sethfischer-rover, a quarter-scale Mars rover. See <${project_url}>. Based on NASA-JPL's Perseverance Mars Rover."

exiftool \
    -overwrite_original \
    -Artist="${copyright_owner}" \
    -Copyright="${copyright_notice}" \
    -AttributionName="${copyright_owner}" \
    -AttributionURL="${project_url}" \
    -Comment="Alternative body for the NASA JPL Open Source Rover." \
    -Description="${description}" \
    -License="https://spdx.org/licenses/MIT.html" \
    -Rights="MIT License" \
    -UsageTerms="MIT License" \
    -Software="${project_url}" \
    "$image_file"
