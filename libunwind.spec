### RPM external libunwind 1.3.1
%define tag 94aa304960927c130ecb5f664a642b32d9850688
%define branch v1.3-stable
Source0: git://github.com/%{n}/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
BuildRequires: autotools gmake

Patch0: libunwind-fix-comma

%prep
%setup -n %{n}-%{realversion}
%patch0 -p1

%build
autoreconf -fiv
./configure CFLAGS="-g -O3" --prefix=%{i} --disable-block-signals
make %{makeprocesses}

%install
make %{makeprocesses} install

%define drop_files %{i}/share/man
