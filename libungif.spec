### RPM external libungif 4.1.4
Source: http://switch.dl.sourceforge.net/sourceforge/%{n}/%{n}-%{v}.tar.gz

%build
./configure --prefix=%{i}
make %makeprocesses
