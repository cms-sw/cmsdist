### RPM external libnl 3.12.0
%define version_path libnl%(echo %{realversion} | tr . _)
Source: git+https://github.com/thom311/libnl.git?obj=main/%{version_path}&export=%{n}&output=/%{n}-%{realversion}.tar.gz
BuildRequires: gmake autotools swig flex bison
%define keep_pkgconfig true

%prep
%setup -n %{n}

%build
autoreconf -vif
./configure --prefix=%{i} --disable-static
make %{makeprocesses} VERBOSE=1

%install
make install

%post
%relocateConfigAll lib/pkgconfig *.pc
