### RPM external py2-cmsml 0.1.0
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}

Requires: python py2-six
Source: https://github.com/cms-ml/cmsml/archive/v%{realversion}.tar.gz

%prep
%setup -n cmsml-%{realversion}

%build

%install
python setup.py install --single-version-externally-managed --record=/dev/null --prefix=%{i}
sed -i "s/#\!.*/#\!\/usr\/bin\/env python/" %{i}/bin/*
