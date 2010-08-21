### RPM external igprof 5.6.0.20100511
Source: http://igprof.git.sourceforge.net/git/gitweb.cgi?p=igprof/igprof;a=snapshot;h=38bf98abe11e69d71d81d9d76efb783910cd90ee;sf=tgz
Requires: libunwind cmake

%prep
%setup -n %n

%build
cmake -DCMAKE_INSTALL_PREFIX=%i .
make %makeprocesses

%install
make %makeprocesses install
