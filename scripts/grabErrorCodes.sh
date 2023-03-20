#!/bin/zsh


eclist=/opt/projects/gemc/home/_data/gemcEC.yml
dirstToCheck=(/opt/projects/gemc/glibrary /opt/projects/gemc/src)

rm -f $eclist ; touch $eclist

declare -a exitCodes

for dirToCheck in ${dirstToCheck[@]}
do
	echo Checking $dirToCheck
	cd $dirToCheck

	ecodes=$(grep -r "#define EC__" */* 2>/dev/null | awk -F"define" '{print $2}' | awk '{print $1"="$2}' | awk -F"EC__" '{print $2}' | sort -u)

	for code in $=ecodes
	do
		codeName="$(echo $code  | awk -F"=" '{print $1}' )"
		codeValue="$(echo $code | awk -F"=" '{print $2}' )"
		echo "exit code : ${codeValue}" -- "error: ${codeName}"
		exitCodes[$codeValue]="$codeName"
	    echo "- name:  ${codeName}"  >> $eclist
	    echo "  code:  ${codeValue}" >> $eclist
	done
done

