### RPM external readline 6.2
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif
Source: ftp://ftp.cwru.edu/pub/bash/%{n}-%{realversion}.tar.gz
%define keep_archives true
%define drop_files %{i}/lib/*.so

%prep
%setup -n %{n}-%{realversion}

%build
case %{cmsplatf} in
   *_mic_* )
CXX="icpc -fPIC -mmic"  CC="icc -fPIC -mmic" \
./configure --prefix %i --disable-shared --enable-static --host=x86_64-k1om-linux
     ;;
    * )
./configure --prefix %{i} --build="%{_build}" --host="%{_host}" \
            --disable-shared --enable-static
     ;;
esac
make %{makeprocesses} CFLAGS="-O2 -fPIC"

%install
make install
