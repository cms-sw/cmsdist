### RPM external python_tools 2.0
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}
Source: none
 
Requires: root curl python python3 xrootd llvm hdf5

%define isslc7 %(case %{cmsplatf} in (slc7_amd64*) echo 1 ;; (*) echo 0 ;; esac)
%define isamd64 %(case %{cmsplatf} in (*amd64*) echo 1 ;; (*) echo 0 ;; esac)
Requires: py2-scipy
Requires: py2-Keras
Requires: py2-Theano
Requires: py2-scikit-learn
Requires: py3-rootpy
Requires: py2-tensorflow py3-tensorflow
Requires: py2-googlePackages

Requires: py2-cloudpickle
Requires: py2-tables
Requires: py3-tables
Requires: py2-numexpr
Requires: py2-histogrammar py3-histogrammar
Requires: py2-pandas
Requires: py3-root_numpy
Requires: py2-Bottleneck
Requires: py2-downhill 
Requires: py2-theanets
Requires: py2-xgboost
Requires: py2-llvmlite
Requires: py2-numba
Requires: py2-hep_ml
Requires: py2-rep
Requires: py2-uncertainties
Requires: py2-hyperas
Requires: py2-hyperopt
Requires: py2-seaborn
Requires: py2-h5py
Requires: py2-h5py-cache
Requires: py2-thriftpy
Requires: py3-root_pandas
Requires: py2-uproot
Requires: py2-oamap

#this DOES NOT depend on numpy..
Requires: py2-xrootdpyfs

Requires: root curl python openldap

Requires: py2-entrypoints
Requires: py2-psutil
Requires: py2-repoze-lru
Requires: py2-Jinja2
Requires: py2-MarkupSafe
Requires: py2-Pygments
Requires: py2-appdirs
Requires: py2-argparse
Requires: py2-bleach
Requires: py2-certifi
Requires: py2-decorator
Requires: py2-html5lib
Requires: py2-ipykernel
Requires: py2-ipython
Requires: py2-ipython_genutils
Requires: py2-ipywidgets
Requires: py2-jsonschema
Requires: py2-jupyter
Requires: py2-jupyter_client
Requires: py2-jupyter_console
Requires: py2-jupyter_core
Requires: py2-mistune
Requires: py2-nbconvert
Requires: py2-nbformat
Requires: py2-notebook
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
Requires: py2-qtconsole
Requires: py2-scandir
Requires: py2-setuptools
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
Requires: py2-python-cjson
Requires: py2-enum34 
Requires: py2-functools32
Requires: py2-mock
Requires: py2-pbr
Requires: py2-mpmath
Requires: py2-sympy
Requires: py2-tqdm
Requires: py2-funcsigs
Requires: py2-nose
Requires: py2-pkgconfig
Requires: py2-pysqlite
Requires: py2-Click
Requires: py2-jsonpickle
Requires: py2-prwlock
Requires: py2-virtualenv
Requires: py2-virtualenvwrapper
Requires: py2-urllib3
Requires: py2-chardet
Requires: py2-idna
Requires: py2-Werkzeug
Requires: py2-pytest
Requires: py2-avro
Requires: py2-fs
Requires: py2-lizard
Requires: py2-flawfinder
Requires: py2-python-ldap
Requires: py2-plac

Requires: py2-matplotlib
Requires: py2-numpy-toolfile
Requires: py2-sqlalchemy
Requires: py2-pygithub
Requires: py2-dxr-toolfile
Requires: py2-PyYAML
Requires: py2-pylint
Requires: py2-pip
%if %isamd64
Requires: py2-cx-Oracle
%endif
Requires: py2-cython
Requires: py2-future
Requires: py2-pybind11-toolfile
Requires: py2-histbook
Requires: py2-flake8
Requires: py2-autopep8
Requires: py2-pycodestyle
Requires: py2-lz4
Requires: py2-ply
Requires: py2-py
Requires: py2-typing
Requires: py2-defusedxml
Requires: py2-atomicwrites
Requires: py2-attrs
Requires: py2-nbdime
Requires: py2-onnx
Requires: py2-backports
Requires: py2-backports_abc
Requires: py2-colorama
Requires: py2-lxml
Requires: py2-beautifulsoup4
Requires: py2-GitPython
Requires: py2-Send2Trash
Requires: py2-gitdb2
Requires: py2-ipaddress
Requires: py2-mccabe
Requires: py2-more-itertools
Requires: py2-pluggy
Requires: py2-prometheus_client
Requires: py2-pyasn1-modules
Requires: py2-pyasn1
Requires: py2-pyflakes
Requires: py2-python-ldap
Requires: py2-smmap2
Requires: py2-stevedore
Requires: py2-typing_extensions
Requires: py2-virtualenv-clone
Requires: py2-asn1crypto
Requires: py2-backcall
Requires: py2-cffi
Requires: py2-cryptography
Requires: py2-google-common
Requires: py2-jedi
Requires: py2-parso
Requires: py2-pycparser
Requires: py2-absl-py
Requires: py2-gast
Requires: py2-grpcio
Requires: py2-Markdown
Requires: py2-subprocess32
Requires: py2-kiwisolver
Requires: py2-pyOpenSSL
Requires: py2-bokeh
Requires: py2-climate
Requires: py2-mpld3
Requires: py2-neurolab
Requires: py2-nose-parameterized
Requires: py2-pillow
Requires: py2-pybrain
Requires: py2-pymongo
Requires: py2-pydot

Requires: py2-astroid
Requires: py2-coverage
Requires: py3-hepdata-lib
Requires: py2-isort
Requires: py2-lazy-object-proxy
Requires: py2-pylint
Requires: py2-pytest-cov
Requires: py2-wrapt

%ifnarch ppc64le
Requires: py2-pycuda
%endif

%prep

%build

%install
mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/python_tools.xml
<tool name="%{n}" version="%{v}">
</tool>
EOF_TOOLFILE

