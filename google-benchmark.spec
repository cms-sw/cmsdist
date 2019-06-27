### RPM external google-benchmark 1.4.x

BuildRequires: cmake ninja

%define benchmarkCommit 7d03f2df490c89b2a2055e9be4e2c36db5aedd80
%define benchmarkBranch master
%define googletestCommit ba96d0b1161f540656efdaed035b3c062b60e006
%define googletestBranch master

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
  -DCMAKE_BUILD_TYPE:STRING=Release

ninja -v %{makeprocesses} -l $(getconf _NPROCESSORS_ONLN)

%install
cd ../build
ninja -v %{makeprocesses} -l $(getconf _NPROCESSORS_ONLN) install

# bla bla
