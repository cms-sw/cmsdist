### RPM external py3-memory-profiler 0.57.0
## IMPORT build-with-pip3

Requires: py3-psutil
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/* 
