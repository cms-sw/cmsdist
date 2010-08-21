### RPM external libunwind 0.99.20100804
Source: http://git.savannah.gnu.org/gitweb/?p=libunwind.git;a=snapshot;h=982d590ddb778f0d301fe2e5647abd9135a2f9bc;sf=tgz
Patch0: libunwind-mincore
Patch1: libunwind-trace
Requires: libatomic_ops

%prep
%setup -n %n-982d590
%patch0 -p1
%patch1 -p1

%build
./configure --prefix=%i --disable-block-signals
make %makeprocesses

%install
make %makeprocesses install
