### RPM external libtool 2.4.2
Source: http://mirror.switch.ch/ftp/mirror/gnu/%n/%n-%realversion.tar.gz

%prep
%setup -n %n-%{realversion}

%build
./configure --prefix=%{i} --enable-static=no
make %makeprocesses

%install
make install

%define drop_files %i/share/{man,info}
%define strip_files %i/lib
