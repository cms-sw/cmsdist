### RPM external py2-html5lib 0.9999999
## INITENV +PATH PYTHONPATH %{i}/$PYTHON_LIB_SITE_PACKAGES

#bleach can not currently use anything newer than 0.9999999 (7 9s)

%define pip_name html5lib
Requires: py2-ordereddict py2-six py2-packaging py2-setuptools py2-webencodings py2-pyparsing py2-appdirs 

## IMPORT build-with-pip

