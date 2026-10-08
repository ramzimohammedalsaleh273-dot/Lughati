# لغتي — تطبيق الجوال
واجهة Android وiOS حقيقية مبنية بـ Flutter، مع SQLite محلي ومبدأ Offline-first.
التشغيل: flutter pub get ثم flutter test ثم flutter run.
البناء: (Get-Content android/app/build.gradle) -replace 'compileSdk = flutter.compileSdkVersion','compileSdk = 36' -replace 'minSdk = flutter.minSdkVersion','minSdk = 24' | Set-Content android/app/build.gradle
flutter build apk --release أو flutter build appbundle --release أو flutter build ios --release.
