### RPM external google-benchmark 1.7.x

BuildRequires: cmake ninja

%define benchmarkCommit b177433f3ee2513b1075140c723d73ab8901790f
%define benchmarkBranch main
%define googletestCommit 0bdaac5a1401fffac6b64581efc639734aded793
%define googletestBranch main

%define keep_archives true

Source0: git+https://github.com/google/benchmark.git?obj=%{benchmarkBranch}/%{benchmarkCommit}&export=benchmark-%{realversion}-%{benchmarkCommit}&module=benchmark-%{realversion}-%{benchmarkCommit}&output=/benchmark-%{realversion}-%{benchmarkCommit}.tgz
Source1: git+https://github.com/google/googletest.git?obj=%{googletestBranch}/%{googletestCommit}&export=googletest-%{realversion}-%{googletestCommit}&module=googletest-%{realversion}-%{googletestCommit}&output=/googletest-%{realversion}-%{googletestCommit}.tgz

%prep
%setup -T -b0 -n benchmark-%{realversion}-%{benchmarkCommit}
%setup -T -D -a1 -c -n benchmark-%{realversion}-%{benchmarkCommit}
mv googletest-%{realversion}-%{googletestCommit} googletest

%build
rm -rf %{_builddir}/build
mkdir -p %{_builddir}/build
cd %{_builddir}/build

cmake ../benchmark-%{realversion}-%{benchmarkCommit} \
  -G Ninja \
  -DCMAKE_INSTALL_PREFIX:PATH="%{i}" \
  -DCMAKE_CXX_FLAGS="-fPIE" \
  -DCMAKE_BUILD_TYPE:STRING=Release

ninja -v %{makeprocesses}

%install
cd ../build
ninja -v %{makeprocesses} install

%post
%{relocateConfig}lib64/pkgconfig/benchmark.pc
