### RPM external clang-uml 0.6.2x

%define tag 5e2993e75ebc88af6cb239f2ffae88da7431cb0d
%define branch master

%define github_user bkryza
Source: git+https://github.com/%{github_user}/clang-uml.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
Patch0: clang-uml-clang21
BuildRequires: cmake ninja 
Requires: yaml-cpp llvm zlib zstd libxml2

%prep
%setup -n %{n}-%{realversion}
%patch0 -p1

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
