### RPM external zlib 1.2.8

%define git_repo davidlt
%define git_branch gcc.amd64
%define git_commit 9940c55156d21253f44acaa108614261753d2ead
Source0: git://github.com/%{git_repo}/%{n}.git?obj=%{git_branch}/%{git_commit}&export=%{n}-%{git_commit}&output=/%{n}-%{git_commit}.tgz

%prep
%setup -n %{n}-%{git_commit}

%build
%if "%{cmscompiler}" == "icc"
%define cfgopts CC="icc -fPIC"
%else
%define cfgopts %{nil}
%endif

case %{cmsplatf} in
   *_amd64_*|*_mic_*)
     CFLAGS="-fPIC -O3 -DUSE_MMAP -DUNALIGNED_OK -D_LARGEFILE64_SOURCE=1 -msse3" \
     ./configure --prefix=%{i}
     ;;
   *_armv7hl_*|*_aarch64_*|*_ppc64le_*)
     CFLAGS="-fPIC -O3 -DUSE_MMAP -DUNALIGNED_OK -D_LARGEFILE64_SOURCE=1" \
     ./configure --prefix=%{i}
     ;;
   *)
     %{cfgopts} ./configure --prefix=%{i}
     ;;
esac

make %{makeprocesses}

# Strip libraries, we are not going to debug them.
%define strip_files %{i}/lib
# Look up documentation online.
%define drop_files %{i}/share
