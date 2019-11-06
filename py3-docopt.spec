### RPM external py3-docopt 0.6.2
## IMPORT build-with-pip3

%define pip_name docopt
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/cherryd
