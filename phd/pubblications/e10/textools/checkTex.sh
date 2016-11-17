#!/bin/bash
for tex in "$@"
do
	echo ""
	echo "==============================================="
	echo "============== ${tex}:"
	echo "WEASEL WORDS: "
	sh textools/find_weasels.sh $tex
	
	echo ""
	echo "PASSIVE VOICE: "
	sh textools/find_passive_voice.sh $tex
	
	echo ""
	echo "DUPLICATES: "
	perl textools/find_doubles.pl $tex
done
