### RPM external yoda 2.1.2
## INITENV +PATH PYTHON3PATH %i/${PYTHON3_LIB_SITE_PACKAGES}

Source: git+https://gitlab.com/hepcedar/yoda.git?obj=main/%{n}-%{realversion}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

Requires: python3 root hdf5 highfive
BuildRequires: py3-cython autotools python-python3

%prep
%setup -q -n %{n}-%{realversion}

autoreconf -fiv

%build

PYTHON=$(which python3) ./configure --prefix=%i --enable-root --with-highfive=${HIGHFIVE_ROOT} CXX="mpicxx"
make %{makeprocesses} all
make install

%install

%post
%{relocateConfig}bin/yoda-config
