### RPM external cython 0.19.1

Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz

Requires: python

%prep
%setup -q -n %{n}/%{realversion}

%build
${PYTHON_ROOT}/bin/python setup.py build

%install
${PYTHON_ROOT}/bin/python setup.py install --prefix %i
