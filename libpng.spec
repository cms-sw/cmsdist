### RPM external libpng 1.2.34
Source: ftp://ftp.simplesystems.org/pub/libpng/png/src/%{n}-%{realversion}.tar.bz2

%build
./configure --prefix=%{i}
make %makeprocesses 
