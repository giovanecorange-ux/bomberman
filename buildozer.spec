[app]
title = Bomberman Corange
package.name = corangebomber
package.domain = org.corangebomber
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,wav,mp3
version = 1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2

[app:android]
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.accept_sdk_license_agreement = True
