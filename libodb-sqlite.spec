### RPM external libodb-sqlite 2.4.0
Source: http://www.codesynthesis.com/download/odb/2.4/libodb-sqlite-%{realversion}.tar.gz

Requires:  sqlite libodb

%prep
%setup -n %{n}-%{realversion}

%build
./configure --prefix=%{i} CPPFLAGS=-I${LIBODB_ROOT}/include LDFLAGS=-L${LIBODB_ROOT}/lib
make 

%install
make install
