### RPM external nspr-bootstrap 4.10.8
Source: https://ftp.mozilla.org/pub/mozilla.org/nspr/releases/v%{realversion}/src/nspr-%{realversion}.tar.gz
%define strip_files %{i}/lib

%prep
%setup -n nspr-%{realversion}

%build
pushd nspr

CONF_OPTS="--disable-static --prefix=%{i} --build=%{_build} --host=%{_host}"
case "%{cmsplatf}" in
  *_aarch64_*|*_amd64_*|*_ppc64le_*|*_mic_*)
    CONF_OPTS="${CONF_OPTS} --enable-64bit"
    ;;
esac

./configure ${CONF_OPTS}
make %{makeprocesses}
popd

%install
pushd nspr
make install
popd
