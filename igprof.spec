### RPM external igprof 5.9.10

%define git_repo ktf
%define git_branch master
%define git_commit d2392737fb612669458e2210564a87782f0dbbbd
Source0: git://github.com/ktf/igprof.git?obj=%{git_branch}/%{git_commit}&export=igprof-%{git_commit}&output=/igprof-%{git_commit}.tgz
#Source0: git:/build/eulisse/ext/CMSSW_7_0_X/20131011_1816/igprof/.git?obj=master/%{git_commit}&export=igprof-%{git_commit}&output=/igprof-%{git_commit}.tgz
Requires: pcre
BuildRequires: cmake libunwind libatomic_ops
%prep
%setup -T -b 0 -n igprof-%{git_commit}
%build
mkdir -p %i
rsync -av $LIBUNWIND_ROOT/ %i/
rsync -av $LIBATOMIC_OPS_ROOT/ %i/
cmake -DCMAKE_INSTALL_PREFIX=%i -DPCRE_INCLUDE_DIR=$PCRE_ROOT/include -DPCRE_LIBRARY=$PCRE_ROOT/lib/libpcre.so -DCMAKE_CXX_FLAGS_RELWITHDEBINFO="-I%i/include -I$PCRE_ROOT/include -g -O3" .
make %makeprocesses

%install
make %makeprocesses install
%define drop_files %i/share/man
