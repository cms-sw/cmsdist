### RPM external py2-nbconvert 5.4.0
## IMPORT build-with-pip

Requires: py2-nbformat py2-Jinja2 py2-Pygments py2-bleach py2-backports py2-defusedxml py2-entrypoints py2-mistune py2-pandocfilters py2-testpath
%define PipPostBuild \
   perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/jupyter-nbconvert
