### RPM external g4hepem 20250610
%define tag %{realversion}
%define branch master
%define github_user mnovak42
Source: git+https://github.com/%github_user/%{n}.git?obj=%{branch}/%{tag}&export=%{n}.%{realversion}&output=/%{n}.%{realversion}-%{tag}.tgz

## INCLUDE geant4-deps
## INCLUDE cuda-flags
Requires: geant4
%{!?without_cuda:Requires: cuda}

%prep
%setup -n %{n}.%{realversion}

%build

rm -rf ../build
mkdir ../build
cd ../build

cmake ../%{n}.%{realversion} \
  -DCMAKE_CXX_COMPILER="g++" \
  -DCMAKE_STATIC_LIBRARY_CXX_FLAGS="%{build_flags}" \
  -DCMAKE_STATIC_LIBRARY_C_FLAGS="%{build_flags}" \
  -DCMAKE_CXX_FLAGS="%{build_flags}" \
  -DCMAKE_C_FLAGS="%{build_flags}" \
  -DCMAKE_AR=$(which gcc-ar) \
  -DCMAKE_RANLIB=$(which gcc-ranlib) \
  -DCMAKE_INSTALL_PREFIX:PATH="%i" \
  -DCMAKE_BUILD_TYPE=Release \
  -DBUILD_SHARED_LIBS=OFF \
  -DG4HepEm_EARLY_TRACKING_EXIT=ON \
%if 0%{!?without_cuda:1}
  -DCMAKE_CUDA_ARCHITECTURES=$(echo %{cuda_arch} | tr ' ' ';' | sed 's|;;*|;|') \
  -DG4HepEm_CUDA_BUILD=ON \
%else
  -DG4HepEm_CUDA_BUILD=OFF \
%endif
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}"

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
