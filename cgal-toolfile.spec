### RPM external cgal-toolfile 1.0
Requires: cgal
%prep

%build

%install

mkdir -p %{i}/etc/scram.d

# CGAL Core
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/cgal.xml
<tool name="cgal" version="@TOOL_VERSION@">
  <info url="http://www.cgal.org/"/>
  <lib name="CGAL_Core"/>
  <lib name="CGAL"/>
  <client>
    <environment name="CGAL_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$CGAL_BASE/lib"/>
    <environment name="INCLUDE" default="$CGAL_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="zlib"/>
  <use name="boost_system"/>
  <use name="gmp"/>
  <use name="mpfr"/>
</tool>
EOF_TOOLFILE

# CGAL ImageIO (brings libSM from X11)
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/cgalimageio.xml
<tool name="cgalimageio" version="@TOOL_VERSION@">
  <info url="http://www.cgal.org/"/>
  <lib name="CGAL_ImageIO"/>
  <use name="zlib"/>
  <use name="boost_system"/>
  <use name="cgal"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
