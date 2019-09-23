#!/bin/bash
dir=$(dirname $0)
if [ -e "${dir}/$1.spec" ] ; then
  cat "${dir}/$1.spec"
else
  echo "### RPM external $1 $2"
  echo "## IMPORT build-with-pip"
  if [ "$3" = "py2" ] ; then
    echo "%define doPython3 no"
  elif [ "$3" == "py3" ] ; then
    echo "%define doPython2 no"
  fi
  subdir=$(basename $dir)
  pycommon=$(echo $1 | sed 's|^py[2-9]-||')
  if [ -f "${dir}/${pycommon}.file" ] ; then
    echo "## INCLUDE ${subdir}/${pycommon}"
  fi
  if [ -f "${dir}/$1.file" ] ; then
    echo "## INCLUDE ${subdir}/${1}"
  fi
fi
