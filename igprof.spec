### RPM external igprof 5.7.0
# ### RPM external libunwind 0.99.20100804
# ### RPM external libatomic_ops 7.2alpha4
Source0: http://www.hpl.hp.com/research/linux/atomic_ops/download/libatomic_ops-7.2alpha4.tar.gz
Source1: http://git.savannah.gnu.org/gitweb/?p=libunwind.git;a=snapshot;h=982d590ddb778f0d301fe2e5647abd9135a2f9bc;sf=tgz;dummy=/libunwind.tar.gz
Source2: http://igprof.git.sourceforge.net/git/gitweb.cgi?p=igprof/igprof;a=snapshot;h=fa30019d9c4dee5f4f710b33a4c5a998eb10f3e8;sf=tgz;dummy=/igprof.tar.gz
Patch0: libunwind-mincore
Patch1: libunwind-trace
Requires: cmake

%prep
%setup -T -b 0 -n libatomic_ops-7.2alpha4
%setup -D -T -b 1 -n libunwind-982d590
%patch0 -p1
%patch1 -p1
%setup -D -T -b 2 -n igprof-fa30019

%build
cd ../libatomic_ops*
./configure --prefix=%i
make %makeprocesses install

cd ../libunwind*
autoreconf -i
./configure CPPFLAGS="-I%i/include" --prefix=%i --disable-block-signals
make %makeprocesses install

cd ../igprof*
cmake -DCMAKE_INSTALL_PREFIX=%i .
make %makeprocesses

%install
make %makeprocesses install
