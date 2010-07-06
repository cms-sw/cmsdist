### RPM external gdbm 1.8.3
Source: http://ftp.download-by.net/gnu/gnu/%{n}/%{n}-%{realversion}.tar.gz

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
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n.xml
  <tool name="%n" version="%v">
    <lib name="gdbm"/>
    <client>
      <environment name="GDBM_BASE" default="%i"/>
      <environment name="LIBDIR" default="$GDBM_BASE/lib"/>
      <environment name="INCLUDE" default="$GDBM_BASE/include"/>
    </client>
  </tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n.xml
