### RPM external monalisa-apmon 2.2.0
## BUILDIF case $(uname):$(uname -m) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;; Linux:ppc64 ) true ;; Darwin:* ) true ;; * ) false ;; esac

Source: http://monalisa.cacr.caltech.edu/download/apmon/ApMon_cpp-%{realversion}.tar.gz

%prep
%setup -n ApMon_cpp-%{realversion}
# Fix an unnecessary class qualification, causes error with gcc4.1.1 
perl -p -i -e "s|ProcUtils::getProcesses|getProcesses|g" proc_utils.h

%build
./configure --prefix=%i
make %makeprocesses
