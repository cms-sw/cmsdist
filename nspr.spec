### RPM external nspr 4.8.9
Source: https://ftp.mozilla.org/pub/mozilla.org/nspr/releases/v%{realversion}/src/%n-%{realversion}.tar.gz

%build
pushd mozilla/nsprpub
  ./configure --disable-static --prefix %i --enable-64bit
  make %makeprocesses
popd

%install
pushd mozilla/nsprpub
  make install
popd
%define strip_files %i/lib
