[app]
title = Bomberman Corange
package.name = corangebomber
package.domain = org.corangebomber
source.dir = .
version = 0.1
requirements = python3,kivy
orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license_agreement = True
p4a.bootstrap = sdl2
