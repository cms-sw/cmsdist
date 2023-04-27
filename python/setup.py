#!/usr/bin/env python


from __future__ import print_function

import os
import sys


from distutils.core import setup

#pjoin = os.path.join
here = os.path.abspath(os.path.dirname(__file__))


setup_args = dict(
    name                = 'pyCMSSW',
    version             = '0.1',
    description         = "CMSSW metapackage. Install all the CMSSW python components in one go.",
    long_description    = """Install the CMSSW python system.""",
    author              = "CMSSW Release Team",
    author_email        = "david.lange@cern.ch",
    py_modules          = [],
    install_requires = [
        'appdirs==1.4.3',
        'argparse==1.4.0',
        'avro==1.8.2',
        'backports_abc==0.5',
        'backports.ssl_match_hostname==3.5.0.1',
        'bleach==2.0.0',
        'bottleneck==1.2.1',
        'certifi==2017.4.17',
        'chardet==3.0.4',
        'python-cjson==1.2.1',
        'click==6.7',
        'climate==0.4.6',
        'configparser==3.5.0',
        'cycler==0.10.0',
        'cython==0.26',
        'decorator==4.0.11',
        'deepdish==0.3.4',
        'docopt==0.6.2',
        'downhill==0.4.0',
        'entrypoints==0.2.3',
        'enum34==1.1.6',
        'fs==2.0.7',
        'funcsigs==1.0.2',
        'functools32==3.2.3-2',
        'futures==3.1.1',
        'h5py==2.7',
        'hep_ml==0.4.0',
        'histogrammar==1.0.8',
        'html5lib==0.999999999',
        'hyperas==0.3',
        'hyperopt==0.1',
        'idna==2.5',
        'ipykernel==4.6.1',
        'ipython_genutils==0.2.0',
        'ipython==5.3.0',
        'ipywidgets==5.2.2',
        'Jinja2==2.9.6',
        'Jinja==1.2',
        'jsonpickle==0.9.4',
        'jsonschema==2.6.0',
        'jupyter_client==5.0.1',
        'jupyter_console==5.1.0',
        'jupyter_core==4.3.0',
        'jupyter==1.0.0',
        'Keras==2.0.5',
        'MarkupSafe==1.0',
        'matplotlib==1.5.2',
        'mistune==0.7.4',
        'mock==2.0.0',
        'mpmath==0.19',
        'nbconvert==5.2.1',
        'nbformat==4.3.0',
        'networkx==1.11',
        'nose==1.3.7',
        'notebook==4.3.1',
        'numpy==1.12.1',
        'numexpr==2.6.2',
        'ordereddict==1.1',
        'packaging==16.8',
        'pandas==0.20.2',
        'pandocfilters==1.4.1',
        'parsimonious==0.7.0',
        'pathlib2==2.3.0',
        'pbr==3.0.1',
        'pexpect==4.2.1',
        'pickleshare==0.7.4',
        'pip==9.0.1',
        'pkgconfig==1.2.2',
        'prettytable==0.7.2',
        'prompt_toolkit==1.0.14',
        'protobuf==3.2.0',
        'prwlock==0.4.0',
        'psutil==5.2.2',
        'ptyprocess==0.5.1',
        'pycurl==7.43.0',
        'Pygments==2.2.0',
        'pyparsing==2.2.0',
        'pytest==3.1.3',
        'python-dateutil==2.6.0',
        'pytz==2017.2',
        'pyzmq==16.0.2',
        'qtconsole==4.3.0',
        'repoze.lru==0.6',
        'rep==0.6.6',
        'requests==2.18.1',
        'scandir==1.5',
        'schema==0.6.6',
        'scikit-learn==0.18.1',
        'scipy==0.19.0',
        'seaborn==0.7.1',
        'backports.shutil_get_terminal_size==1.0.0',
        'simplegeneric==0.8.1',
        'singledispatch==3.4.0.3',
        'sympy==1.0',
        'tables==3.4.2',
        'tensorflow==1.1.0',
        'terminado==0.6',
        'testpath==0.3.1',
        'theanets==0.7.3',
        'Theano==0.8.2',
        'thriftpy==0.3.9',
        'tornado==4.4.2',
        'tqdm==4.14.0',
        'traitlets==4.3.2',
        'uncertainties==3.0.1',
        'urllib3==1.21.1',
        'virtualenv==15.1.0',
        'virtualenvwrapper==4.7.2',
        'wcwidth==0.1.7',
        'webencodings==0.5.1',
        'werkzeug==0.12.2',
        'wheel==0.30.0a0',
        'widgetsnbextension==1.2.6',
        'xgboost==0.6a2'
    ],
    url                 = "http://github.com/cms-sw/cmssw",
    license             = "BSD",
    classifiers         = [
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)

 
if any(bdist in sys.argv for bdist in ['bdist_wheel', 'bdist_egg']):
    import setuptools


if 'ROOTSYS' in os.environ:
    setup_args['install_requires'].append('rootpy==0.9.1') 
    setup_args['install_requires'].append('root_numpy==4.7.2')
    setup_args['install_requires'].append('xrootdpyfs==0.1.4')

if __name__ == '__main__':

    setup( #cmdclass={'install':InstallCommand,},
        **setup_args)
