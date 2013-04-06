### RPM external cvs2git 5419
Source: svn://cvs2svn.tigris.org/svn/cvs2svn/trunk?scheme=http&revision=%realversion&module=cvs2git-%realversion&output=/cvs2git-%realversion.tgz
Requires: python

%prep
%setup -n %n-%realversion
%build
./setup.py build
%install
mkdir -p %i
mv build/lib %i/lib
mv build/script* %i/bin
