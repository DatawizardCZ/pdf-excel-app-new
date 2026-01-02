# 🔑 Rychlý průvodce: Oprava "Cannot deploy without deploy key"

## 🚨 DŮLEŽITÉ: Deploy keys jsou zakázané v organizaci

**Pokud máte problém s deploy keys zakázanými v GitHub organizaci, použijte řešení níže:**

### ✅ Řešení pro organizace s zakázanými deploy keys

1. **Použijte GitHub App (nejlepší řešení):**
   - Streamlit Cloud podporuje GitHub Apps, které nevyžadují deploy keys
   - V Streamlit Cloud Settings → GitHub App můžete nainstalovat Streamlit Cloud GitHub App
   - Toto automaticky nastaví potřebná oprávnění bez deploy keys

2. **OAuth Token Authentication:**
   - Pokud OAuth už funguje, Streamlit Cloud by měl používat OAuth tokeny místo deploy keys
   - Zkontrolujte v Streamlit Cloud Settings, zda je aktivní "Use OAuth token" místo "Use deploy key"

3. **Kontaktujte organizačního administrátora:**
   - Požádejte admina o povolení Streamlit Cloud GitHub App v organizaci
   - Nebo požádejte o dočasné povolení deploy keys pro váš repozitář

4. **Alternativa: Použijte osobní fork:**
   - Vytvořte fork repozitáře do vašeho osobního GitHub účtu
   - Deploy z osobního účtu (deploy keys tam nejsou zakázané)
   - Nastavte automatickou synchronizaci změn z organizačního repozitáře

---

## ✅ Nejjednodušší řešení (doporučeno)

### Krok 1: Autorizujte Streamlit Cloud na GitHub

1. **Jděte na Streamlit Cloud:**
   - Otevřete [share.streamlit.io](https://share.streamlit.io)
   - Přihlaste se pomocí GitHub účtu

2. **Zkontrolujte připojení GitHub:**
   - Klikněte na váš **profil** (pravý horní roh)
   - Vyberte **"Settings"** nebo **"Account settings"**
   - Najděte sekci **"Connected accounts"** nebo **"GitHub"**

3. **Připojte GitHub (pokud není připojen):**
   - Klikněte na **"Connect GitHub"** nebo **"Authorize Streamlit"**
   - GitHub vás přesměruje na autorizační stránku
   - **Povolte přístup** k vašim repozitářům
   - Můžete omezit přístup pouze na konkrétní repozitář

4. **Zkuste znovu deploy:**
   - Vraťte se na Streamlit Cloud
   - Vytvořte novou aplikaci nebo upravte existující
   - Měli byste nyní vidět váš repozitář v seznamu

---

## 🔧 Alternativní řešení 1: GitHub App (doporučeno pro organizace)

**Pokud jsou deploy keys zakázané v organizaci, použijte GitHub App:**

1. **V Streamlit Cloud:**
   - Jděte na [share.streamlit.io](https://share.streamlit.io)
   - Otevřete Settings vaší aplikace
   - Najděte sekci **"GitHub App"** nebo **"Repository access"**
   - Klikněte na **"Install GitHub App"** nebo **"Configure GitHub App"**

2. **Na GitHub:**
   - Budete přesměrováni na GitHub pro autorizaci
   - Vyberte organizaci a repozitář
   - Klikněte na **"Install"** nebo **"Authorize"**
   - GitHub App automaticky nastaví potřebná oprávnění

3. **Vraťte se na Streamlit Cloud:**
   - GitHub App by měl být nyní aktivní
   - Zkuste znovu deploy

**Výhody GitHub App:**
- ✅ Nevyžaduje deploy keys
- ✅ Funguje i když jsou deploy keys zakázané
- ✅ Bezpečnější než deploy keys
- ✅ Snadnější správa oprávnění

---

## 🔧 Alternativní řešení 2: Nastavení Deploy Key

**⚠️ POZOR: Toto nefunguje, pokud jsou deploy keys zakázané v organizaci!**

Pokud OAuth autorizace nefunguje a deploy keys jsou povolené, použijte deploy key:

### Krok 1: Vygenerujte SSH klíč

**Windows (PowerShell):**
```powershell
# Otevřete PowerShell
ssh-keygen -t ed25519 -C "streamlit-cloud-deploy" -f $env:USERPROFILE\.ssh\streamlit_deploy_key
```

**Při dotazu na passphrase:** Stiskněte Enter (nechte prázdné)

**Linux/Mac:**
```bash
ssh-keygen -t ed25519 -C "streamlit-cloud-deploy" -f ~/.ssh/streamlit_deploy_key
```

### Krok 2: Zkopírujte veřejný klíč

**Windows (PowerShell):**
```powershell
Get-Content $env:USERPROFILE\.ssh\streamlit_deploy_key.pub
```

**Linux/Mac:**
```bash
cat ~/.ssh/streamlit_deploy_key.pub
```

**Zkopírujte celý výstup** (začíná `ssh-ed25519` a končí `streamlit-cloud-deploy`)

### Krok 3: Přidejte Deploy Key na GitHub

1. Jděte na váš GitHub repozitář
2. Klikněte na **Settings** (vpravo nahoře v repozitáři)
3. V levém menu klikněte na **Deploy keys**
4. Klikněte na **Add deploy key**
5. Vyplňte:
   - **Title:** `Streamlit Cloud Deploy`
   - **Key:** Vložte zkopírovaný veřejný klíč
   - ✅ **Zaškrtněte "Allow write access"** (důležité!)
6. Klikněte na **Add key**

### Krok 4: Přidejte Deploy Key do Streamlit Cloud

1. Jděte na [share.streamlit.io](https://share.streamlit.io)
2. Otevřete vaši aplikaci nebo vytvořte novou
3. Jděte na **Settings** (⚙️ ikona)
4. Najděte sekci **"Deploy key"** nebo **"Repository access"**
5. Zkopírujte **soukromý klíč**:

   **Windows (PowerShell):**
   ```powershell
   Get-Content $env:USERPROFILE\.ssh\streamlit_deploy_key
   ```

   **Linux/Mac:**
   ```bash
   cat ~/.ssh/streamlit_deploy_key
   ```

6. Vložte celý obsah soukromého klíče do pole v Streamlit Cloud
7. Uložte nastavení

### Krok 5: Zkuste znovu deploy

- Klikněte na **"Deploy"** nebo **"Redeploy"**
- Mělo by to nyní fungovat

---

## 🚨 Časté problémy

### "Repository not found"
- **Řešení:** Ujistěte se, že máte přístup k repozitáři (jste owner nebo collaborator)
- Zkontrolujte, že repozitář existuje a máte k němu oprávnění

### "Permission denied"
- **Řešení:** Při přidávání deploy key na GitHub zaškrtněte **"Allow write access"**
- Streamlit Cloud potřebuje write přístup pro automatické deploye

### "Invalid key format"
- **Řešení:** Ujistěte se, že kopírujete celý klíč včetně `ssh-ed25519` na začátku
- Zkontrolujte, že nekopírujete veřejný klíč místo soukromého (nebo naopak)

### OAuth stále nefunguje
- **Řešení:** Zkuste použít jiný prohlížeč nebo vymazat cookies
- Nebo použijte deploy key metodu výše

### "Deploy keys are disabled for this organization"
- **Řešení 1:** Použijte GitHub App v Streamlit Cloud Settings (nevyžaduje deploy keys)
- **Řešení 2:** Požádejte organizačního admina o povolení Streamlit Cloud GitHub App
- **Řešení 3:** Použijte osobní fork repozitáře pro deployment
- **Řešení 4:** Kontaktujte Streamlit support - mohou mít řešení pro enterprise účty

---

## 💡 Tipy

1. **Pro veřejné repozitáře:** OAuth autorizace by měla fungovat automaticky
2. **Pro soukromé repozitáře:** Buď použijte OAuth s oprávněním, nebo deploy key
3. **Pro organizační repozitáře:** Použijte GitHub App místo deploy keys
4. **Bezpečnost:** Deploy key je bezpečný - má přístup pouze k jednomu repozitáři
5. **GitHub App:** Streamlit Cloud také podporuje GitHub Apps, které jsou ještě bezpečnější a nevyžadují deploy keys

---

## 📞 Potřebujete pomoc?

- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-community-cloud)
- [GitHub Deploy Keys Guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/managing-deploy-keys)
- Zkontrolujte také `DEPLOYMENT_GUIDE.md` pro kompletní průvodce

