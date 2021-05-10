### RPM external libunwind 1.5
%define tag 4c980e2b29cdb9d21cfc341abdec3a6ee46e0483
%define branch v1.5-stable
Source0: git://github.com/%{n}/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
BuildRequires: autotools gmake
Requires: zlib

Patch0: libunwind-fix-comma

%prep
%setup -n %{n}-%{realversion}
%patch0 -p1

%build
autoreconf -fiv
./configure CFLAGS="-g -O3 -fcommon" --prefix=%{i} --libdir=%{i}/lib --disable-block-signals --enable-zlibdebuginfo
make %{makeprocesses}

%install
make %{makeprocesses} install

%define drop_files %{i}/share/man %{i}/lib/pkgconfig %{i}/lib/*.a
