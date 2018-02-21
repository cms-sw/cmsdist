### RPM external libodb 2.4.0
Source: http://www.codesynthesis.com/download/odb/2.4/%{n}-%{realversion}.tar.gz

%prep
%setup -n %{n}-%{realversion}

%build
./configure --prefix=%{i} 
make

%install
make install
