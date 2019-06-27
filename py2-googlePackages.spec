### RPM external py2-googlePackages 1.0
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}
Source: none

Requires: python python3
BuildRequires: py2-google-common
BuildRequires: py2-protobuf

%prep

%build
 
%install

mkdir -p %{i}/${PYTHON_LIB_SITE_PACKAGES}
for pkg in %builddirectpkgreqs ; do
  SOURCE=%{cmsroot}/%{cmsplatf}/${pkg}/${PYTHON_LIB_SITE_PACKAGES}
  if [ -d $SOURCE ] ; then
    echo "Checking for duplicates ...."
    for f in $(ls $SOURCE) ; do
      if [ -e %{i}/${PYTHON_LIB_SITE_PACKAGES}/$f ] ; then 
        # https://github.com/jupyter/jupyter_core/issues/55 - now I delete jupyter.py from one of the providers
        #backports is an example directory that can have multiple packages inside
        if [ $f != "backports" ] ; then  
        if [ $f != "google" ] ; then  
           echo "  Duplicate file found: $f"
           exit 1
        fi
        fi

      fi
    done
    echo "Copying $SOURCE in %{pkgrel}"
#try cp instead of rsync as we don't want to overwrite duplicate directories
#    rsync -av $SOURCE/ %{i}/${PYTHON_LIB_SITE_PACKAGES}/
    cp -r ${SOURCE}/* %{i}/${PYTHON_LIB_SITE_PACKAGES}/ 
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

mkdir -p %{i}/${PYTHON3_LIB_SITE_PACKAGES}
for pkg in %builddirectpkgreqs ; do
  SOURCE=%{cmsroot}/%{cmsplatf}/${pkg}/${PYTHON3_LIB_SITE_PACKAGES}
  if [ -d $SOURCE ] ; then
    echo "Checking for duplicates ...."
    for f in $(ls $SOURCE) ; do
      if [ -e %{i}/${PYTHON3_LIB_SITE_PACKAGES}/$f ] ; then 
        # https://github.com/jupyter/jupyter_core/issues/55 - now I delete jupyter.py from one of the providers
        #backports is an example directory that can have multiple packages inside
        if [ $f != "backports" ] ; then  
        if [ $f != "google" ] ; then  
           echo "  Duplicate file found: $f"
           exit 1
        fi
        fi

      fi
    done
    echo "Copying $SOURCE in %{pkgrel}"
#try cp instead of rsync as we don't want to overwrite duplicate directories
#    rsync -av $SOURCE/ %{i}/${PYTHON_LIB_SITE_PACKAGES}/
    cp -r ${SOURCE}/* %{i}/${PYTHON3_LIB_SITE_PACKAGES}/ 
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

# bla bla
