### RPM external libxslt 1.1.26

%define tag 2818aec36119907206bab050811e4ec8347ffa40
%define branch master
%define github_user cms-externals
Source0: git+https://github.com/%github_user/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

Requires: libxml2
BuildRequires: autotools
%prep
%setup -n %{n}-%{realversion}

%build
./autogen.sh --prefix=%{i} --with-libxml-prefix=$LIBXML2_ROOT --with-libxml-include-prefix=$LIBXML2_ROOT/include  --with-libxml-libs-prefix=$LIBXML2_ROOT/lib
make

%install
make install
