## INCLUDE openloops-common
### RPM external openloops-process %{openloop_version}

## NOCOMPILER
## NO_AUTO_DEPENDENCY

%define process_src process_src.tgz
Source2: https://cmsrep.cern.ch/cmssw/download/openloops/%{realversion}/%{cmsdist_chksum_source1}?cmdist-generated=1&output=/%{process_src}
Patch0: openloops-urlopen2curl

%prep
%setup -n openloops-%{realversion}
%patch0 -p1

%build

%install
chksum_source2="SOURCES/cache/$(echo %{cmsdist_chksum_source2} | cut -c1-2)/%{cmsdist_chksum_source2}"
if [ ! -e %{cmsroot}/${chksum_source2}/%{process_src} ] ; then
  cp %{_sourcedir}/openloops-user.coll openloops-user.coll
  pyol/bin/download_process.py $(cat %{_sourcedir}/openloops-user.coll | tr '\n' ' ')
  tar -czf %{process_src} process_src proclib
  mkdir -p %{cmsroot}/${chksum_source2}
  mv %{process_src} %{cmsroot}/${chksum_source2}/
fi
if [ ! -e %{_sourcedir}/%{process_src} ] ; then
  mkdir -p %{_sourcedir}
  ln -s %{cmsroot}/${chksum_source2}/%{process_src} %{_sourcedir}/%{process_src}
fi
ln -s %{cmsroot}/${chksum_source2}/%{process_src} %{pkginstroot}/
