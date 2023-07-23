#!/bin/bash

# ans="\$1"

# for i in {2..12}
# do
#     ans="$ans, \$$i"
# done

# # print DIMM0 info
# echo "sudo pmwatch 1 -td | awk '{print $ans}'"
# sudo pmwatch 1 -td | awk '{print $ans}'

sudo pmwatch 1 -td | awk '{print $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12}'