### RPM external libzmq 4.3.4
Source: https://github.com/zeromq/libzmq/releases/download/v%{realversion}/zeromq-%{realversion}.tar.gz
Source1: https://patch-diff.githubusercontent.com/raw/zeromq/libzmq/pull/4334.patch
BuildRequires: autotools

%prep
%setup -n zeromq-%{realversion}
patch -p1 < %{_sourcedir}/4334.patch

./configure --prefix=%{i} \
            --without-docs \
            --disable-dependency-tracking

%build
make all %makeprocesses

%install
make install
