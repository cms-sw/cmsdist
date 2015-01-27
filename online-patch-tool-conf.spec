### RPM cms online-patch-tool-conf 2.0
# with cmsBuild, change the above version only when a new
# tool is added
## INITENV SET CMSSW_PATCH_TOOL_CONF_ROOT $ONLINE_PATCH_TOOL_CONF_ROOT
%define onlinesystemtoolsroot ${ONLINESYSTEMTOOLS_ROOT}

Requires: online-toolfile

# still need this (from the non-patch tool-conf spec ...
%define skipreqtools jcompiler

## IMPORT scramv1-tool-conf
