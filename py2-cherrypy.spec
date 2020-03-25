### RPM external py2-cherrypy 17.4.0
## IMPORT build-with-pip
Requires: py2-six py2-cheroot py2-portend py2-more-itertools py2-zc-lockfile py2-contextlib2

%define pip_name CherryPy
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/cherryd
