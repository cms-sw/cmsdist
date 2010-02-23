### RPM external beecrypt 4.1.2-CMS19
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib64
Source: http://puzzle.dl.sourceforge.net/sourceforge/%n/%n-%realversion.tar.gz
%prep
%setup -n %n-%realversion
%build
./configure --prefix=%i --without-python --without-java
make
