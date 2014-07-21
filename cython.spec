### RPM external cython 0.19.1
## INITENV +PATH PYTHONPATH %{i}/$PYTHON_LIB_SITE_PACKAGES

Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz

Requires: python

%prep
%setup -q -n %{n}/%{realversion}

%build
${PYTHON_ROOT}/bin/python setup.py build

%install
${PYTHON_ROOT}/bin/python setup.py install --prefix %{i}

sed -ideleteme 's|#!.*/bin/python|#!/usr/bin/env python|' \
  %{i}/bin/cython \
  %{i}/bin/cygdb \
  %{i}/${PYTHON_LIB_SITE_PACKAGES}/Cython/Debugger/libpython.py

find %{i} -name '*deleteme' -delete

find %{i}/${PYTHON_LIB_SITE_PACKAGES} -name '*.egg-info' -print0 | xargs -0 rm -f
