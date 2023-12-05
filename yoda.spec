### RPM external yoda 1.9.8
## INITENV +PATH PYTHON3PATH %i/${PYTHON3_LIB_SITE_PACKAGES}

Source: git+https://gitlab.com/hepcedar/yoda.git?obj=main/%{n}-%{realversion}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
Patch0: yoda-deprecated-warn
Requires: python3 root
BuildRequires: py3-cython autotools python-python3

%prep
%setup -q -n %{n}-%{realversion}
%patch0 -p1

autoreconf -fiv

%build

PYTHON=$(which python3) ./configure --prefix=%i --enable-root
sed -i "s|env python|env python3|" bin/*
make %{makeprocesses} all
make install

%install

%post
%{relocateConfig}bin/yoda-config
