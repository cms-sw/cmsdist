### RPM external perl 5.8.8
## INITENV +PATH PATH %i/bin
Source: http://www.perl.com/CPAN/src/%n-%v.tar.bz2
%prep
%setup -n %{n}-%{v}
%build
./Configure -des -Dprefix='%i' \
            -Dccflags='-I%i/include' \
            -Dldflags=-L'%i/lib' \
            -Dvendorprefix='%i' 
make %makeprocesses
%install
make install
