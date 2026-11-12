[app]
title = Corange Video Game
package.name = corangevideogame
package.domain = org.corange.videogame
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,mp3,wav,txt,ogg
source.include_patterns = main.py,cobrinha.py,tetris.py,bomberman.py,icon.png,recorde*.txt
version = 1.4
requirements = python3,kivy
p4a.bootstrap = sdl2
p4a.fork = kivy
p4a.branch = master
orientation = portrait
fullscreen = 1
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.build_tools = 33.0.1
android.archs = arm64-v8a
android.accept_sdk_license_agreements = True
android.allow_backup = True
icon.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
warn_on_root = 1
