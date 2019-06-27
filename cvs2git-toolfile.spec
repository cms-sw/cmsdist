### RPM external cvs2git-toolfile 1.0
Requires: cvs2git 
%prep
%build
%install
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/cvs2git.xml
<tool name="cvs2git" version="@TOOL_VERSION@">
  <client>
    <environment name="CVS2GIT_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PATH" value="$CVS2GIT_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
