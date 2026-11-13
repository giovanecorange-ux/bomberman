[app]
title = Bomberman Corange
package.name = bombermancorange
package.domain = org.corange.bomberman
source.dir = .
source.include_exts = py,png,mp3,txt,wav
version = 1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/icon.png
android.presplash_color = #101020
android.permissions = INTERNET
android.logcat_filters = *:S python:D
p4a.branch = master
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1
