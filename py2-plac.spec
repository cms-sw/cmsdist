### RPM external py2-plac 1.0.0
## IMPORT build-with-pip

%define PipPostBuild \
  perl -p -i -e "s|^#!.*python(.*)|#!/usr/bin/env python$1|" `grep -r -e "^#\!.*python.*" %i | cut -d: -f1`
