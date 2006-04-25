### RPM external libungif 4.1.4
Source: http://switch.dl.sourceforge.net/sourceforge/%{n}/%{n}-%{v}.tar.gz

%build
./configure --prefix=%{i}
make %makeprocesses
%install
make install
perl -p -i -e "s|^#!.*perl|#!/usr/bin/env perl|" %{i}/bin/gifburst
