[app]
title = Corange Jogos
package.name = corangejogos
package.domain = org.corange
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,mp3,wav,ttf,json
version = 1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,VIBRATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
