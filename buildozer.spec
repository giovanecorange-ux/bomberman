[app]
title = Bomberman Corange
package.name = corangebomber
package.domain = org.corangebomber
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,mp3
version = 1.0
requirements = python3,kivy
orientation = portrait
icon.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2

[app:android]
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
p4a.branch = master
