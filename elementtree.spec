### RPM external elementtree 1.2.6
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif
Source: http://effbot.org/downloads/%n-%realversion-20050316.zip
Requires: python
 
%prep
%setup -n %n-%realversion-20050316

%build
%install
%if "%mic" == "true"
$PYTHON_ROOT/host/hostpython setup.py install --prefix=%i/share
%else
python setup.py install --prefix=%i/share
%endif
