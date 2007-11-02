### RPM external gdbm 1.8.3-CMS18
Source: http://rm.mirror.garr.it/mirrors/gnuftp/gnu/%{n}/%{n}-%{realversion}.tar.gz

%define thisuser %(id -u)
%define thisgroup %(id -g)

%prep
%setup -n %n-%{realversion}

%build
perl -p -i -e "s|BINOWN = bin|BINOWN = %{thisuser}|g" Makefile.in
perl -p -i -e "s|BINGRP = bin|BINGRP = %{thisgroup}|g" Makefile.in
./configure --prefix=%{i}
make %makeprocesses

%install
make install

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<Lib name=gdbm>
<Client>
 <Environment name=GDBM_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$GDBM_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$GDBM_BASE/include"></Environment>
</Client>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
