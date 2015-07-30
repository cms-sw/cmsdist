### RPM external professor 1.4.0
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
Source: http://www.hepforge.org/archive/professor/professor-%{realversion}.tar.gz

Requires: py2-numpy py2-scipy pyminuit2 py2-matplotlib
%prep
%setup -n professor-%{realversion}

%build
${PYTHON_ROOT}/bin/python setup.py build -e "/usr/bin/env python"

%install
${PYTHON_ROOT}/bin/python setup.py install --prefix=%i
