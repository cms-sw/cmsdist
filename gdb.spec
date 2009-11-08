### RPM external gdb 7.0
## BUILDIF case $(uname):$(uname -p) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) false ;; esac 

Source: http://ftp.gnu.org/gnu/%{n}/%{n}-%{realversion}.tar.bz2
Requires: python

%prep
%setup -n %n-%{realversion}

%build
export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)
#./configure --prefix=%{i} --with-expat=no --with-python=yes --with-python-lib=$PYTHON_ROOT/lib --with-python-include=$PYTHON_ROOT/include/python${PYTHONV}
./configure --prefix=%{i} --with-expat=no --with-python=$PYTHON_ROOT
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
