### RPM external py2-memory-profiler 0.55.0
## IMPORT build-with-pip

Requires: py2-psutil
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/* 
