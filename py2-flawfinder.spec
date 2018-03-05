### RPM external py2-flawfinder 2.0.5
%define PipDownloadOptions --no-deps%%20--no-binary%%3D:none:
%define pip_name flawfinder 

## IMPORT build-with-pip
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/flawfinder
