### RPM external expat 2.0.0-CMS18
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib64
Source: http://dl.sourceforge.net/sourceforge/%n/%n-%realversion.tar.gz
Provides: libc.so.6()(64bit)
Provides: libc.so.6(GLIBC_2.2.5)(64bit)  
%define _ldd ldd
%if "%(uname)" == "Darwin"
%define _ldd otool -L
%endif

%prep
%setup -n %n-%{realversion}

%build
./configure --prefix=%{i} 
make 
make install

%if "%(%_ldd /usr/bin/gcc | xargs | grep lib64)" != ""
make clean
echo "64 bit compiler found let's build expat in 64 bit to be used by scram perl modules." 
export PATH=/usr/bin:/bin
export GCC_EXEC_PREFIX=/usr/lib/gcc/

CXX=/usr/bin/c++ CC=/usr/bin/gcc setarch x86_64 ./configure --prefix=%{i} --bindir=%{i}/bin/64 --libdir=%{i}/lib64
setarch x86_64 make
setarch x86_64 make install
%endif
%install
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<Lib name=expat>
<Client>
 <Environment name=EXPAT_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$EXPAT_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$EXPAT_BASE/include"></Environment>
 <Environment name=BINDIR default="$EXPAT_BASE/bin"></Environment>
</Client>
<Runtime name=PATH value="$BINDIR" type=path>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
%{relocateConfig}lib/libexpat.la
