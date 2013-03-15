### RPM external libunwind 1.1
Source0: http://download.savannah.gnu.org/releases/%{n}/%{n}-%{realversion}.tar.gz
Requires: libatomic_ops

%prep
%setup -n %{n}-%{realversion}

%build
./configure CFLAGS="-g -O3" CPPFLAGS="-I${LIBATOMIC_OPS_ROOT}/include" --prefix=%{i} --disable-block-signals
make %{makeprocesses}

%install
make %{makeprocesses} install

%define drop_files %{i}/share/man
