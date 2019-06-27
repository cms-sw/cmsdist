### RPM external p5-extutils-makemaker-toolfile 1.0
Requires: p5-extutils-makemaker

%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/p5-extutils-makemaker.xml
<tool name="p5-extutils-makemaker" version="@TOOL_VERSION@">
  <client>
    <environment name="P5_EXTUTILS_MAKEMAKER_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PATH" value="$P5_EXTUTILS_MAKEMAKER_BASE/bin" type="path"/>
  <runtime name="PERL5LIB" value="$P5_EXTUTILS_MAKEMAKER_BASE/lib/perl5" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
