# 🔨 Sudoku Solver - Build Instructions

Bu dosya, Sudoku Solver uygulamasını executable (çalıştırılabilir) dosyaya dönüştürmek için gerekli adımları içerir.

## 📋 Gereksinimler

Öncelikle tüm bağımlılıkların yüklü olduğundan emin olun:

```bash
pip install -r requirements.txt
pip install pyinstaller pillow
```

## 🚀 Build Alma

### Otomatik Build (Önerilen)

Tek komutla build alın:

```bash
python build.py
```

Bu script:
- ✅ PyInstaller'ı otomatik yükler (yoksa)
- ✅ Eski build dosyalarını temizler
- ✅ Platform-specific icon oluşturur (.ico veya .icns)
- ✅ Tek dosya executable üretir
- ✅ Terminal penceresi olmadan çalışır
- ✅ Gerekli dosyaları paketler (media, utils, config.ini)

### Manuel Build

PyInstaller komutunu manuel çalıştırmak isterseniz:

#### macOS:
```bash
pyinstaller --name SudokuSolver \
            --onefile \
            --windowed \
            --icon media/icon.png \
            --add-data "media:media" \
            --add-data "utils:utils" \
            --add-data "config.ini:." \
            main.py
```

#### Windows:
```bash
pyinstaller --name SudokuSolver ^
            --onefile ^
            --windowed ^
            --icon media/icon.ico ^
            --add-data "media;media" ^
            --add-data "utils;utils" ^
            --add-data "config.ini;." ^
            main.py
```

## 📦 Build Çıktıları

Build başarılı olunca şu dosyalar/klasörler oluşur:

```
dist/
├── SudokuSolver.exe      (Windows)
└── SudokuSolver.app      (macOS)

build/                     (Geçici dosyalar - silinebilir)
main.spec                  (PyInstaller spec - silinebilir)
```

## 🎯 Dağıtım

### Windows Kullanıcıları İçin:
1. `dist/SudokuSolver.exe` dosyasını paylaşın
2. Kullanıcılar `.exe` ile aynı klasöre `config.ini` dosyası koymalı
3. `config.ini` içinde API key olmalı:
   ```ini
   [GENAI]
   API_KEY = your_api_key_here
   ```

### macOS Kullanıcıları İçin:
1. `dist/SudokuSolver.app` bundle'ını paylaşın
2. İlk açılışta "Güvenilmeyen geliştirici" hatası alınırsa:
   - Sistem Tercihleri → Güvenlik ve Gizlilik → "Yine de Aç"
3. Veya terminal'den imzalayın (geliştirici hesabı gerekir):
   ```bash
   codesign -s "Developer ID" dist/SudokuSolver.app
   ```

## 🔧 Sorun Giderme

### "ModuleNotFoundError" hatası
```bash
# Eksik modülleri hidden-import olarak ekleyin
pyinstaller ... --hidden-import eksik_modul_adi ...
```

### Icon görünmüyor
- Windows: `media/icon.ico` dosyasının var olduğundan emin olun
- macOS: `media/icon.icns` dosyası build script tarafından otomatik oluşturulur

### Executable çok büyük
- `--onefile` yerine `--onedir` kullanın (birden fazla dosya oluşturur ama daha küçük)
- Gereksiz kütüphaneleri çıkarın

### Config dosyası bulunamıyor
- Kullanıcılar executable ile aynı dizine `config.ini` koymalı
- Veya spec dosyasında default config içerebilirsiniz

## 📝 Notlar

- Build süreci 2-5 dakika sürebilir
- İlk build en uzun olanıdır (PyInstaller cache oluşturur)
- Her platform için o platformda build alın (cross-compilation desteklenmez)
- Executable dosya boyutu ~150-200 MB olabilir (PyQt5 dahil)

## ✅ Build Testi

Build'i test etmek için:

```bash
# macOS
./dist/SudokuSolver.app/Contents/MacOS/SudokuSolver

# Windows
dist\SudokuSolver.exe

# Linux
./dist/SudokuSolver
```

## 🎨 Icon Değiştirme

Farklı bir icon kullanmak için:

1. PNG formatında icon hazırlayın (512x512 önerilir)
2. `media/icon.png` dosyasını değiştirin
3. `python build.py` komutuyla tekrar build alın

---

**Destek:** Sorun yaşarsanız PyInstaller dokümantasyonuna bakın: https://pyinstaller.org
