### RPM external libpng 1.2.10
Source: ftp://ftp.simplesystems.org/pub/libpng/png/src/%{n}-%{v}.tar.bz2

%build
./configure --prefix=%{i}
make %makeprocesses 
