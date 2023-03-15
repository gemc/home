#!/bin/bash


eclist=/opt/projects/gemc/home/_data/gemcEC.yml
dirstToCheck=(/opt/projects/gemc/glibrary /opt/projects/gemc/src)

rm -f $eclist ; touch $eclist

declare -a exitCodes

for dirToCheck in ${dirstToCheck[@]}
do
	echo Checking $dirToCheck
	cd $dirToCheck

	ecodes1=$(grep "#define EC__" */*         2>/dev/null | awk -F"define" '{print $2}' | awk '{print $1"="$2}' | awk -F"EC__" '{print $2}')
	ecodes2=$(grep "#define EC__" */*/*       2>/dev/null | awk -F"define" '{print $2}' | awk '{print $1"="$2}' | awk -F"EC__" '{print $2}')
	ecodes3=$(grep "#define EC__" */*/*/*     2>/dev/null | awk -F"define" '{print $2}' | awk '{print $1"="$2}' | awk -F"EC__" '{print $2}')
	ecodes4=$(grep "#define EC__" */*/*/*/*   2>/dev/null | awk -F"define" '{print $2}' | awk '{print $1"="$2}' | awk -F"EC__" '{print $2}')
	ecodes5=$(grep "#define EC__" */*/*/*/*/* 2>/dev/null | awk -F"define" '{print $2}' | awk '{print $1"="$2}' | awk -F"EC__" '{print $2}')

	for code in $ecodes1 $ecodes2 $ecodes3 $ecodes4 $ecodes5
	do
		codeName="$(echo $code  | awk -F"=" '{print $1}' )"
		codeValue="$(echo $code | awk -F"=" '{print $2}' )"
		exitCodes[$codeValue]=$codeName
	done
done

for elem in "${!exitCodes[@]}"
do
	echo "exit code : ${elem}" -- "error: ${exitCodes[${elem}]}"
	echo "- name: "${exitCodes[${elem}]}  >> $eclist
	echo "  code: "${elem}                >> $eclist
done


