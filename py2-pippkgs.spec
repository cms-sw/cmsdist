### RPM external py2-pippkgs 1.0
## INITENV +PATH PYTHONPATH %{i}/$PYTHON_LIB_SITE_PACKAGES
Source: none

BuildRequires: py2-rootpy
BuildRequires: py2-configparser 
BuildRequires: py2-entrypoints

%prep

%build
 
%install
mkdir -p %{i}/$PYTHON_LIB_SITE_PACKAGES
for pkg in %builddirectpkgreqs ; do
  SOURCE=%{cmsroot}/%{cmsplatf}/${pkg}/$PYTHON_LIB_SITE_PACKAGES
  if [ -d $SOURCE ] ; then
    echo "Checking for duplicates ...."
    for f in $(ls $SOURCE) ; do
      if [ -e %{i}/$PYTHON_LIB_SITE_PACKAGES/$f ] ; then
        echo "  Duplicate file found: $f"
        exit 1
      fi
    done
    echo "Copying $SOURCE in %{pkgrel}"
    rsync -av $SOURCE/ %{i}/$PYTHON_LIB_SITE_PACKAGES/
  fi
done

