### RPM external python_tools 1.0
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}
Source: none
 
Requires: root curl python python3 xrootd llvm hdf5

%define isslc7 %(case %{cmsplatf} in (slc7_amd64*) echo 1 ;; (*) echo 0 ;; esac)
%define isamd64 %(case %{cmsplatf} in (*amd64*) echo 1 ;; (*) echo 0 ;; esac)
Requires: py2-scipy
Requires: py2-Keras
Requires: py2-Theano-toolfile
Requires: py2-scikit-learn
Requires: py2-rootpy-toolfile
Requires: py2-tensorflow-toolfile
Requires: py2-googlePackages

Requires: py2-tables-toolfile
Requires: py2-numexpr
Requires: py2-deepdish-toolfile
Requires: py2-histogrammar-toolfile
Requires: py2-pandas
Requires: py2-root_numpy
Requires: py2-bottleneck 
Requires: py2-downhill 
Requires: py2-theanets
Requires: py2-xgboost
#Requires: py2-llvmlite
#Requires: py2-numba
Requires: py2-hep_ml
Requires: py2-rep
Requires: py2-uncertainties
Requires: py2-hyperas
Requires: py2-hyperopt-toolfile
Requires: py2-seaborn
Requires: py2-h5py
Requires: py2-h5py-cache
Requires: py2-thriftpy
Requires: py2-root_pandas
Requires: py2-uproot
Requires: py2-oamap

#this DOES NOT depend on numpy..
Requires: py2-xrootdpyfs

Requires: root curl python openldap

Requires: py2-configparser 
Requires: py2-entrypoints
Requires: py2-psutil
Requires: py2-repozelru
Requires: py2-Jinja2
Requires: py2-MarkupSafe
Requires: py2-Pygments-toolfile
Requires: py2-appdirs
Requires: py2-argparse
Requires: py2-backports_abc
Requires: py2-backportsssl_match_hostname
Requires: py2-bleach
Requires: py2-certifi
Requires: py2-decorator
Requires: py2-html5lib
Requires: py2-ipykernel
Requires: py2-ipython-toolfile
Requires: py2-ipython_genutils
Requires: py2-ipywidgets
Requires: py2-jsonschema-toolfile
Requires: py2-send2trash
Requires: py2-jupyter
Requires: py2-jupyter_client-toolfile
Requires: py2-jupyter_console-toolfile
Requires: py2-jupyter_core-toolfile
Requires: py2-mistune
Requires: py2-nbconvert-toolfile
Requires: py2-nbformat-toolfile
Requires: py2-notebook-toolfile
Requires: py2-ordereddict
Requires: py2-packaging
Requires: py2-pandocfilters
Requires: py2-pathlib2
Requires: py2-pexpect
Requires: py2-pickleshare
Requires: py2-prompt_toolkit
Requires: py2-ptyprocess
Requires: py2-pyparsing
Requires: py2-pyzmq
Requires: py2-qtconsole-toolfile
Requires: py2-scandir
Requires: py2-setuptools-toolfile
Requires: py2-simplegeneric
Requires: py2-singledispatch
Requires: py2-six
Requires: py2-terminado
Requires: py2-testpath
Requires: py2-tornado
Requires: py2-traitlets
Requires: py2-wcwidth
Requires: py2-webencodings
Requires: py2-widgetsnbextension
Requires: py2-cycler
Requires: py2-docopt
Requires: py2-futures
Requires: py2-networkx
Requires: py2-parsimonious
Requires: py2-prettytable
Requires: py2-pycurl
Requires: py2-pytz
Requires: py2-requests
Requires: py2-schema
#Requires: py2-Jinja
Requires: py2-python-dateutil
Requires: py2-cjson
Requires: py2-enum34 
Requires: py2-shutil_get_terminal_size
Requires: py2-functools32
Requires: py2-mock
Requires: py2-pbr-toolfile
Requires: py2-mpmath
Requires: py2-sympy-toolfile
Requires: py2-tqdm-toolfile
Requires: py2-funcsigs
Requires: py2-nose-toolfile
Requires: py2-pkgconfig
Requires: py2-pysqlite
Requires: py2-click
Requires: py2-jsonpickle
Requires: py2-prwlock
Requires: py2-virtualenv-toolfile
Requires: py2-virtualenvwrapper-toolfile
Requires: py2-climate
Requires: py2-urllib3
Requires: py2-chardet-toolfile
Requires: py2-idna
Requires: py2-werkzeug
Requires: py2-pytest-toolfile
Requires: py2-avro-toolfile
Requires: py2-fs-toolfile
Requires: py2-lizard-toolfile
Requires: py2-flawfinder-toolfile
Requires: python-ldap
Requires: py2-plac-toolfile

Requires: py2-matplotlib
Requires: py2-numpy-toolfile
Requires: py2-sqlalchemy
Requires: py2-pygithub
Requires: py2-dablooms
Requires: py2-dxr-toolfile
Requires: py2-PyYAML
Requires: py2-lint-toolfile
Requires: py2-pip-toolfile
%if %isamd64
Requires: py2-cx-oracle
%endif
Requires: py2-cython-toolfile
Requires: py2-future
Requires: py2-backports_lzma
Requires: py2-pybind11-toolfile
Requires: py2-histbook
Requires: py2-flake8-toolfile
Requires: py2-autopep8-toolfile
Requires: py2-pycodestyle

%prep

%build

%install


