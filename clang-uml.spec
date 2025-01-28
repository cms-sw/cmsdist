### RPM external clang-uml 0.5.6

%define tag 5e8d35f181d1818310fb337e133e9d7600280e1f
%define branch master

%define github_user bkryza
Source: git+https://github.com/%{github_user}/clang-uml.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
BuildRequires: cmake ninja 
Requires: yaml-cpp llvm zlib zstd libxml2

%prep
%setup -n %{n}-%{realversion}

%build
rm -rf ../build
mkdir ../build
cd ../build

#GIT_VERSION can be a random string with the correct set of fields
#it is required as the current default in clang-uml cmake system is not
#correctly formated (issue opened)

cmake ../%{n}-%{realversion} \
  -G Ninja \
  -DCMAKE_INSTALL_PREFIX:PATH="%i" \
  -DCMAKE_BUILD_TYPE=Release \
%ifarch aarch64
  -DCMAKE_CXX_FLAGS="-Wno-sign-compare" \
%endif
  -DGIT_VERSION="%{realversion}" \
  -DCMAKE_EXE_LINKER_FLAGS="-L${YAML_CPP_ROOT}/lib64" \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}"

ninja -v %{makeprocesses}

%install
cd ../build
ninja %{makeprocesses} install
