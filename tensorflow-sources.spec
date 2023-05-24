### RPM external tensorflow-sources 2.12.0
%define tag         bb361a0a183d45222d8ff7dbf4a04c44c0e094bd
%define branch      cms/v%{realversion}
%define github_user cms-externals
%define python_cmd python3
%define python_env PYTHON3PATH
%define build_type opt
%define pythonOnly no
%define vectorize_flag -msse3
## INCLUDE tensorflow-sources
