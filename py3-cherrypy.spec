### RPM external py3-cherrypy 17.4.0
## IMPORT build-with-pip3
Requires: py3-six py3-cheroot py3-portend py3-more-itertools py3-zc-lockfile py3-contextlib2

%define pip_name CherryPy
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/cherryd
