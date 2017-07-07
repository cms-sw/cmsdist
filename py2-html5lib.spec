### RPM external py2-html5lib 0.999999999
## INITENV +PATH PYTHONPATH %{i}/${PYTHON_LIB_SITE_PACKAGES}

%define pip_name html5lib
Requires: py2-ordereddict py2-six py2-packaging py2-setuptools py2-webencodings py2-pyparsing py2-appdirs 

## IMPORT build-with-pip

