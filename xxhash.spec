### RPM external xxhash 0.8.2

Source: https://github.com/Cyan4973/xxHash/archive/refs/tags/v%{realversion}.tar.gz

%prep
%setup -n xxHash-%{realversion}

%build
make %{makeprocesses} prefix=%{i}

%install
make install prefix=%{i}
