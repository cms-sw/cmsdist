### RPM external py2-virtualenv-clone 0.4.0
## IMPORT build-with-pip

%define PipDownloadSourceType none
%define DownloadOptionsExtra pkg_filename=virtualenv_clone
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
