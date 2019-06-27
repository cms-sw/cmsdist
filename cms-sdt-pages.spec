### RPM cms cms-sdt-pages 1.0
## NOCOMPILER

%prep
%build
%install
cat << \EOF > %cmsroot/WEB/index.html
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
   "http://www.w3.org/TR/html4/strict.dtd">

<html lang="en">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <title>Overview of cmssdt.cern.ch</title>
  <meta name="generator" content="TextMate http://macromates.com/">
  <meta name="author" content="Andreas Pfeiffer">
  <!-- Date: 2010-06-15 -->

</head>
<body>

<h1 id="overview_of_services_provided_on_cmssw.cern.ch">Overview of services provided by the Software Development Tools service</h1>

<h3>Portals for the CMSSW IntegrationBuild and related applications</h3>
<ul>
  <li> <a href="/SDT/html/showIB.html">CMSSW IB - Integration Build portal</a> </li>
  <li> <a href="/qa/perfmondb/">CMSSW perfDB - performance database </a> </li>
  <li> <a href="/tcdev/">CMSSW TagCollector upgrade (dev) </a> </li>
</ul>

<h3>Code documentation service for CMSSW</h3>
<ul>
  <li> <a href="/SDT/lxr">CMSSW lxr - software cross-reference</a> </li>
  <!-- li> <a href="https://cms-cpt-software.web.cern.ch/cms-cpt-software/General/gendoxy-doc.php"> CMSSW doxygen reference documentation </a> </li -->
  <li> <a href="/SDT/cgi-bin/doxygen.php"> CMSSW doxygen reference documentation </a> </li>
</ul>

</body>
</html>
EOF
# bla bla
