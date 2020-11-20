### RPM external tensorflow-sources 2.3.1
%define python_cmd python
%define python_env PYTHON27PATH
%define build_type opt
%define pythonOnly no
%define vectorize_flag -msse3
Requires: py2-futures
## INCLUDE tensorflow-sources

