### RPM external adept v0.1.6-alpha
%define tag %{realversion}
%define branch master
%define github_user apt-sim
Source: git+https://github.com/%github_user/%{n}.git?obj=%{branch}/%{tag}&export=%{n}.%{realversion}&output=/%{n}.%{realversion}-%{tag}.tgz

## INCLUDE geant4-deps
## INCLUDE cuda-flags
Requires: geant4 g4hepem
%{!?without_cuda:Requires: cuda}

%prep
%setup -n %{n}.%{realversion}

%build

rm -rf ../build
mkdir ../build
cd ../build

cmake ../%{n}.%{realversion} \
  -DCMAKE_CXX_COMPILER="g++" \
  -DCMAKE_CXX_STANDARD:STRING="%{cms_cxx_standard}" \
  -DCMAKE_CXX_FLAGS="%{build_flags}" \
  -DCMAKE_C_FLAGS="%{build_flags}" \
  -DCMAKE_STATIC_LIBRARY_CXX_FLAGS="%{build_flags}" \
  -DCMAKE_STATIC_LIBRARY_C_FLAGS="%{build_flags}" \
  -DCMAKE_AR=$(which gcc-ar) \
  -DCMAKE_RANLIB=$(which gcc-ranlib) \
  -DCMAKE_INSTALL_PREFIX:PATH="%i" \
  -DBUILD_SHARED_LIBS=OFF \
  -DCMAKE_BUILD_TYPE=Release \
%if 0%{!?without_cuda:1}
  -DCMAKE_CUDA_ARCHITECTURES=$(echo %{cuda_arch} | tr ' ' ';' | sed 's|;;*|;|') \
%endif
  -DASYNC_MODE=ON \
  -DADEPT_USE_EXT_BFIELD=ON \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}"

make %makeprocesses VERBOSE=1

%install

cd ../build
make install

%post
%{relocateCmsFiles} $(find $RPM_INSTALL_PREFIX/%{pkgrel} -name '*.cmake')
