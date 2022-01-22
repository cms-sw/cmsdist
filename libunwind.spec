### RPM external libunwind 1.6.2
%define tag b3ca1b59a795a617877c01fe5d299ab7a07ff29d
%define branch v1.6-stable
Source0: git://github.com/%{n}/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
BuildRequires: autotools gmake
Requires: zlib

%prep
%setup -n %{n}-%{realversion}

%build
autoreconf -fiv
./configure CFLAGS="-g -O3 -fcommon" --prefix=%{i} --disable-block-signals --enable-zlibdebuginfo
make %{makeprocesses}

%install

make %{makeprocesses} install
[ -d %{i}/lib64 ] && mv %{i}/lib64 %{i}/lib
%define drop_files %{i}/share/man %{i}/lib/pkgconfig %{i}/lib/*.a