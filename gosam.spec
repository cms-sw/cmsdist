### RPM external gosam 2.1.0
%define tag %{realversion}
%define branch master
%define github_user gudrunhe
Source: git+https://github.com/%{github_user}/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

Requires: qgraf
Requires: form
Requires: gosamcontrib
Requires: python3 py3-cython

%prep
%setup -q -n %{n}-%{realversion}
grep -q '^VERSION *=' setup.py && grep -q '^GIT_REVISION *=' setup.py && grep -q '^TAR_VERSION *=' setup.py
sed -i -r -e 's#^VERSION *=.*#VERSION = "%{realversion}"#' setup.py
sed -i -r -e 's#^GIT_REVISION *=.*#GIT_REVISION = "%{realversion}"#' setup.py
sed -i -r -e 's#^TAR_VERSION *=.*#TAR_VERSION = "%{realversion}"#' setup.py

%build
CXX="$(which c++) -fPIC"
CC="$(which gcc) -fPIC"
FC="$(which gfortran)"
PLATF_CONF_OPTS="--enable-shared --disable-static"
python3 setup.py install --prefix=%{i}

%install
perl -p -i -e "s|^#!.*python.*|#!/usr/bin/env python3|" $(grep -r -e "^#\!.*python.*" %i | cut -d: -f1)
find %{i}/lib -name '*.la' -exec rm -f {} \;

%post
%{relocateConfig}bin/gosam.py
%{relocateConfig}bin/gosam-config.py
%{relocateConfig}lib/python%{cms_python3_major_minor_version}/site-packages/golem/installation.py
