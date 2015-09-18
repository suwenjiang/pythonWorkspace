__author__ = 'jiangmb'
import os
import tempfile

tempdir = tempfile.TemporaryFile("w")
tmpdir2=tempfile.NamedTemporaryFile('w')
dd=tempfile.mkdtemp()
print os.path.join(dd,'tmp.ags')

print tmpdir2,tempdir,dd