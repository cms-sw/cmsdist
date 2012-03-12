### RPM external nspr 4.8.9
Source: https://ftp.mozilla.org/pub/mozilla.org/nspr/releases/v%{realversion}/src/%n-%{realversion}.tar.gz

%build
case %cmsplatf in
  *_amd64_*)
    USER_CFGOPTS="--enable-64bit"
  ;;
esac

pushd mozilla/nsprpub
  ./configure --disable-static --prefix %i $USER_CFGOPTS
  make %makeprocesses
popd

%install
pushd mozilla/nsprpub
  make install
popd
%define strip_files %i/lib
