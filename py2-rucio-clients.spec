### RPM external py2-rucio-clients 1.20.5
## IMPORT build-with-pip
## INITENV SET RUCIO_HOME %i/

Source1: rucio-config
Requires: py2-argcomplete py2-requests py2-urllib3 py2-dogpile-cache py2-nose py2-boto
Requires: py2-tabulate py2-progressbar2 py2-bz2file py2-python-magic py2-six py2-futures
Requires: py2-boto3 py2-pysftp

# setup a CMS rucio configuration standard file
%define PipPreBuild mkdir -p %i/etc/; cp -f %_sourcedir/rucio-config %i/etc/rucio.cfg

%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
