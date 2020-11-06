### RPM external py3-fixtures 3.0.0
## IMPORT build-with-pip3

%define patchsrc sed -i -e 's|^testtools.*||' requirements.txt
Requires: py3-pbr py3-six
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
