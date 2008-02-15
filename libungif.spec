### RPM external libungif 4.1.4-CMS19

Source: http://switch.dl.sourceforge.net/sourceforge/%{n}/%{n}-%{realversion}.tar.gz

%prep
%setup -n %n-%{realversion}

%build
./configure --prefix=%{i}
make %makeprocesses

%install
make install
perl -p -i -e "s|^#!.*perl|#!/usr/bin/env perl|" %{i}/bin/gifburst

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<info url="http://sourceforge.net/projects/libungif"></info>
<lib name=ungif>
<Client>
 <Environment name=LIBUNGIF_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$LIBUNGIF_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$LIBUNGIF_BASE/include"></Environment>
</Client>
<use name=libjpg>
<use name=zlib>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}lib/libungif.la
%{relocateConfig}etc/scram.d/%n
