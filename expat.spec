### RPM external expat 2.1.0
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib64
Source: http://downloads.sourceforge.net/project/%{n}/%{n}/%{realversion}/%{n}-%{realversion}.tar.gz

%define drop_files %{i}/share

%prep
%setup -n %{n}-%{realversion}

%build
# Update to detect aarch64 and ppc64le
rm -f ./conftools/config.{sub,guess}
curl -L -k -s -o ./conftools/config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./conftools/config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./conftools/config.{sub,guess}

./configure --prefix=%{i} 
make %{makeprocesses}

%install
make install
# bla bla
