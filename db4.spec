### RPM external db4 4.4.20
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif
Source: http://download.oracle.com/berkeley-db/db-%{realversion}.NC.tar.gz
%define drop_files %i/docs
%define strip_files %i/lib

%prep
%setup -n db-%{realversion}.NC

%build
mkdir obj
cd obj
case %{cmsplatf} in
   *_mic_* )
     CXX="icpc -fPIC -mmic"  CC="icc -fPIC -mmic" ../dist/configure --prefix=%{i} --disable-java --disable-tcl --disable-static --build="%{_build}" --host=x86_64-k1om-linux
     ;;
   * )
     ../dist/configure --prefix=%{i} --build="%{_build}" --host="%{_host}" \
                  --disable-java --disable-tcl --disable-static
     ;;
esac
make %{makeprocesses}

%install
cd obj
make install
