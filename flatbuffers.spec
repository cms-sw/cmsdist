### RPM external flatbuffers 2.0.6
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib64

%define tag v%{realversion}
%define branch master
%define github_user google
Source: git+https://github.com/%{github_user}/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
Patch0: flatbuffers-7422

BuildRequires: cmake gmake

%prep
%setup -n %{n}-%{realversion}
%patch0 -p1

%build
rm -rf ../build
mkdir ../build
cd ../build

cmake ../%{n}-%{realversion} \
   -DCMAKE_BUILD_TYPE=Release \
  -DFLATBUFFERS_BUILD_CPP17=ON \
  -DFLATBUFFERS_BUILD_SHAREDLIB=ON \
  -DFLATBUFFERS_BUILD_TESTS=OFF \
  -DCMAKE_INSTALL_PREFIX="%{i}"

make -v %{makeprocesses}

%install
cd ../build

make %{makeprocesses} install

%post
%{relocateConfig}lib64/pkgconfig/flatbuffers.pc
