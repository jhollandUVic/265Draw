#!/bin/bash

if [[ $# -ne 3 ]]; then
	echo "$0: usage: sierpinski recursions patterns colour-theme"
	exit 1
fi

re='^[0-9]+$'

if ! [[ $1 =~ $re ]] ; then
	echo "$0: usage: sierpinski recursions '$1' not numeric"
	exit 1
fi

if [[ $1 -lt 0 || $1 -gt 4 ]] ; then
	echo "$0: usage: sierpinski recursions '$1' out of range 0 to 4"
	exit 1
fi

recursions=$1

if [[ $2 == carpet ]] ; then
	pattern=$2
elif [[ $2 == cross ]] ; then
	pattern=$2
elif [[ $2 == diagonal ]] ; then
	pattern=$2
elif [[ $2 == rotate ]] ; then
	pattern=$2
else 
	echo "$0: usage: sierpinski pattern '$2' not valid"
	exit 1
fi

if [[ $3 == primary ]] ; then
	col_theme=$3
elif [[ $3 == secondary ]] ; then
	col_theme=$3
elif [[ $3 == bold ]] ; then
	col_theme=$3
elif [[ $3 == tropical ]] ; then
	col_theme=$3
else 
	echo "$0: usage: sierpinski colour theme '$3' not valid"
	exit 1
fi

scale_to_a_third=.3333

echo	"*"
echo	"* Create a Recursive Sierpinski carpet line file with ${recursions} Levels"
CMD="python generate_carpet.py ${recursions} ${col_theme} > carpet_${recursions}.txt"
echo "${CMD}"
eval "${CMD}"
rc=$?; if [[ $rc != 0 ]]; then exit $rc; fi
echo	"*"
echo	"* Create colour svg file from base carpet line file"
CMD="python lines_to_svg_colour.py < carpet_${recursions}.txt > carpet_${recursions}.svg"
echo "${CMD}"
eval "${CMD}"
rc=$?; if [[ $rc != 0 ]]; then exit $rc; fi
echo	"*"
echo	"* Scale carpet line file down to fit in central ninth of canvas"
CMD="python rotate_scale_translate.py -f ${scale_to_a_third} < carpet_${recursions}.txt > carpet_${recursions}S.txt"
echo "${CMD}"
eval "${CMD}"
rc=$?; if [[ $rc != 0 ]]; then exit $rc; fi
echo	"*"
echo	"* Build tile patterns from scaled line file"
CMD="python transform_carpet.py ${pattern} < carpet_${recursions}S.txt > carpet_${recursions}ST.txt"
echo "${CMD}"
eval "${CMD}"
rc=$?; if [[ $rc != 0 ]]; then exit $rc; fi
echo	"*"
echo "* Create colour svg file from tiled carpet line file"
CMD="python lines_to_svg_colour.py < carpet_${recursions}ST.txt > carpet_${recursions}ST.svg"
echo "${CMD}"
eval "${CMD}"
rc=$?; if [[ $rc != 0 ]]; then exit $rc; fi
echo	"*"
echo "* Display information about files produced"
CMD="ls -Farlt carpet_${recursions}*.svg"
echo "${CMD}"
eval "${CMD}"
rc=$?; if [[ $rc != 0 ]]; then exit $rc; fi
exit 0
