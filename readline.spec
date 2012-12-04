### RPM external readline 6.2
Source: ftp://ftp.cwru.edu/pub/bash/readline-%realversion.tar.gz
%define keep_archives true
%define drop_files %i/lib/*.so

%prep
%setup -n readline-%realversion
%build
./configure --prefix %i --disable-shared --enable-static
make %makeprocesses
%install
make install
