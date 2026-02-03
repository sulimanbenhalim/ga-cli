# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['ga_cli/cli.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('ga_cli/*.py', 'ga_cli'),
        ('ga_cli/commands/*.py', 'ga_cli/commands'),
        ('ga_cli/formatters/*.py', 'ga_cli/formatters'),
    ],
    hiddenimports=[
        'click',
        'google.analytics.admin_v1alpha',
        'google.auth',
        'rich',
        'pytz',
        'ga_cli.commands.accounts',
        'ga_cli.commands.properties',
        'ga_cli.commands.datastreams',
        'ga_cli.commands.config',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ga-cli',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
