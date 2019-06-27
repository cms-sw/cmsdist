#!/bin/sh -e
#
rm -f lhapdf_makeLinks.file
echo "#!/bin/sh -e" > lhapdf_makeLinks.file
echo >> lhapdf_makeLinks.file
echo "#PDF sets list is made for:" >> lhapdf_makeLinks.file
echo "export lhapdf6setsVersion=$1" >> lhapdf_makeLinks.file
echo >> lhapdf_makeLinks.file
echo "if [ x%1 != x%lhapdf6setsVersion ]; then" >> lhapdf_makeLinks.file
echo "  echo lhapdf_makeLinks: lhapdf6sets versions do not coincide" >> lhapdf_makeLinks.file
echo "  echo please create this script by running lhapdf_makeScript.sh with correct version" >> lhapdf_makeLinks.file
echo "  exit 1" >> lhapdf_makeLinks.file
echo "fi" >> lhapdf_makeLinks.file
echo >> lhapdf_makeLinks.file
#
echo "export cvmfspath=/cvmfs/cms.cern.ch/lhapdf/pdfsets/%1" >> lhapdf_makeLinks.file
export ss=`ls /cvmfs/cms.cern.ch/lhapdf/pdfsets/$1`
echo export pdflist=@${ss}@ >> lhapdf_makeLinks.file
echo "for pdf in %{pdflist} ; do" >> lhapdf_makeLinks.file 
echo "  if [ ! -d @%{pdf}@ ] ; then" >> lhapdf_makeLinks.file
echo "    echo missing pdf: %{pdf} ---" >> lhapdf_makeLinks.file
echo "    echo making soft link to cvmfs" >> lhapdf_makeLinks.file
echo "    ln -fs %{cvmfspath}/%{pdf} %{pdf}" >> lhapdf_makeLinks.file
echo "  fi" >> lhapdf_makeLinks.file
echo "done" >> lhapdf_makeLinks.file

sed "s/%/$/g" < lhapdf_makeLinks.file > lhapdf_makeLinks.file_1
sed "s/@/\"/g" < lhapdf_makeLinks.file_1 > lhapdf_makeLinks.file_2
mv lhapdf_makeLinks.file_2 lhapdf_makeLinks.file
rm -f lhapdf_makeLinks.file_*

cp -f /cvmfs/cms.cern.ch/lhapdf/pdfsets/$1/pdfsets.index lhapdf_pdfsetsindex.file
# bla bla
