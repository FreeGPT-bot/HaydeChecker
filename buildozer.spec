[app]

# Основные настройки
title = HaydeChecker
package.name = haydechecker
package.domain = org.hayde
source.dir = .
version = 1.0
requirements = 
    python3==9.0.0,
    kivy==2.3.0,
    telethon==1.28.0,
    pycryptodome==3.18.0,
    pysocks==1.7.1,
    openssl,
    asyncio

# Android-специфичные настройки
android.arch = arm64-v8a  # Оптимально для современных устройств
android.ndk_path = 
android.sdk_path = 
android.ndk_version = 23b
android.sdk = 34
android.minapi = 21
android.targetapi = 33
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE
android.allow_backup = False
android.debuggable = False

# Дополнительные библиотеки
android.add_libs_armeabi_v7a = libs/*.so
android.add_libs_arm64_v8a = libs/arm64-v8a/*.so

# Оптимизации
p4a.branch = develop
p4a.options = --use-venv
android.enable_androidx = True
android.release_artifact = .apk

[buildozer]
log_level = 2
warn_on_root = 1
