### RPM external blackhat 0.9.9
Source: http://www.hepforge.org/archive/blackhat/blackhat-%{realversion}.tar.gz
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
Requires: icc icc-provides
%endif

Patch0: blackhat-gcc48
Patch1: blackhat-0.9.9-armv7hl
Patch2: blackhat-no_warnings

Requires: qd python openssl swig
%prep
%setup -n blackhat-%{realversion}

%patch0 -p1
%patch1 -p1
%patch2 -p1

%if "%mic" == "true"
export LD_LIBRARY_PATH=$PYTHON_ROOT/host
PYTHON=$PYTHON_ROOT/host/python ./configure --prefix=%i --with-QDpath=$QD_ROOT CXXFLAGS="-Wno-deprecated -I$OPENSSL_ROOT/include" LDFLAGS="-L$OPENSSL_ROOT/lib -L$PYTHON_ROOT/lib" \
            CXX="icpc -mmic " \
            CC="icc -mmic" \
            FC="ifort -mmic" \
            --host=x86_64-k1om-linux
%else
./configure --prefix=%i --with-QDpath=$QD_ROOT CXXFLAGS="-Wno-deprecated -I$OPENSSL_ROOT/include" LDFLAGS="-L$OPENSSL_ROOT/lib"
%endif
# The following hack insures that the bins with the library linked explicitly
# rather than indirectly, as required by the gold linker
%build
make %{makeprocesses}
%install
make install
