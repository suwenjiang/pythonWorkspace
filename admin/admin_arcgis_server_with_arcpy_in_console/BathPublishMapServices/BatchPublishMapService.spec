# -*- mode: python -*-
a = Analysis(['BatchPublishMapService.py'],
             pathex=['D:\\Personalwork\\pythonProject\\admin\\Arcpy_Project-master\\BathPublishMapServices'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='BatchPublishMapService.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
