### RPM external libzmq 4.3.2
Source: https://github.com/zeromq/libzmq/releases/download/v%{realversion}/zeromq-%{realversion}.tar.gz
BuildRequires: autotools

%prep
%setup -n %{n}-%{realversion}

./configure --prefix=%{i} \
            --disable-doc \
            --disable-dependency-tracking

%build
make all %makeprocesses

%install
make install