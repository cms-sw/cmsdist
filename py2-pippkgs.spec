### RPM external py2-pippkgs 2.0
## INITENV +PATH PYTHONPATH %{i}/$PYTHON_LIB_SITE_PACKAGES
Source: none

BuildRequires: py2-rootpy
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

