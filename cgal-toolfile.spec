### RPM external cgal-toolfile 1.0
Requires: cgal
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/cgal.xml
<tool name="cgal" version="@TOOL_VERSION@">
  <info url="http://www.cgal.org/"/>
  <lib name="CGAL_Core"/>
  <lib name="CGAL_ImageIO"/>
  <lib name="CGAL"/>
  <client>
    <environment name="CGAL_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$CGAL_BASE/lib"/>
    <environment name="INCLUDE" default="$CGAL_BASE/include"/>
  </client>
  <use name="zlib"/>
  <use name="boost_system"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
