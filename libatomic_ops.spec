### RPM external libatomic_ops 7.2alpha4
Source0: http://www.hpl.hp.com/research/linux/atomic_ops/download/libatomic_ops-%{realversion}.tar.gz
%prep
%setup -b 0 -n libatomic_ops-7.2alpha4

%build
./configure --prefix=%i
make %makeprocesses install

%install
%define drop_files %i/share/man

