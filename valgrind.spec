### RPM external valgrind 3.1.0
## BUILDIF case $(uname):$(uname -m) in Linux:i*86 ) true ;; * ) false ;; esac
Source: http://www.valgrind.org/downloads/%{n}-%{v}.tar.bz2
%build
./configure --prefix=%i
make %makeprocesses
