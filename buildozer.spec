[app]
title = Bomberman Corange
package.name = corangebomber
package.domain = org.corangebomber
source.dir = .
source.include_exts = py,png,jpg,kv,mp3,wav,ttf
version = 1.0
requirements = python3,kivy==2.3.0,pillow
p4a.bootstrap = sdl2
p4a.branch = v2024.01.21
orientation = portrait

[buildozer]
log_level = 2

[app:android]
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk_build_tools_version = 33.0.2
android.accept_sdk_license_agreement = True
android.archs = arm64-v8a,armeabi-v7a
