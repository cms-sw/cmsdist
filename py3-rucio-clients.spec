### RPM external py3-rucio-clients 1.22.2
## IMPORT build-with-pip3
## INITENV SET RUCIO_HOME %i/

Source1: rucio-config
Requires: py3-argcomplete py3-requests py3-urllib3 py3-dogpile-cache py3-nose py3-boto
Requires: py3-tabulate py3-progressbar2 py3-bz2file py3-python-magic py3-six 
Requires: py3-boto3 py3-pysftp

# setup a CMS rucio configuration standard file
%define PipPreBuild mkdir -p %i/etc/; cp -f %_sourcedir/rucio-config %i/etc/rucio.cfg

%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
