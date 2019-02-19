### RPM external py2-scipy 1.1.0
## IMPORT build-with-pip

Requires: py2-numpy
%define PipPostBuild \
perl -p -i -e "s|^#!.*python(.*)|#!/usr/bin/env python$1|" `grep -r -e "#\!.*python" %i | cut -d: -f1`
