### RPM external qd 2.3.13
Source: http://crd.lbl.gov/~dhbailey/mpdist/qd-%{realversion}.tar.gz
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
Requires: icc icc-provides
%endif

%prep
%setup -n qd-%{realversion}
%if "%mic" == "true"
./configure --prefix=%i --enable-shared \
            CXX="icpc -mmic " \
            CC="icc -mmic" \
            FC="ifort -mmic" \
            --host=x86_64-k1om-linux
%else
./configure --prefix=%i --enable-shared 
%endif
# The following hack insures that the bins with the library linked explicitly
# rather than indirectly, as required by the gold linker
%build
make %{makeprocesses}
%install
make install
