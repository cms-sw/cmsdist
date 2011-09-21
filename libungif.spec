### RPM external libungif 4.1.4

Source: http://switch.dl.sourceforge.net/sourceforge/giflib/%{n}-%{realversion}.tar.gz

%prep
%setup -n %n-%{realversion}

%build
./configure --prefix=%{i} --disable-static
make %makeprocesses

%install
make install
# Strip libraries, we are not going to debug them.
%define strip_files %i/{lib,bin}
perl -p -i -e "s|^#!.*perl|#!/usr/bin/env perl|" %{i}/bin/gifburst
