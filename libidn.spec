### RPM external libidn 1.32
Source: http://ftp.gnu.org/gnu/%n/%n-%realversion.tar.gz

%prep
%setup -n %n-%{realversion}

%build
./configure --prefix=%{i} --enable-static=no
make %makeprocesses

%install
make install

%define drop_files %i/share/{man,info,emacs,locale}
%define strip_files %i/lib
