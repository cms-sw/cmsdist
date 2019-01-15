### RPM external py2-nose 1.3.7
## IMPORT build-with-pip

%define PipPostBuild \
   perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/nosetests %{i}/bin/nosetests-2.7

