### RPM external c-ares 1.15.0
%define uversion %(echo %realversion | sed -e 's/\\./_/g')
Source: https://github.com/c-ares/c-ares/archive/cares-%{uversion}.tar.gz

BuildRequires: cmake gmake

%define drop_files %{i}/lib/pkgconfig
%define strip_files %{i}/lib

%prep
%setup -n %{n}-cares-%{uversion}

%build
rm -rf ../build
mkdir ../build
cd ../build

cmake ../%{n}-cares-%{uversion} \
  -DCMAKE_INSTALL_PREFIX:PATH="%i" \
  -DCMAKE_BUILD_TYPE=Release

make %{makeprocesses} VERBOSE=1

%install
cd ../build
make %{makeprocesses} install
