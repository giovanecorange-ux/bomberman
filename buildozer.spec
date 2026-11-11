[app]
title = Corange Video Game
package.name = corangevideogame
package.domain = org.corange.videogame
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,mp3,wav,txt,ogg
source.include_patterns = main.py,cobrinha.py,tetris.py,bomberman.py,icon.png,recorde*.txt
version = 1.2
requirements = python3,sdl2,pygame,sdl2_ttf,sdl2_mixer,sdl2_image
p4a.bootstrap = sdl2
orientation = portrait
fullscreen = 1
android.api = 33
android.minapi = 21
android.ndk = 25.1.8937393
android.sdk = 33
android.archs = arm64-v8a
android.allow_backup = True
android.accept_sdk_license = True
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/icon.png
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

[buildozer]
log_level = 2
warn_on_root = 1
