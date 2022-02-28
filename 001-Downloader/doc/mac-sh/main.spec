# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['main.py','type_enum.py','ui.py','utils.py','downloader.py','douyin/dy_download.py'],
             pathex=['.'],
             binaries=[],
             datas=[('res/logo.ico', 'images'),('config.ini', '.')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
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
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='res/logo.ico')
app = BUNDLE(exe,
             name='Downloader.app',
             icon='res/logo.ico',
             bundle_identifier=None)