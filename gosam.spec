
### RPM external gosam 2.0.4-12f4de9
Source: http://www.hepforge.org/archive/gosam/gosam-%{realversion}.tar.gz

Requires: qgraf
Requires: form
Requires: gosamcontrib
Requires: python cython

%prep
%setup -q -n gosam

%build
CXX="$(which c++) -fPIC"
CC="$(which gcc) -fPIC"
FC="$(which gfortran)"
PLATF_CONF_OPTS="--enable-shared --disable-static"
export PYTHONPATH=${CYTHON_ROOT}/${PYTHON_LIB_SITE_PACKAGES}
python setup.py install --prefix=%{i}

%install
perl -p -i -e "s|^#!.*python|#!/usr/bin/env python$1|" $(grep -r -e "^#\!.*python.*" %i | cut -d: -f1)
find %{i}/lib -name '*.la' -exec rm -f {} \;

%post
%{relocateConfig}bin/gosam.py
%{relocateConfig}bin/gosam-config.py
%{relocateConfig}lib/python2.7/site-packages/golem/installation.py
