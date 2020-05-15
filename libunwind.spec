### RPM external libunwind 1.4.0
%define tag 9a055a43bfc955658f88d21cf66386bfdd982c94
%define branch v1.4-stable
Source0: git://github.com/%{n}/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
BuildRequires: autotools gmake

Patch0: libunwind-fix-comma

%prep
%setup -n %{n}-%{realversion}
%patch0 -p1

%build
autoreconf -fiv
./configure CFLAGS="-g -O3 -fcommon" --prefix=%{i} --disable-block-signals
make %{makeprocesses}

%install
make %{makeprocesses} install

%define drop_files %{i}/share/man
