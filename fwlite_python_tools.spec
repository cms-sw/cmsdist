### RPM external fwlite_python_tools 1.0
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}
Source: none
 
Requires: py2-six
Requires: py2-scipy
Requires: py2-numpy

%prep

%build

%install
mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/python_tools.xml
<tool name="%{n}" version="%{v}">
</tool>
EOF_TOOLFILE
