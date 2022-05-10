### RPM external libunwind 1.6.2
%define tag e44877a4545d55332a9358f8b9e3468f5c1782f7
%define branch v1.6-stable
Source0: git://github.com/%{n}/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
Patch0: libunwind-dwarf
BuildRequires: autotools gmake
Requires: zlib

%prep
%setup -n %{n}-%{realversion}
%patch0 -p1

%build
autoreconf -fiv
./configure CFLAGS="-g -O3 -fcommon" --prefix=%{i} --disable-block-signals --enable-zlibdebuginfo
make %{makeprocesses}

%install

make %{makeprocesses} install
[ -d %{i}/lib64 ] && mv %{i}/lib64 %{i}/lib
%define drop_files %{i}/share/man %{i}/lib/pkgconfig %{i}/lib/*.a
