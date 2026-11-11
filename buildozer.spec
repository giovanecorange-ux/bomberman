[app]
title = Corange Jogos
package.name = corangejogos
package.domain = com.corange.jogos
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,mp3,wav,ttf
version = 1.0
requirements = python3,kivy,pygame,pillow
orientation = landscape
fullscreen = 0
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
android.permissions = INTERNET,VIBRATE
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
