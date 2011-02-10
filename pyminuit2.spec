### RPM external pyminuit2 0.0.1
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
Source: http://pyminuit2.googlecode.com/files/%{n}-%{realversion}.tar.gz
Requires: root 


%prep
%setup -n %{n}-%{realversion}

%build
%install
python setup.py install --prefix=%i
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/pyminuit2.xml
<tool name="pyminuit2" version="%v">
<client>
<environment name="PYMINUIT2_BASE" default="%i"/>
</client>
<runtime name="PYTHONPATH" value="$PYMINUIT2_BASE/lib/python2.6/site-packages" type="path"/>
</tool>
EOF_TOOLFILE

#export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)
