### RPM external py2-dxr master
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
BuildRequires: llvm sqlite
Requires: python py2-setuptools py2-futures py2-jinja py2-markupsafe py2-ordereddict py2-parsimonious

%define dxrCommit 6ea764102a
%define triliteCommit e64a2a1 
%define branch master
%define github_user mozilla

Source0: git+https://github.com/%github_user/dxr.git?obj=%{branch}/%{dxrCommit}&export=dxr-%{realversion}-%{dxrCommit}&module=dxr-%realversion-%dxrCommit&output=/dxr-%{realversion}-%{dxrCommit}.tgz
Source1: git+https://github.com/jonasfj/trilite.git?obj=%{branch}/%{triliteCommit}&export=trilite-%{realversion}-%{triliteCommit}&module=trilite-%realversion-%triliteCommit&output=/trilite-%{realversion}-%{triliteCommit}.tgz

%define keep_archives true

%prep
%setup -T -b0 -n dxr-%realversion-%dxrCommit
%setup -T -D -a1 -c -n dxr-%realversion-%dxrCommit
mv trilite-%realversion-%triliteCommit/* trilite
%setup -T -D -n dxr-%realversion-%dxrCommit

%build
make build-plugin-clang build-plugin-pygmentize trilite ; python setup.py build

%install
mkdir %i/lib
cp -p trilite/libtrilite.so %i/lib
python setup.py install --prefix=%i  --single-version-externally-managed --record=/dev/null
