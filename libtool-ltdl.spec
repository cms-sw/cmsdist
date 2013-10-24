### RPM external libtool-ltdl 2.4.2
Source: http://mirror.switch.ch/ftp/mirror/gnu/libtool/libtool-%realversion.tar.gz

%prep
%setup -n libtool-%realversion

%build
./configure --prefix=%{i}
make

%install
make install-libLTLIBRARIES install-ltdlincludeHEADERS

%define drop_files %i/docs
%define strip_files %i/lib
