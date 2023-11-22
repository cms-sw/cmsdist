### RPM external tensorflow-sources 2.15.0
#FIXME: Set tfversion only for non-tagged TF versions
%define tag         9be80c88ecdd559940e6467fb780369e4740c8e4
%define branch      cms/v%{realversion}
%define github_user cms-externals
%define build_type opt
%define pythonOnly no
%define vectorize_flag -msse3
## INCLUDE tensorflow-sources
