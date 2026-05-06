### RPM external file-bootstrap 5.47
%define keep_archives true
%define file_tag %(echo FILE%{realversion} | tr . _)
AutoReqProv: no
Source: https://github.com/file/file/archive/%{file_tag}.tar.gz

%prep  
%setup -n file-%{file_tag}

%build
autoreconf -fiv
./configure --prefix=%{i} \
  --disable-shared \
  --enable-static \
  --disable-xzlib \
  --disable-zstdlib

make %{makeprocesses}

%install
make install
