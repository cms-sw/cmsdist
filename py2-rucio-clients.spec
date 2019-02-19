### RPM external py2-rucio-clients 1.18.8.post1
## IMPORT build-with-pip
Requires: py2-argcomplete py2-requests py2-urllib3 py2-dogpile-cache py2-nose py2-boto
Requires: py2-tabulate py2-progressbar2 py2-bz2file py2-python-magic py2-six py2-futures

%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
