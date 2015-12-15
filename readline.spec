### RPM external readline 6.3
Source: ftp://ftp.cwru.edu/pub/bash/%{n}-%{realversion}.tar.gz
%define keep_archives true
%define drop_files %{i}/lib/*.so

%prep
%setup -n %{n}-%{realversion}

%build
./configure --prefix %{i} --build="%{_build}" --host="%{_host}" \
            --disable-shared --enable-static
make %{makeprocesses} CFLAGS="-O2 -fPIC"


%install
make install
