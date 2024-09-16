### RPM external clang-uml 0.5.2

%define tag cd6dce2b0b34d55534d3de512ab088b9ad71bc76
%define branch master

%define github_user bkryza
Source: git+https://github.com/%{github_user}/clang-uml.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
BuildRequires: cmake ninja 
Requires: yaml-cpp llvm zlib

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
  -DCMAKE_PREFIX_PATH="${YAML_CPP_ROOT}/lib64/cmake/yaml-cpp;${ZLIB_ROOT}"

ninja -v %{makeprocesses}

%install
cd ../build
ninja %{makeprocesses} install
