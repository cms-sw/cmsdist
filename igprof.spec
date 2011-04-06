### RPM external igprof 5.9.0rc1
# ### RPM external libunwind 0.99.20100804
# ### RPM external libatomic_ops 7.2alpha4
Source0: http://www.hpl.hp.com/research/linux/atomic_ops/download/libatomic_ops-7.2alpha4.tar.gz
Source1: http://git.savannah.gnu.org/gitweb/?p=libunwind.git;a=snapshot;h=e2962af9d31266761700b431da894421c0d757ec;sf=tgz;dummy=/libunwind.tar.gz
Source2: http://igprof.git.sourceforge.net/git/gitweb.cgi?p=igprof/igprof;a=snapshot;h=1a5c2d05b8f74d15303e9a45a721733632f4398d;sf=tgz;dummy=/igprof.tar.gz
Patch0: libunwind-perf
Requires: cmake

%prep
%setup -T -b 0 -n libatomic_ops-7.2alpha4
%setup -D -T -b 1 -n libunwind-e2962af
%patch0 -p1
%setup -D -T -b 2 -n igprof-1a5c2d0

%build
cd ../libatomic_ops*
./configure --prefix=%i
make %makeprocesses install

cd ../libunwind*
autoreconf -i
./configure CFLAGS="-g -O3" CPPFLAGS="-I%i/include" --prefix=%i --disable-block-signals
make %makeprocesses install

cd ../igprof*
cmake -DCMAKE_INSTALL_PREFIX=%i -DCMAKE_CXX_FLAGS_RELWITHDEBINFO="-g -O3" .
make %makeprocesses

%install
make %makeprocesses install
