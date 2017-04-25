### RPM external py2-pippkgs 5.0
## INITENV +PATH PYTHONPATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
Source: none

Requires: root curl python

BuildRequires: py2-configparser 
BuildRequires: py2-entrypoints
BuildRequires: py2-psutil
BuildRequires: py2-repozelru
BuildRequires: py2-Jinja2
BuildRequires: py2-MarkupSafe
BuildRequires: py2-Pygments
BuildRequires: py2-appdirs
BuildRequires: py2-argparse
BuildRequires: py2-backports_abc
BuildRequires: py2-backportsssl_match_hostname
BuildRequires: py2-bleach
BuildRequires: py2-certifi
BuildRequires: py2-decorator
BuildRequires: py2-html5lib
BuildRequires: py2-ipykernel
BuildRequires: py2-ipython
BuildRequires: py2-ipython_genutils
BuildRequires: py2-ipywidgets
BuildRequires: py2-jsonschema
BuildRequires: py2-jupyter
BuildRequires: py2-jupyter_client
BuildRequires: py2-jupyter_console
BuildRequires: py2-jupyter_core
BuildRequires: py2-mistune
BuildRequires: py2-nbconvert
BuildRequires: py2-nbformat
BuildRequires: py2-notebook
BuildRequires: py2-ordereddict
BuildRequires: py2-packaging
BuildRequires: py2-pandocfilters
BuildRequires: py2-pathlib2
BuildRequires: py2-pexpect
BuildRequires: py2-pickleshare
BuildRequires: py2-prompt_toolkit
BuildRequires: py2-ptyprocess
BuildRequires: py2-pyparsing
BuildRequires: py2-pyzmq
BuildRequires: py2-qtconsole
BuildRequires: py2-scandir
BuildRequires: py2-setuptools
BuildRequires: py2-simplegeneric
BuildRequires: py2-singledispatch
BuildRequires: py2-six
BuildRequires: py2-terminado
BuildRequires: py2-testpath
BuildRequires: py2-tornado
BuildRequires: py2-traitlets
BuildRequires: py2-wcwidth
BuildRequires: py2-webencodings
BuildRequires: py2-widgetsnbextension
BuildRequires: py2-cycler
BuildRequires: py2-docopt
BuildRequires: py2-futures
BuildRequires: py2-networkx
BuildRequires: py2-parsimonious
BuildRequires: py2-prettytable
BuildRequires: py2-pycurl
BuildRequires: py2-pytz
BuildRequires: py2-requests
BuildRequires: py2-schema
BuildRequires: py2-Jinja
BuildRequires: py2-python-dateutil
BuildRequires: py2-cjson
BuildRequires: py2-enum34
BuildRequires: py2-shutil_get_terminal_size
BuildRequires: py2-functools32
BuildRequires: py2-mock
BuildRequires: py2-pbr
BuildRequires: py2-mpmath
BuildRequires: py2-sympy
BuildRequires: py2-tqdm
BuildRequires: py2-funcsigs
BuildRequires: py2-nose
BuildRequires: py2-pkgconfig
BuildRequires: py2-pysqlite
BuildRequires: py2-click
BuildRequires: py2-jsonpickle

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
           echo "  Duplicate file found: $f"
           exit 1
        fi

      fi
    done
    echo "Copying $SOURCE in %{pkgrel}"
    rsync -av $SOURCE/ %{i}/${PYTHON_LIB_SITE_PACKAGES}/
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

