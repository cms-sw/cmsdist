### RPM external igprof 5.9.16
%define git_repo igprof
%define git_user cms-externals
%define git_branch cms/master/c6882f4
%define git_commit 67f31868ae84f4ec0f3362ee93e3cf89d51f0a07
Source0: git://github.com/%{git_user}/igprof.git?obj=%{git_branch}/%{git_commit}&export=igprof-%{git_commit}&output=/igprof-%{git_commit}.tgz
Patch0: igprof-gcc12
Requires: pcre libunwind
BuildRequires: cmake
%prep
%setup -T -b 0 -n igprof-%{git_commit}
%patch0 -p1

%build
mkdir -p %i
rm -rf ../build; mkdir ../build; cd ../build

cmake ../igprof-%{git_commit} \
   -DCMAKE_INSTALL_PREFIX=%i -DCMAKE_VERBOSE_MAKEFILE=TRUE \
   -DCMAKE_CXX_FLAGS_RELWITHDEBINFO="-g -O3 -Wno-error=deprecated-declarations" \
   -DCMAKE_PREFIX_PATH="$LIBUNWIND_ROOT;$PCRE_ROOT"
make DEBUG=1 VERBOSE=1 %makeprocesses

%install
cd ../build
make %makeprocesses install
%define drop_files %i/share/man
