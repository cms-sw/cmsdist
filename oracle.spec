### RPM external oracle 11.2.0.1.0p2
## INITENV SET ORACLE_HOME %i
## BUILDIF case `uname`:`uname -m` in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) false ;; esac

Source0: http://cmsrep.cern.ch/cmssw/oracle-mirror/%cmsos/%realversion/oracle_lcg.tgz
Source9: oracle-license
Requires: fakesystem 

## INITENV +PATH SQLPATH %i/bin
%prep 
%setup -n %realversion

%build

%install
mkdir -p %i/bin %i/lib %i/doc %i/include
cp %_sourcedir/oracle-license %{i}/oracle-license
cp -r bin/* %i/bin/
cp -r lib/* %i/lib/
cp -r doc/* %i/doc/
cp -r include/* %i/include/
