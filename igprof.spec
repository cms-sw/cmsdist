### RPM external igprof 5.9.16
%define git_repo igprof
%define git_user cms-externals
%define git_branch cms/master/c6882f4
%define git_commit 4235186fd1a9b9adb86a8a45bb7a8ece74953039
Source0: git://github.com/%{git_user}/igprof.git?obj=%{git_branch}/%{git_commit}&export=igprof-%{git_commit}&output=/igprof-%{git_commit}.tgz
Patch0: igprof-gcc8
Requires: pcre
BuildRequires: cmake libunwind libatomic_ops
%prep
%setup -T -b 0 -n igprof-%{git_commit}
%patch0 -p1

%build
mkdir -p %i
rsync -av $LIBUNWIND_ROOT/ %i/
rsync -av $LIBATOMIC_OPS_ROOT/ %i/
cmake -DCMAKE_INSTALL_PREFIX=%i -DCMAKE_VERBOSE_MAKEFILE=TRUE -DPCRE_INCLUDE_DIR=$PCRE_ROOT/include -DPCRE_LIBRARY=$PCRE_ROOT/lib/libpcre.so -DCMAKE_CXX_FLAGS_RELWITHDEBINFO="-I%i/include -I$PCRE_ROOT/include -g -O3" .
make %makeprocesses

%install
make %makeprocesses install
%define drop_files %i/share/man
