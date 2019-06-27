### RPM external git-toolfile 1.0
Requires: git
%prep

%build

%install

case "%{cmsplatf}" in
  *)
    PERL5LIB_PATH=/share/perl5
    ;;
  osx*)
    PERL5LIB_PATH=/lib/perl5/site_perl
    ;;
esac

export PERL5LIB_PATH

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
  <runtime name="GIT_SSL_CAINFO" value="$GIT_BASE/share/ssl/certs/ca-bundle.crt" type="path"/>
  <runtime name="GIT_EXEC_PATH" value="$GIT_BASE/libexec/git-core" type="path"/>
  <runtime name="PERL5LIB" value="$GIT_BASE@PERL5LIB_PATH@" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
