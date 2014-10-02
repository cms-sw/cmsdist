### RPM external cython 0.19.1

Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz

Requires: python

%prep
%setup -q -n %{n}/%{realversion}

%build
python setup.py build

%install
python setup.py install --prefix %i
perl -p -i -e "s|^#!%{cmsroot}/.*|#!/usr/bin/env python|" %{i}/bin/cython
perl -p -i -e "s|^#!%{cmsroot}/.*|#!/usr/bin/env python|" %{i}/bin/cygdb
