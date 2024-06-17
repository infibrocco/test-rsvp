# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.building.build_main import *
import sys
import os

path = os.path.abspath(".")
kivymd_repo_path = path.split("demos")[0]
sys.path.insert(0, kivymd_repo_path)

#from kivy_deps import sdl2, glew
from kivymd import hooks_path as kivymd_hooks_path


block_cipher = None


a = Analysis(
    ['src/main.py'],
    pathex=[path],
    binaries=[],
    datas=[("rssg/", "rssg/"), ("consts.json", "consts.json")],
    hiddenimports=['pkg_resources.extern',
    "libs.baseclass.bottom_app_bar",
        "libs.baseclass.bottom_sheet",
        "libs.baseclass.cards",
        "libs.baseclass.chips",
        "libs.baseclass.data_tables",
        "libs.baseclass.dialog_change_theme",
        "libs.baseclass.dialogs",
        "libs.baseclass.drop_item",
        "libs.baseclass.expansionpanel",
        "libs.baseclass.filemanager",
        "libs.baseclass.grid",
        "libs.baseclass.home",
        "libs.baseclass.list_items",
        "libs.baseclass.md_icons",
        "libs.baseclass.menu",
        "libs.baseclass.navigation_drawer",
        "libs.baseclass.pickers",
        "libs.baseclass.refresh_layout",
        "libs.baseclass.snackbar",
        "libs.baseclass.stack_buttons",
        "libs.baseclass.tabs",
        "libs.baseclass.taptargetview",
        "libs.baseclass.textfields",
        "libs.baseclass.toggle_button",
        "libs.baseclass.toolbar",
        "libs.baseclass.user_animation_card",
        "kivymd.stiffscroll",

    'kivymd.icon_definitions.md_icons'
    ],
    hookspath=[kivymd_hooks_path],
    #hooksconfig={},
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
    name='rsvp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
