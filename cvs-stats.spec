### RPM external cvs-stats 20121025

%prep
%build
mkdir -p %i
cvs rlog -N -r CMSSW_6_0_0 CMSSW 2>/dev/null | grep -e "^date" | \
   sed -e 's/^date: \([0-9]*\)-\([0-9]*\)-[0-9]* .*;  author: \([^;]*\).*/\1 \2 \3/' | \
   sort -u > %i/per-user-data.txt
%install
