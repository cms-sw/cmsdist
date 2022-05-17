### RPM external libzmq 4.3.4
Source: https://github.com/zeromq/libzmq/releases/download/v%{realversion}/zeromq-%{realversion}.tar.gz
BuildRequires: autotools

%prep
%setup -n zeromq-%{realversion}

./configure --prefix=%{i} \
            --without-docs \
            --disable-dependency-tracking

%build
make all %makeprocesses

%install
make install
