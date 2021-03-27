#!/usr/bin/bash
owd=$(pwd)
source vendor/ini-parser/bash-ini-parser
cfg_parser "phase.ini"
cd PhaseBot

while getopts "shmd:o:" opt; do
   case "$opt" in
      s ) silent=1 ;;
      h ) help=1 ;;
      m ) makedatafod=1 ;;
      d ) datafod=$owd/$OPTARG ;;
      o ) outfile=$owd/$OPTARG ;;
      ? ) help=1 ;;
   esac
done

if [ $silent ] && [ $outfile ]; then
   echo "WARNING: -s and -o are not compatible. Silent operation takes precedent"
fi

if [ $silent ]; then
   outfile=/dev/null
fi

if [ !$datafod ]; then
   cfg_section_"phaseconfig"
   datafod=$datafolder
fi

if [ $help ]; then
   echo
   echo "Usage: $0 [options]"
   echo
   echo "-s         Silence the operation of the bot"
   echo "-m         Create the required data folder & files, overrides existing files"
   echo "-d folder  Set a custom data folder for the bot, does not override the setting in phase.ini"
   echo "-o file    Set a logfile for the bot"
   echo "-h         Show this menu"
   exit
fi

if [ $makedatafod ]; then
   mkdir $datafod
   echo "" > $datafod/starred.txt
   echo "{\"default\":{}}" > $datafod/userdata.json
   echo "Please enter your bot token"
   read token
   echo $token > $datafod/token
fi

if [ $outfile ]; then
   python3 bot.py $datafod > $outfile 2> $outfile
else
   python3 bot.py $datafod
fi
