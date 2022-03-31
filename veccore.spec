### RPM external veccore 0.8.0
## INCLUDE compilation_flags
Source: https://github.com/root-project/veccore/archive/refs/tags/v%{realversion}.tar.gz

BuildRequires: cmake gmake

%prep
%setup -n %{n}-%{realversion}

%build
rm -rf ../build
mkdir ../build
cd ../build

cmake ../%{n}-%{realversion} \
  -DCMAKE_INSTALL_PREFIX:PATH="%i" \
%if "%{?arch_build_flags}"
  -DCMAKE_CXX_FLAGS="%{arch_build_flags}" \
%endif
  -DCMAKE_BUILD_TYPE=Release

make %{makeprocesses}

%install
cd ../build
make %{makeprocesses} install

%post
%{relocateConfig}lib/cmake/VecCore/*.cmake

