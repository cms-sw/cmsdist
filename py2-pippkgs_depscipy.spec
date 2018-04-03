### RPM external py2-pippkgs_depscipy 3.0
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
Source: none
 
Requires: root curl python py2-pippkgs py2-numpy py2-matplotlib xrootd llvm hdf5

%define isslc7 %(case %{cmsplatf} in (slc7_amd64*) echo 1 ;; (*) echo 0 ;; esac)
%define isamd64 %(case %{cmsplatf} in (*amd64*) echo 1 ;; (*) echo 0 ;; esac)
BuildRequires: py2-scipy
BuildRequires: py2-Keras
BuildRequires: py2-Theano
BuildRequires: py2-scikit-learn
BuildRequires: py2-rootpy
BuildRequires: py2-tensorflow
BuildRequires: py2-googlecommon
BuildRequires: py2-protobuf

BuildRequires: py2-tables
BuildRequires: py2-numexpr
BuildRequires: py2-deepdish
BuildRequires: py2-histogrammar
BuildRequires: py2-pandas
BuildRequires: py2-root_numpy
BuildRequires: py2-bottleneck 
BuildRequires: py2-downhill 
BuildRequires: py2-theanets
BuildRequires: py2-xgboost
#BuildRequires: py2-llvmlite
#BuildRequires: py2-numba
BuildRequires: py2-hep_ml
BuildRequires: py2-rep
BuildRequires: py2-uncertainties
BuildRequires: py2-hyperas
BuildRequires: py2-hyperopt
BuildRequires: py2-seaborn
BuildRequires: py2-h5py
BuildRequires: py2-thriftpy
BuildRequires: py2-root_pandas
BuildRequires: py2-uproot
BuildRequires: py2-oamap

#this DOES NOT depend on numpy..
BuildRequires: py2-xrootdpyfs

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

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %{i}/etc/profile.d
: > %{i}/etc/profile.d/dependencies-setup.sh
: > %{i}/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test \$?$root != 0 || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done
