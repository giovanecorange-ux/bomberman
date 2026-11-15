[app]
title = Bomberman
package.name = bomberman
package.domain = org.corange
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,mp3
version = 1.1
requirements = python3,kivy==2.3.0
orientation = portrait
fullscreen = 0

# ICONE E TELA INICIAL - ISSO QUE FALTAVA
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/icon.png

android.api = 33
android.minapi = 24
android.ndk = 25b
android.sdk = 33
android.accept_sdk_license = True
android.archs = arm64-v8a,armeabi-v7a
p4a.branch = v2024.01.21
android.permissions = INTERNET
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
