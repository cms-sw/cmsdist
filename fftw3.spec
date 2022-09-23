### RPM external fftw3 3.3.8
Source: http://www.fftw.org/fftw-%{realversion}.tar.gz

%prep
%setup -n fftw-%{realversion}

%build
CONFIG_ARGS="--with-pic --enable-shared --enable-threads --disable-fortran
             --disable-dependency-tracking --disable-mpi --disable-openmp
             --prefix=%{i} --build=%{_build} --host=%{_host}"

%ifarch x86_64
    CONFIG_ARGS="${CONFIG_ARGS} --enable-sse2"
%endif

./configure ${CONFIG_ARGS}

make %{makeprocesses}

%install
make install

# Strip libraries, we are not going to debug them.
%define strip_files %{i}/lib

# Remove documentation. 
%define drop_files %{i}/share

%post
%relocateConfigAll lib/cmake *.cmake
