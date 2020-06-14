### RPM external py3-nose 1.3.7
## IMPORT build-with-pip3

%define PipPostBuild \
   perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/nosetests %{i}/bin/nosetests-2.7

