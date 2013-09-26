### RPM external nspr 4.9.5
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif
Source: https://ftp.mozilla.org/pub/mozilla.org/nspr/releases/v%{realversion}/src/%{n}-%{realversion}.tar.gz
Patch0: nspr-4.8.9-mic
%define strip_files %{i}/lib

%define isamd64 %(case %{cmsplatf} in (*amd64*|*_mic_*) echo 1 ;; (*) echo 0 ;; esac)

%prep
%setup -n %n-%{realversion}
%if "%mic" == "true"
%patch0 -p1
%endif

%build
pushd mozilla/nsprpub
CONF_OPTS="--disable-static --prefix=%{i} --build=%{_build} --host=%{_host}"
%if %isamd64
CONF_OPTS="${CONF_OPTS} --enable-64bit"
%endif

%if "%mic" == "true"
CXX="icpc -fPIC -mmic"  CC="icc -fPIC -mmic" ./configure ${CONF_OPTS}
%else
./configure ${CONF_OPTS}
%endif
make %{makeprocesses}
popd

%install
pushd mozilla/nsprpub
make install
popd
