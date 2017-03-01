### RPM external py2-pippkgs_depscipy 3.0
## INITENV +PATH PYTHONPATH %{i}/$PYTHON_LIB_SITE_PACKAGES
Source: none

Requires: root curl python py2-scipy py2-pippkgs

%define isslc7 %(case %{cmsplatf} in (slc7_amd64*) echo 1 ;; (*) echo 0 ;; esac)


BuildRequires: py2-Keras
BuildRequires: py2-Theano
BuildRequires: py2-scikit-learn
BuildRequires: py2-rootpy
%if %isslc7
BuildRequires: py2-tensorflow
%endif
BuildRequires: py2-protobuf

BuildRequires: py2-tables
BuildRequires: py2-numexpr
BuildRequires: py2-deepdish

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
        # https://github.com/jupyter/jupyter_core/issues/55 - now I delete jupyter.py from one of the providers
        #backports is an example directory that can have multiple packages inside
        if [ $f != "backports" ] ; then  
           echo "  Duplicate file found: $f"
           exit 1
        fi

      fi
    done
    echo "Copying $SOURCE in %{pkgrel}"
    rsync -av $SOURCE/ %{i}/$PYTHON_LIB_SITE_PACKAGES/
  fi
done

#and for bin
mkdir -p %{i}/bin
for pkg in %builddirectpkgreqs ; do
  SOURCE=%{cmsroot}/%{cmsplatf}/${pkg}/bin
  if [ -d $SOURCE ] ; then
    echo "Checking for duplicates ...."
    for f in $(ls $SOURCE) ; do
      if [ -e %{i}/bin/$f ] ; then 
           echo "  Duplicate file found: $f"
           exit 1
      fi
    done
    echo "Copying $SOURCE in %{pkgrel}"
    rsync -av $SOURCE/ %{i}/bin/
  fi
done

