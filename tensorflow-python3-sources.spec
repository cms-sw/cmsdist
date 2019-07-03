### RPM external tensorflow-python3-sources 1.13.1
%define python_cmd python3
%define python_env PYTHON3PATH
%define build_type opt
%define pythonOnly yes
#Just to make sure that only one tensorflow-source package built at a time
BuildRequires: tensorflow-sources
## INCLUDE tensorflow-sources
