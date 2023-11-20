### RPM external tensorflow-sources 2.15.0
#FIXME: Set tfversion only for non-tagged TF versions
%define tag         b47a1dc0032b63c98d63d5b5b78e9a9942e8d379
%define branch      cms/v%{realversion}
%define github_user cms-externals
%define build_type opt
%define pythonOnly no
%define vectorize_flag -msse3
## INCLUDE tensorflow-sources
