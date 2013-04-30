### RPM external igprof 5.9.7

Source0: git://github.com/ktf/igprof.git?obj=master/v%{realversion}&export=igprof-%{realversion}&output=/igprof-%{realversion}.tgz
#Source0: git:%(pwd)/../igprof?obj=master/HEAD&export=igprof-%{realversion}&date=%(date +%s)&output=/igprof-HEAD.tgz
Requires: pcre
BuildRequires: cmake libunwind libatomic_ops
%prep
%setup -T -b 0 -n igprof-%{realversion}
%build
mkdir -p %i
rsync -av $LIBUNWIND_ROOT/ %i/
rsync -av $LIBATOMIC_OPS_ROOT/ %i/
cmake -DCMAKE_INSTALL_PREFIX=%i -DCMAKE_CXX_FLAGS_RELWITHDEBINFO="-I%i/include -I$PCRE_ROOT/include -g -O3" .
make %makeprocesses

%install
make %makeprocesses install
%define drop_files %i/share/man
