### RPM external tensorflow-sources 2.12.0
%define tag         75e38ccee85313ae89c01c4810e8188a27020efb
%define branch      cms/v%{realversion}
%define github_user cms-externals
%define python_cmd python3
%define python_env PYTHON3PATH
%define build_type opt
%define pythonOnly no
%define vectorize_flag -msse3
## INCLUDE tensorflow-sources
