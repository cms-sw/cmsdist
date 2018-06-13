### RPM external py2-xgboost 0.72
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}


%define pip_name xgboost

#%define PipPreBuild tar -xvzf %{pip_name}-%{realversion}.tar.gz && \
#                    pushd %{pip_name}-%{realversion} && \
#                    for patch_file in %{patches} ; do patch -p1 < ${patch_file} ; done && \
#                    popd && \
#                    rm -f %{pip_name}-%{realversion}.tar.gz && \
#                    tar cvzf %{pip_name}-%{realversion}.tar.gz %{pip_name}-%{realversion}

## IMPORT build-with-pip

%define PipPostBuild \
   perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/lib/python2.7/site-packages/xgboost/rabit/*/*.py; \
   perl -p -i -e "s|^#!.*python|#!/usr/bin/env python3|" %{i}/lib/python3.*/site-packages/xgboost/rabit/*/*.py 

