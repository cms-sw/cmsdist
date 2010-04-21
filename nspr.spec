### RPM external nspr 4.8.4 
Source: https://ftp.mozilla.org/pub/mozilla.org/nspr/releases/v%{realversion}/src/%n-%{realversion}.tar.gz

%build
pushd mozilla/nsprpub
  ./configure --prefix %i
  make %makeprocesses
popd

%install
pushd mozilla/nsprpub
  make install
popd
find %i/lib -name '*.so' -exec rm {} \;
find %i/lib -name '*.dylib' -exec rm {} \;
