#!/bin/bash
dir=$(dirname $0)
if [ -e "${dir}/$1.spec" ] ; then
  cat "${dir}/$1.spec"
  exit 0
fi

echo "### RPM cms $1 $2"
if [ -f "${dir}/$1.file" ] ; then
  cat "${dir}/$1.file"
else
  case $3 in
    data-build-github)
      echo ""
      echo "%prep"
      echo ""
      ;;
  esac
fi
echo "## IMPORT $3"

case $1 in 
  data-CalibTracker-SiStripDCS|data-SLHCUpgradeSimulations-Geometry|data-GeneratorInterface-ReggeGribovPartonMCInterface) echo "";;
esac

