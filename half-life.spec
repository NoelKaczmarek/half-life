# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
    ( 'icon.ico', '.' ),
]


a = Analysis(['window.py'],
             pathex=['C:\\Users\\Noel Kaczmarek\\.virtualenvs\\half-life-5kkWj3xB\\Lib\\site-packages', 'E:\\Development\\half-life'],
             binaries=[],
             datas=added_files,
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Half-Life',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon='icon.ico' )