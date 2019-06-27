### RPM external gsl-toolfile 1.0
Requires: gsl
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/gsl.xml
<tool name="gsl" version="@TOOL_VERSION@">
  <info url="http://www.gnu.org/software/gsl/gsl.html"/>
  <lib name="gsl"/>
  <lib name="gslcblas"/>
  <client>
    <environment name="GSL_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$GSL_BASE/lib"/>
    <environment name="INCLUDE" default="$GSL_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
