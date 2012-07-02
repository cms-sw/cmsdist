### RPM external gdb 7.3.1
## BUILDIF case $(uname):$(uname -m) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) true ;; * ) false ;; esac
Source: http://ftp.gnu.org/gnu/%{n}/%{n}-%{realversion}.tar.bz2
Patch0: gdb-7.3.1-fix-pythonhome
Requires: python
#Requires: expat

%prep
%setup -n %n-%realversion
%patch0 -p1

%build
export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)
./configure --prefix=%{i} --with-expat=no --with-python=$PYTHON_ROOT LDFLAGS="-L$PYTHON_ROOT/lib"
make %makeprocesses

%install
make install

cd %i/bin/
ln -s gdb gdb-%{realversion}

# To save space, clean up some things that we don't really need 
%define drop_files %i/lib/* %i/bin/{gdbserver,gdbtui} %i/share/{man,info,locale}
