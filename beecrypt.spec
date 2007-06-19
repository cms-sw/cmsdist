### RPM external beecrypt 3.1.0-wt1
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib64
Source: http://switch.dl.sourceforge.net/sourceforge/%n/%n-%realversion.tar.gz
%prep
%setup -n %n-%realversion
%build
./configure --prefix=%i --without-python --without-java
make
