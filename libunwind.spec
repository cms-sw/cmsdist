### RPM external libunwind 1.1
%define tag 01caf2895fb52f241d1efb42752082aa8864492e
%define branch cms/65ac867
%define github_user cms-externals
Source: git+https://github.com/%github_user/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
Requires: libatomic_ops
BuildRequires: autotools

%prep
%setup -n %{n}-%{realversion}

%build
autoreconf -fiv
./configure CFLAGS="-g -O3" CPPFLAGS="-I${LIBATOMIC_OPS_ROOT}/include" --prefix=%{i} --disable-block-signals
make %{makeprocesses}

%install
make %{makeprocesses} install

%define drop_files %{i}/share/man
