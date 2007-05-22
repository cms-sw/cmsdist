### RPM external libungif 4.1.4-XXXX

Source: http://switch.dl.sourceforge.net/sourceforge/%{n}/%{n}-%{realversion}.tar.gz

%prep
%setup -n %n-%{realversion}

%build
./configure --prefix=%{i}
make %makeprocesses
%install
make install
perl -p -i -e "s|^#!.*perl|#!/usr/bin/env perl|" %{i}/bin/gifburst
