### RPM external py2-nbdime 1.0.2
## IMPORT build-with-pip

BuildRequires: py2-backports-shutil_get_terminal_size py2-configparser py2-backports-functools_lru_cache py2-backports-shutil_which
Requires: py2-notebook py2-GitPython py2-requests py2-colorama py2-backports
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*


