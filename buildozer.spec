[app]
title = Bomberman Corange
package.name = corangebomber
package.domain = org.corangebomber
source.dir = .
source.include_exts = py,png,wav,mp3
version = 1.0
requirements = python3,kivy
orientation = portrait

[buildozer]
log_level = 2

[app:android]
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.build_tools_version = 33.0.2
android.accept_sdk_license_agreement = True
