### RPM external py2-markdown 3.1.1
## IMPORT build-with-pip

%define pip_name Markdown

perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
