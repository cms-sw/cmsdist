### RPM external yoda 1.8.3
## INITENV +PATH PYTHON27PATH %i/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %i/${PYTHON3_LIB_SITE_PACKAGES}

Source: git+https://gitlab.com/hepcedar/yoda.git?obj=master/%{n}-%{realversion}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

Requires: python root
BuildRequires: py2-cython autotools

%prep
%setup -q -n %{n}-%{realversion}

autoreconf -fiv
./configure --prefix=%i --enable-root

%build
make all

%install
make install

%post
%{relocateConfig}bin/yoda-config
