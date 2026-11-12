[app]
title = Bomberman Corange
package.name = corangebomber
package.domain = org.corangebomber
source.dir = .
source.include_exts = py,png,mp3
version = 1.0
requirements = python3,kivy==2.3.0,pillow
p4a.bootstrap = sdl2
p4a.branch = master
orientation = portrait

[buildozer]
log_level = 1

[app:android]
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license_agreements = True
