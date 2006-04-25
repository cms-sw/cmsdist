### RPM external gdbm 1.8.3
Source: http://rm.mirror.garr.it/mirrors/gnuftp/gnu/%{n}/%{n}-%{v}.tar.gz

%build
./configure --prefix=%{i}
make %makeprocesses
