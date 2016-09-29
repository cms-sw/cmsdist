### RPM external py2-h5py-toolfile 1.0
Requires: py2-h5py
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/py2-h5py.xml
<tool name="py2-h5py" version="@TOOL_VERSION@">
  <info url="https://pypi.python.org/pypi/h5py"/>
  <client>
    <environment name="PY2_H5PY" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$PY2_H5PY/lib"/>
    <runtime name="PYTHONPATH" value="$PY2_H5PY/lib/python@PYTHONV@/site-packages" type="path"/>
  </client>
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
