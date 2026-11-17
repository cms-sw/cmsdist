## INCLUDE openloops-common
### RPM external openloops-process %{openloop_version}

## NOCOMPILER
## NO_AUTO_DEPENDENCY

%define process_src process_src.tgz
Source2: https://cmsrep.cern.ch/cmssw/download/openloops/%{realversion}/%{cmsdist_chksum_source1}?cmdist-generated=1&output=/%{process_src}
Patch0: openloops-urlopen2curl

%prep
if [ ! -e %{SOURCE2} ] ; then
%setup -n openloops-%{realversion}
%patch0 -p1
else
mkdir openloops-%{realversion}
fi

%build

%install
if [ ! -e %{SOURCE2} ] ; then
  cp %{_sourcedir}/openloops-user.coll openloops-user.coll
  python3 pyol/bin/download_process.py $(cat %{_sourcedir}/openloops-user.coll | tr '\n' ' ')
  tar -czf %{process_src} process_src proclib
  cp {process_src} %{i}/%{process_src}
else
  cp %{SOURCE2} %{i}/%{process_src}
fi
