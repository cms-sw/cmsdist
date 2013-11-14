### RPM external py2-pyfits-toolfile 1.0
Requires: py2-pyfits
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-pyfits.xml
<tool name="py-pyfits" version="@TOOL_VERSION@">
  <info url="http://www.stsci.edu/institute/software_hardware/pyfits"/>
  <client>
    <environment name="PY2_PYFITS" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PY2_PYFITS/lib"/>
    <runtime name="PYTHONPATH" value="$PY2_PYFITS/lib/python2.7/site-packages" type="path"/>
  </client>
  <use name="gsl"/>
  <use name="lapack"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
