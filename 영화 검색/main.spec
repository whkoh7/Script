# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['검색\\main.py'],
             pathex=['C:\\Users\\whkoh\\Desktop\\2020_1_Semester\\스언어\\term_project\\Script\\영화', 'C:\\Users\\whkoh\\Desktop\\2020_1_Semester\\스언어\\term_project\\Script\\영화 검색'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
