[app]
title = Bomberman Corange
package.name = bomberman
package.domain = org.corange.bomberman
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,mp3,ogg
icon.filename = %(source.dir)s/icon.png
version = 0.1
requirements = python3,kivy==2.3.0
orientation = portrait
fullscreen = 1
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license_agreements = True
android.archs = arm64-v8a, armeabi-v7a
p4a.branch = v2024.01.21

[buildozer]
log_level = 2
