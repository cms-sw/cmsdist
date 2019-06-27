### RPM external libxslt 1.1.28

%define tag 195f644cf7b5e93208b033fa7c5501c41cf82f59
%define branch master
%define github_user cms-externals
Source0: git+https://github.com/%github_user/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

Requires: libxml2 python
BuildRequires: autotools
%prep
%setup -n %{n}-%{realversion}

%build
./autogen.sh \
  --prefix=%{i} \
  --with-libxml-prefix=$LIBXML2_ROOT \
  --with-libxml-include-prefix=$LIBXML2_ROOT/include \
  --with-libxml-libs-prefix=$LIBXML2_ROOT/lib \
  --without-crypto
make

%install
make install

%post
%{relocateConfig}bin/xslt-config
# bla bla
