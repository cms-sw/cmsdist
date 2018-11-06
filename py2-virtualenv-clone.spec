### RPM external py2-virtualenv-clone 0.4.0
## IMPORT build-with-pip

%define PipDownloadOptions --no-binary%%3D:none:
%define DownloadOptionsExtra pkg_filename=virtualenv_clone
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
