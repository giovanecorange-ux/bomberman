[app]
title = Corange Video Game
package.name = corangevideogame
package.domain = org.corange.videogame
source.dir = .
source.include_exts = py,png,jpg,txt,ttf
source.include_patterns = main.py,cobrinha.py,tetris.py,bomberman.py,icon.png
version = 1.6
requirements = python3, pygame==2.5.2
p4a.bootstrap = sdl2
orientation = landscape
fullscreen = 0
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.build_tools = 33.0.1
android.archs = arm64-v8a
android.accept_sdk_license = True
android.allow_backup = True
android.wakelock = True
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
icon.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
warn_on_root = 1
