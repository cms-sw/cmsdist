### RPM external jemalloc 4.5.0
Source: https://github.com/jemalloc/jemalloc/releases/download/%{realversion}/jemalloc-%{realversion}.tar.bz2

%prep
%setup -n %{n}-%{realversion}

%build
perl -p -i -e 's|-no-cpp-precomp||' configure
./configure --disable-stats --prefix %{i}

%define drop_files %{i}/share
