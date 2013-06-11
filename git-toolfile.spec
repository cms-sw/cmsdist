### RPM external git-toolfile 1.0
Requires: git
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/git.xml
<tool name="git" version="@TOOL_VERSION@">
  <info url="http://git-scm.com"/>
  <client>
    <environment name="GIT_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PATH" value="$GIT_BASE/bin" type="path"/>
  <runtime name="PATH" value="$GIT_BASE/libexec/git-core" type="path"/>
  <runtime name="GIT_TEMPLATE_DIR" value="$GIT_BASE/share/git-core/templates" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
