### RPM external odb 2.4.0
Source: http://www.codesynthesis.com/download/odb/2.4/%{n}-%{realversion}.tar.gz

Requires: libcutl libodb libodb-sqlite sqlite

%prep
%setup -n %{n}-%{realversion}

%build
./configure --prefix=%{i} CPPFLAGS=-I${LIBCUTL_ROOT}/include LDFLAGS=-L${LIBCUTL_ROOT}/lib
make

%install
make install
