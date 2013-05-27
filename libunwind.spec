### RPM external libunwind 1.0.1
Source0: http://download.savannah.gnu.org/releases/libunwind/libunwind-%{realversion}.tar.gz
Requires: libatomic_ops

%prep
%setup -n libunwind-%{realversion}

%build
./configure CFLAGS="-g -O3" CPPFLAGS="-I$LIBATOMIC_OPS_ROOT/include" --prefix=%i --disable-block-signals
make %makeprocesses install

%install
make %makeprocesses install
%define drop_files %i/share/man

