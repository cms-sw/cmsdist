### RPM external yoda 1.9.6
## INITENV +PATH PYTHON3PATH %i/${PYTHON3_LIB_SITE_PACKAGES}

Source: git+https://gitlab.com/hepcedar/yoda.git?obj=main/%{n}-%{realversion}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

Requires: python3 root
BuildRequires: py3-cython autotools python-python3

%prep
%setup -q -n %{n}-%{realversion}

autoreconf -fiv

%build

sed -i -e "s|lPyROOT|lcppyyX.X|" ./pyext/setup.py.in

sed -i -e "s|lcppyy...|lcppyy$(echo %{cms_python3_major_minor_version} | tr . _)|" ./pyext/setup.py.in
PYTHON=$(which python3) ./configure --prefix=%i --enable-root
sed -i "s|env python|env python3|" bin/*
make %{makeprocesses} all
make install

%install

%post
%{relocateConfig}bin/yoda-config
%{relocateConfig}lib/python*/site-packages/yoda*egg-info/SOURCES.txt
