### RPM external millepede V04-13-01
Source: https://gitlab.desy.de/claus.kleinwort/millepede-ii/-/archive/%{realversion}/%{n}-ii-%{realversion}.tar.gz
Requires: zlib

%prep
%setup -n %{n}-ii-%{realversion}

%build
make \
  ZLIB_INCLUDES_DIR="${ZLIB_ROOT}/include" \
  ZLIB_LIBS_DIR="${ZLIB_ROOT}/lib" \
  SUPPORT_LAPACK64=yes \
  LAPACK64=MKL \
  LAPACK64_LIBS_DIR="/cvmfs/projects.cern.ch/intelsw/oneAPI/linux/x86_64/2022/mkl/2022.1.0/lib/intel64" \
  LAPACK64_LIB=mkl_rt 

%install
make install PREFIX=%{i}
