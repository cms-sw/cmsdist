### RPM external libzmq 4.3.5-5bf04ee
%define branch master
%define tag 5bf04ee2ff207f0eaf34298658fe354ea61e1839
Source: git+https://github.com/zeromq/libzmq.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
BuildRequires: autotools

%prep
%setup -n %{n}-%{realversion}

./autogen.sh

./configure --prefix=%{i} \
            --without-docs \
            --disable-dependency-tracking

%build
make all %makeprocesses

%install
make install
