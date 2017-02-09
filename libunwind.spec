### RPM external libunwind 1.2
%define tag 5f354cb7b9c84dae006f0ebd8ad7a78d7e2aad0c
%define branch v1.2-stable
Source: git+https://git0.savannah.gnu.org/r/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
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
