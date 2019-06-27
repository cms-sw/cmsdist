### RPM external p5-compress-zlib-toolfile 1.0
Requires: p5-compress-zlib

%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/p5-compress-zlib.xml
<tool name="p5-compress-zlib" version="@TOOL_VERSION@">
  <client>
    <environment name="P5_COMPRESS_ZLIB_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PERL5LIB" value="$P5_COMPRESS_ZLIB_BASE/lib/perl5" type="path"/>
  <use name="p5-extutils-makemaker"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
