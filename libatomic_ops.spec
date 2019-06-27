### RPM external libatomic_ops 7.4.0
Source0: http://www.hpl.hp.com/research/linux/atomic_ops/download/%{n}-%{realversion}.tar.gz
%prep
%setup -b 0 -n %{n}-%{realversion}

%build
./configure --prefix=%{i}
make %{makeprocesses} install

%install
%define drop_files %{i}/share/man
# bla bla
