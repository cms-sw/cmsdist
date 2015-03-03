### RPM external igprof 5.9.14

%define git_repo igprof
%define git_branch master
%define git_commit cbb14bd326
Source0: git://github.com/%{git_repo}/igprof.git?obj=%{git_branch}/%{git_commit}&export=igprof-%{git_commit}&output=/igprof-%{git_commit}.tgz
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
