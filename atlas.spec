### RPM external atlas 3.10.2
# NB: http://www.netlib.org/atlas/atlas-comm/msg00280.html
#     http://cvs.pld-linux.org/cgi-bin/cvsweb/SPECS/atlas.spec
Source: http://sourceforge.net/projects/math-atlas/files/Stable/%{realversion}/atlas%{realversion}.tar.bz2
Patch0: atlas.3.10.2

%prep
%setup -n ATLAS
%patch0 -p1

%build
curl -L -O http://www.netlib.org/lapack/lapack-3.3.1.tgz
mkdir BUILD
cd BUILD
../configure -b 64 --prefix=%{i} --with-netlib-lapack-tarfile=../lapack-3.3.1.tgz --shared
make build
make check
make ptcheck
make time

cd lib
make libatlas.so
make libf77blas.so
make libcblas.so
make liblapack.so
make libptf77blas.so
make libptcblas.so
make libptlapack.so
cd ..

%install
cd BUILD
make install
