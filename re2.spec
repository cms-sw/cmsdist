### RPM external re2 2021-06-01
Source: https://github.com/google/re2/archive/%{realversion}.tar.gz

BuildRequires: cmake gmake

%define strip_files %{i}/lib

%prep
%setup -n %{n}-%{realversion}

%build
rm -rf ../build
mkdir ../build
cd ../build

cmake ../%{n}-%{realversion} \
  -DCMAKE_INSTALL_PREFIX:PATH="%i" \
  -DCMAKE_BUILD_TYPE=Release \
  -DBUILD_SHARED_LIBS=True \
  -DCMAKE_POSITION_INDEPENDENT_CODE=True \
  -DCMAKE_INSTALL_LIBDIR=lib

make %{makeprocesses} VERBOSE=1

%install
cd ../build
make %{makeprocesses} install
