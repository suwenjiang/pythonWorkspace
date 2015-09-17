import tempfile
import zipfile
import shutil
import os
import xml.dom.minidom as DOM
def remove_from_zip(zipfname, *filenames):
    EXCLUDED_FILE_NAMES = ["DocumentInfo.xml", "layers/layers.xml","GISProject.xml"]
    tempdir = tempfile.mkdtemp()
    try:
        tempname = os.path.join(tempdir, 'new.zip')
        with zipfile.ZipFile(zipfname, 'r') as zipread:
            with zipfile.ZipFile(tempname, 'w') as zipwrite:
                for item in zipread.infolist():
                    data = zipread.read(item.filename)
                    if item.filename not in filenames:
                        zipwrite.writestr(item, data)
                    else:
                        xml=zipread.open(item.filename)
                        print xml
                        dom=DOM.parse(xml)
                        pWorkspaceConnectionString=dom.getElementsByTagName('WorkspaceConnectionString')[0].childNodes[0].nodeValue
                        print pWorkspaceConnectionString
                        dom.getElementsByTagName('WorkspaceConnectionString')[0].childNodes[0].nodeValue='dd'
                        pWorkspaceConnectionString=dom.getElementsByTagName('WorkspaceConnectionString')[0].childNodes[0].nodeValue
                        print pWorkspaceConnectionString

                        outxml=r"d:\text.xml"
                        f=open(outxml,"w")
                        dom.writexml(f)
                        f.close()
                        newdata=zipread.read(item.filename)
                        zipwrite.writestr(item,newdata)



        shutil.move(tempname, zipfname)
    finally:
        shutil.rmtree(tempdir)
path=r"C:\arcgisserver\directories\arcgissystem\arcgisinput\test4\testCopy.MapServer\extracted\v101\testCopy.msd"
remove_from_zip(path, 'layers/_population.xml')
with zipfile.ZipFile(path, 'a') as z:
    z.write('hello.txt')