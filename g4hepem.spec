### RPM external g4hepem 20230309
## INCLUDE compilation_flags
## INCLUDE compilation_flags_lto
%define tag %{realversion}
%define branch master
%define github_user mnovak42
Source: git+https://github.com/%github_user/%{n}.git?obj=%{branch}/%{tag}&export=%{n}.%{realversion}&output=/%{n}.%{realversion}-%{tag}.tgz

BuildRequires: cmake gmake

Requires: geant4

%define keep_archives true
%define build_flags -fPIC %{?arch_build_flags} %{?lto_build_flags} %{?pgo_build_flags}

%prep
%setup -n %{n}.%{realversion}

%build

rm -rf ../build
mkdir ../build
cd ../build

cmake ../%{n}.%{realversion} \
  -DCMAKE_CXX_COMPILER="g++" \
  -DCMAKE_CXX_FLAGS="%{build_flags}" \
  -DCMAKE_AR=$(which gcc-ar) \
  -DCMAKE_RANLIB=$(which gcc-ranlib) \
  -DCMAKE_INSTALL_PREFIX:PATH="%i" \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="${GEANT4_ROOT}"

make %makeprocesses VERBOSE=1

%install

cd ../build
make install

mkdir -p %i/lib64/archive
cd %i/lib64/archive
find %i/lib64 -name "*.a" -exec gcc-ar x {} \;
gcc-ar rcs libg4hepem-static.a *.o
find . -name "*.o" -delete

%post
%{relocateCmsFiles} $(find $RPM_INSTALL_PREFIX/%{pkgrel} -name '*.cmake')
