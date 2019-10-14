### RPM external zlib 1.2.11
%define git_repo cms-externals
%define git_branch cms/v1.2.11
%define git_commit 822f7f5a8c57802faf8bbfe16266be02eff8c2e2
Source0: git://github.com/%{git_repo}/zlib.git?obj=%{git_branch}/%{git_commit}&export=zlib-%{realversion}&output=/zlib-%{realversion}.tgz

%prep
%setup -n zlib-%{realversion}

%build

case %{cmsplatf} in
   *_amd64_*|*_mic_*)
     CFLAGS="-fPIC -O3 -DUSE_MMAP -DUNALIGNED_OK -D_LARGEFILE64_SOURCE=1 -msse3" \
     ./configure --prefix=%{i}
     ;;
   *_armv7hl_*|*_aarch64_*|*_ppc64le_*|*_ppc64_*)
     CFLAGS="-fPIC -O3 -DUSE_MMAP -DUNALIGNED_OK -D_LARGEFILE64_SOURCE=1" \
     ./configure --prefix=%{i}
     ;;
   *)
     ./configure --prefix=%{i}
     ;;
esac

make %{makeprocesses}

# Strip libraries, we are not going to debug them.
%define strip_files %{i}/lib
# Look up documentation online.
%define drop_files %{i}/share
