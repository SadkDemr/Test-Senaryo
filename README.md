  Adım 1: Remote URL'i HTTPS'e çevir
  git remote set-url origin https://github.com/KULLANICI_ADI/REPO_ADI.git

  Repo adını öğrenmek için:
  git remote -v

  Adım 2: GitHub Personal Access Token oluştur

  GitHub'da: Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token

  - Scope olarak repo seç
  - Token'ı kopyala

  Adım 3: git pull yap
  git pull

  Kullanıcı adı ve şifre soracak — şifre yerine token'ı yapıştır.

  Adım 4: Token'ı kaydet (her seferinde sormasm için)
  git config --global credential.helper store

  Bir kez daha git pull yapınca token'ı gir, sonra kaydedecek.
