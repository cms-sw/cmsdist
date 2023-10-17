### RPM external libunwind 1.7.2-master
%define tag 24947191d61dda869e039e0414fe97e9f594acd5
%define branch master
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
