### RPM external igprof 5.9.2
# ### RPM external libunwind 0.99.20100804
# ### RPM external libatomic_ops 7.2alpha4
Source0: http://www.hpl.hp.com/research/linux/atomic_ops/download/libatomic_ops-7.2alpha4.tar.gz
Source1: http://git.savannah.gnu.org/gitweb/?p=libunwind.git;a=snapshot;h=5c2cade264010c9855c4ea5effc5b4789739e7ca;sf=tgz;dummy=/libunwind.tar.gz
Source2: http://downloads.sourceforge.net/igprof/igprof-%{realversion}.tar.gz
Requires: cmake

%prep
%setup -T -b 0 -n libatomic_ops-7.2alpha4
%setup -D -T -b 1 -n libunwind-5c2cade
%setup -D -T -b 2 -n igprof-%{realversion}

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
