### RPM external py2-numpy-toolfile 1.0
Requires: py2-numpy

%define pythonver %(echo %{allpkgreqs} | tr ' ' '\\n' | grep ^external/python/ | cut -d/ -f3 | cut -d. -f 1,2)
%define numpyver %(echo %{allpkgreqs} | tr ' ' '\\n' | grep ^external/py2-numpy/ | cut -d/ -f3 | cut -d- -f 1)
%define numpyArch %(uname -m)


%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/py2-numpy.xml
<tool name="py2-numpy" version="@TOOL_VERSION@">
  <client>
    <environment name="PY2_NUMPY_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="PATH" value="$PY2_NUMPY_BASE/bin" type="path"/>
  <runtime name="PYTHON27PATH" value="$PY2_NUMPY_BASE/lib/python@PYTHONV@/site-packages/numpy-%{numpyver}-py%{pythonver}-linux-%{numpyArch}.egg" type="path"/>
  <use name="python"/>
  <use name="zlib"/>
  <use name="lapack"/>
  <use name="OpenBLAS"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-numpy-c-api.xml
<tool name="py2-numpy-c-api" version="@TOOL_VERSION@">
  <client>
    <environment name="PY2_NUMPY_C_API_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$PY2_NUMPY_C_API_BASE/c-api/core/include"/>
  </client>
  <use name="python"/>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)
## IMPORT scram-tools-post
