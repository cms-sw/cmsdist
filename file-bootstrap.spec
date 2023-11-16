### RPM external file-bootstrap 5.33
%define file_tag %(echo FILE%{realversion} | tr . _)
AutoReqProv: no
Source: https://github.com/file/file/archive/%{file_tag}.tar.gz

%prep  
%setup -n file-%{file_tag}

%build
autoreconf -fiv
./configure --prefix=%{i}
make

%install
make install
