### RPM cms reqmon-meta 1204h

# This is a meta package that only requires all the projects
# needed for a reqmon deployment release. This is to be used
# with the Deploy script -R option (see
# https://cms-http-group.web.cern.ch/cms-http-group/ops-deploy.html)

Requires: reqmon frontend rotatelogs pystack 

%prep
%build
%install
