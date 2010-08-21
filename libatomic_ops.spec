### RPM external libatomic_ops 7.2alpha4
Source: http://www.hpl.hp.com/research/linux/atomic_ops/download/%n-%realversion.tar.gz

%prep
%setup

%build
./configure --prefix=%i
make %makeprocesses

%install
make %makeprocesses install
