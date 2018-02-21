### RPM external libcutl 1.10.0
Source0: https://www.codesynthesis.com/download/libcutl/1.10/%{n}-%{realversion}.tar.gz

%prep
%setup -n %{n}-%{realversion}

%build
./configure --prefix=%{i}
make

%install
make install
