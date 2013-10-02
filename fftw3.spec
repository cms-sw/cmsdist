### RPM external fftw3 3.3.2
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif
Source: http://www.fftw.org/fftw-%{realversion}.tar.gz

%prep
%setup -n fftw-%{realversion}

%build
CONFIG_ARGS="--with-pic --enable-shared --enable-threads --disable-fortran
             --disable-dependency-tracking --disable-mpi --disable-openmp
             --prefix=%{i} --build=%{_build} --host=%{_host}"

case "%{cmsplatf}" in
  *_mic_*)
    CONFIG_ARGS="${CONFIG_ARGS} --host=x86_64-k1om-linux"
  ;;
  *amd64*|*_mic_*)
    CONFIG_ARGS="${CONFIG_ARGS} --enable-sse2 "
  ;;
#  *armv7hl*)
#    CONFIG_ARGS="${CONFIG_ARGS} --enable-neon --enable-float"
#  ;;
esac

%if "%mic" == "true"
CXX="icpc -mmic" CC="icc -mmic" \
%endif
./configure ${CONFIG_ARGS}

make %{makeprocesses}

%install
make install

# Strip libraries, we are not going to debug them.
%define strip_files %{i}/lib

# Remove documentation. 
%define drop_files %{i}/share
