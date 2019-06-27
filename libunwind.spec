### RPM external libunwind 1.2.1
%define tag a77b0cd7bd14c27ff7c18463f432599ce9469c75
%define branch v1.2-stable
Source0: git://github.com/%{n}/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
Requires: libatomic_ops
BuildRequires: autotools

Patch0: libunwind-fix-comma

%prep
%setup -n %{n}-%{realversion}
%patch0 -p1

%build
autoreconf -fiv
./configure CFLAGS="-g -O3" CPPFLAGS="-I${LIBATOMIC_OPS_ROOT}/include" --prefix=%{i} --disable-block-signals
make %{makeprocesses}

%install
make %{makeprocesses} install

%define drop_files %{i}/share/man
# bla bla
