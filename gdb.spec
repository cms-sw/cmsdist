### RPM external gdb 6.8
Source: http://ftp.gnu.org/gnu/%{n}/%{n}-%{realversion}.tar.bz2

%prep
%setup -n %n-%{realversion}

%build
./configure --prefix=%{i}
make %makeprocesses

%install
make install
mv %i/bin/gdb %i/bin/gdb-%{realversion}

# To save space, clean up some things that we don't really need
rm %i/lib/*
rm %i/bin/gdbserver
rm %i/bin/gdbtui

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<Tool name=gdb version=%v>
<Client>
 <Environment name=GDB_BASE default="%i"></Environment>
</Client>
<Runtime name=PATH value="$GDB_BASE/bin" type=path>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
