### RPM external tensorflow-sources 2.16.0
#FIXME: Set tfversion only for non-tagged TF versions
%define tag         a3f1252d98ab26e1021a90455094edbe496c79b3
%define branch      cms/v2.15-ac5003a
%define github_user cms-externals
%define build_type opt
%define pythonOnly no
%define vectorize_flag -msse3
## INCLUDE tensorflow-sources
