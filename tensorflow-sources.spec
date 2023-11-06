### RPM external tensorflow-sources 2.15.0
#FIXME: Set tfversion only for non-tagged TF versions
%define tag         62ea0e481ee95c0c24ca2702afceb935f48c6d30
%define branch      cms/v%{realversion}-rc1
%define github_user cms-externals
%define build_type opt
%define pythonOnly no
%define vectorize_flag -msse3
## INCLUDE tensorflow-sources
