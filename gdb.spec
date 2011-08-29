### RPM external gdb 7.1
## BUILDIF case $(uname):$(uname -m) in Linux:i*86 | Linux:x86_64 | Darwin:* ) true ;; * ) false ;; esac 

Source: http://ftp.gnu.org/gnu/%{n}/%{n}-%{realversion}.tar.bz2
Requires: python
#Requires: expat

%prep
%setup -n %n-%{realversion}

%build
export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)
#./configure --prefix=%{i} --with-expat=$EXPAT_ROOT --with-python=$PYTHON_ROOT
./configure --prefix=%{i} --with-expat=no --with-python=$PYTHON_ROOT
make %makeprocesses

%install
make install

cd %i/bin/
ln -s gdb gdb-%{realversion}

# To save space, clean up some things that we don't really need 
rm -r %i/lib/* %i/bin/{gdbserver,gdbtui} %i/share/{man,info}
