### RPM external py2-flawfinder 2.0.6
## IMPORT build-with-pip

%define PipDownloadOptions --no-binary%%3D:none:
%define pip_name flawfinder
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/flawfinder
