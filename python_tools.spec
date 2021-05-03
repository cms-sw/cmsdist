### RPM external python_tools 2.0
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}
Source: none

Requires: root curl python python3 xrootd llvm hdf5 mxnet-predict yoda opencv

Requires: py2-scipy
Requires: py3-Keras
Requires: py3-Theano
Requires: py2-scikit-learn
#save for the end
Requires: py3-tensorflow
Requires: py2-googlePackages
Requires: py3-cmsml
Requires: py3-law

Requires: py3-cloudpickle
Requires: py3-tables
Requires: py3-numexpr
Requires: py3-histogrammar
Requires: py3-pandas
Requires: py3-root_numpy
Requires: py3-Bottleneck
Requires: py3-downhill
Requires: py3-theanets
Requires: py2-xgboost py3-xgboost
Requires: py3-llvmlite
Requires: py3-numba
Requires: py3-hep_ml
Requires: py3-rep
Requires: py3-uncertainties
Requires: py3-hyperas
Requires: py3-hyperopt
Requires: py3-seaborn
Requires: py2-h5py
Requires: py3-h5py-cache
Requires: py3-root_pandas
Requires: py3-uproot
Requires: py3-uproot4
Requires: py2-opt-einsum
Requires: py2-joblib py3-joblib

#this DOES NOT depend on numpy..
Requires: py3-xrootdpyfs

Requires: root curl python openldap

Requires: py3-entrypoints
Requires: py3-psutil
Requires: py3-repoze-lru
Requires: py3-Jinja2
Requires: py3-MarkupSafe
Requires: py3-Pygments
Requires: py2-appdirs
Requires: py2-argparse
Requires: py3-bleach
Requires: py3-certifi
Requires: py2-decorator
Requires: py3-html5lib
Requires: py3-ipykernel
Requires: py3-ipython
Requires: py3-ipython_genutils
Requires: py3-ipywidgets
Requires: py3-jsonschema
Requires: py3-jupyter
Requires: py3-jupyter_client
Requires: py3-jupyter_console
Requires: py3-jupyter_core
Requires: py3-mistune
Requires: py3-nbconvert
Requires: py3-nbformat
Requires: py3-notebook
Requires: py2-ordereddict
Requires: py2-packaging
Requires: py3-pandocfilters
Requires: py2-pathlib2
Requires: py3-pexpect
Requires: py3-pickleshare
Requires: py3-prompt_toolkit
Requires: py3-ptyprocess
Requires: py2-pyparsing
Requires: py3-pyzmq
Requires: py3-qtconsole
Requires: py2-scandir
Requires: py2-setuptools
Requires: py3-setuptools
Requires: py3-simplegeneric
Requires: py2-singledispatch
Requires: py2-six
Requires: py3-terminado
Requires: py2-testpath
Requires: py3-testpath
Requires: py2-tornado
Requires: py3-traitlets
Requires: py2-wcwidth
Requires: py3-webencodings
Requires: py3-widgetsnbextension
Requires: py3-cycler
Requires: py3-docopt
Requires: py2-futures
Requires: py2-networkx
Requires: py3-parsimonious
Requires: py2-prettytable
Requires: py2-pycurl
Requires: py2-pytz
Requires: py3-requests
Requires: py3-schema
#Requires: py2-Jinja
Requires: py2-python-dateutil
Requires: py2-enum34
Requires: py3-mock
Requires: py3-pbr
Requires: py3-mpmath
Requires: py3-sympy
Requires: py3-tqdm
Requires: py2-funcsigs
Requires: py2-nose
Requires: py2-pkgconfig
Requires: py2-pysqlite
Requires: py3-Click
Requires: py3-jsonpickle
Requires: py3-prwlock
Requires: py3-virtualenv
Requires: py3-virtualenvwrapper
Requires: py3-urllib3
Requires: py3-chardet
Requires: py3-idna
Requires: py3-Werkzeug
Requires: py2-pytest
Requires: py3-avro
Requires: py2-fs
Requires: py3-lizard
Requires: py3-flawfinder
Requires: py3-python-ldap
Requires: py3-plac

Requires: py3-matplotlib
Requires: py2-numpy-toolfile
Requires: py2-sqlalchemy
Requires: py2-pygithub
Requires: py2-dxr-toolfile
Requires: py2-PyYAML
Requires: py3-pylint
Requires: py2-pip
Requires: py3-pip
%ifarch x86_64
Requires: py2-cx-Oracle
%endif
Requires: py2-cython
Requires: py2-future
Requires: py2-pybind11-toolfile
Requires: py3-histbook
Requires: py3-flake8
Requires: py3-autopep8
Requires: py3-pycodestyle
Requires: py2-lz4
Requires: py3-ply
Requires: py2-py
Requires: py2-typing
Requires: py3-defusedxml
Requires: py2-atomicwrites
Requires: py2-attrs
Requires: py3-nbdime
Requires: py2-onnx
Requires: py3-onnxmltools
Requires: py2-backports
Requires: py2-backports_abc
Requires: py2-colorama
Requires: py3-lxml
Requires: py3-beautifulsoup4
Requires: py3-GitPython
Requires: py3-Send2Trash
Requires: py3-ipaddress
Requires: py3-mccabe
Requires: py2-more-itertools
Requires: py2-pluggy
Requires: py3-prometheus_client
Requires: py3-pyasn1-modules
Requires: py2-pyasn1
Requires: py2-pyflakes
Requires: py3-smmap2
Requires: py3-stevedore
Requires: py2-typing_extensions
Requires: py3-virtualenv-clone
Requires: py3-asn1crypto
Requires: py3-backcall
Requires: py3-cffi
Requires: py3-cryptography
Requires: py2-google-common
Requires: py3-jedi
Requires: py3-parso
Requires: py2-pycparser
Requires: py2-absl-py
Requires: py3-gast
Requires: py2-grpcio
Requires: py2-grpcio-tools
Requires: py3-Markdown
Requires: py3-subprocess32
Requires: py3-kiwisolver
Requires: py3-pyOpenSSL
Requires: py3-bokeh py3-bokeh
Requires: py3-climate
Requires: py3-mpld3
Requires: py3-neurolab
Requires: py2-nose-parameterized
Requires: py2-pillow
Requires: py3-pybrain
Requires: py3-pymongo
Requires: py3-pydot

Requires: py3-astroid
Requires: py2-coverage
Requires: py3-hepdata-lib
Requires: py3-isort
Requires: py3-lazy-object-proxy
Requires: py3-pytest-cov
Requires: py3-wrapt

Requires: py3-distlib
Requires: py3-filelock
Requires: py3-gitdb
Requires: py3-importlib-resources
Requires: py3-smmap
Requires: py2-zipp py3-zipp

Requires: py3-pycuda
Requires: onnxruntime

Requires: py3-boost-histogram
Requires: py3-hist
Requires: py3-histoprint
Requires: py3-mplhep
Requires: py3-correctionlib

%prep

%build

%install
mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/python_tools.xml
<tool name="%{n}" version="%{v}">
</tool>
EOF_TOOLFILE

