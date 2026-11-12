[app]
title = Bomberman Corange
package.name = corangebomber
package.domain = org.corangebomber
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 1.0
requirements = python3==3.11.8,kivy==2.3.0
orientation = portrait

[buildozer]
log_level = 2

[app:android]
p4a.branch = master
android.bootstrap = sdl2
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
