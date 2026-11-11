[app]
title = Bomberman Corange
package.name = bombermancorange
package.domain = org.corange.bomberman
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,mp3,wav
version = 1.0
requirements = python3,kivy==2.3.0
orientation = portrait
fullscreen = 0
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a,armeabi-v7a
android.allow_backup = True
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
