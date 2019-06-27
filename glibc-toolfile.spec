### RPM external glibc-toolfile 1.0
Requires: glibc

%prep
%build
%install
mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE > %{i}/etc/scram.d/glibc.xml
  <tool name="glibc" version="@TOOL_VERSION@">
    <info url="http://www.gnu.org/software/libc/libc.html"/>
    <client>
      <environment name="GLIBC_BASE" default="@TOOL_ROOT@"/>
    </client>
  </tool>
EOF_TOOLFILE
## IMPORT scram-tools-post
# bla bla
