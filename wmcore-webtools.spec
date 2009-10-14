### RPM cms wmcore-webtools forHEARTBEATr01
## INITENV +PATH PYTHONPATH %i/lib

%define cvstag %v
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=WMCORE&export=WMCORE&&tag=-r%{cvstag}&output=/WMCORE.tar.gz

# added the versions
Requires: wmcore cherrypy py2-cheetah py2-openid

%prep
%setup -n WMCORE
%build

# we use this to generate a script which initializes the dependencies

rm -rf %i/etc/profile.d
mkdir -p %i/etc/profile.d
mkdir -p %i/etc/init.d
echo '#!/bin/sh' > %{i}/etc/profile.d/dependencies-setup.sh
echo '#!/bin/tcsh' > %{i}/etc/profile.d/dependencies-setup.csh
echo requiredtools `echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'`
for tool in `echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'`
do
    case X$tool in
        Xdistcc|Xccache )
        ;;
        * )
            toolcap=`echo $tool | tr a-z- A-Z_`
            eval echo ". $`echo ${toolcap}_ROOT`/etc/profile.d/init.sh" >> %{i}/etc/profile.d/dependencies-setup.sh
            eval echo "source $`echo ${toolcap}_ROOT`/etc/profile.d/init.csh" >> %{i}/etc/profile.d/dependencies-setup.csh
        ;;
    esac
done

perl -p -i -e 's|\. /etc/profile\.d/init\.sh||' %{i}/etc/profile.d/dependencies-setup.sh
perl -p -i -e 's|source /etc/profile\.d/init\.csh||' %{i}/etc/profile.d/dependencies-setup.csh


%install
make PREFIX=%i install
mkdir -p %i
cp -r * %i

mkdir -p %{i}/etc/profile.d
mkdir -p %i/workdir

#(echo "#!/bin/sh"; \
# echo "source $PY2_SIMPLEJSON_ROOT/etc/profile.d/init.sh"; \
# echo "source $PY2_SQLALCHEMY_ROOT/etc/profile.d/init.sh") > %{i}/etc/profile.d/dependencies-setup.sh

#(echo "#!/bin/tcsh"; \
# echo "source $PY2_SIMPLEJSON_ROOT/etc/profile.d/init.csh"; \
# echo "source $PY2_SQLALCHEMY_ROOT/etc/profile.d/init.csh") > %{i}/etc/profile.d/dependencies-setup.csh


%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
