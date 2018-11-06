### RPM external py2-notebook 5.6.0
## IMPORT build-with-pip

BuildRequires: py2-backports-shutil_get_terminal_size py2-configparser
Requires: py2-terminado py2-nbconvert py2-ipykernel py2-Send2Trash py2-ipaddress py2-prometheus_client
%define PipPostBuild \
   perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
