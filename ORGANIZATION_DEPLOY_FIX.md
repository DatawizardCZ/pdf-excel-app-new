# 🏢 Řešení: Deploy keys zakázané v GitHub organizaci

## 🎯 Rychlé řešení (3 kroky)

### Krok 1: Otevřete Streamlit Cloud Settings
1. Jděte na [share.streamlit.io](https://share.streamlit.io)
2. Otevřete vaši aplikaci
3. Klikněte na **Settings** (⚙️ ikona)

### Krok 2: Nainstalujte GitHub App
1. V Settings najděte sekci **"GitHub App"** nebo **"Repository access"**
2. Klikněte na **"Install GitHub App"** nebo **"Configure GitHub App"**
3. Budete přesměrováni na GitHub

### Krok 3: Autorizujte na GitHub
1. Na GitHub vyberte vaši **organizaci**
2. Vyberte **repozitář** (nebo "All repositories")
3. Klikněte na **"Install"** nebo **"Authorize"**
4. Vraťte se na Streamlit Cloud a zkuste znovu **Deploy**

---

## ✅ Proč to funguje?

- **GitHub App** nevyžaduje deploy keys
- Funguje i když jsou deploy keys zakázané v organizaci
- Je bezpečnější než deploy keys
- Automaticky spravuje oprávnění

---

## 🚨 Pokud GitHub App není dostupný

### Možnost 1: Požádejte organizačního admina

Pošlete adminovi tuto zprávu:

```
Ahoj,

potřebuji nasadit aplikaci na Streamlit Cloud z našeho organizačního 
repozitáře [REPO_NAME]. Streamlit Cloud potřebuje přístup přes GitHub App.

Můžeš prosím:
1. Povolit Streamlit Cloud GitHub App v organizačních nastaveních?
   Nebo
2. Dočasně povolit deploy keys pro tento repozitář?

Díky!
```

### Možnost 2: Použijte osobní fork

1. **Vytvořte fork do osobního účtu:**
   - Na GitHub klikněte na **Fork** v pravém horním rohu
   - Vyberte svůj osobní GitHub účet

2. **Deploy z osobního forku:**
   - V Streamlit Cloud vytvořte novou aplikaci
   - Vyberte váš osobní fork repozitáře
   - Deploy by měl fungovat (deploy keys nejsou zakázané v osobních účtech)

3. **Synchronizace změn (volitelné):**
   - Pravidelně synchronizujte změny z organizačního repozitáře
   - Nebo použijte GitHub Actions pro automatickou synchronizaci

### Možnost 3: Kontaktujte Streamlit Support

- Email: support@streamlit.io
- Nebo přes [Streamlit Community Forum](https://discuss.streamlit.io/)
- Vysvětlete situaci: "Deploy keys are disabled in our organization, need alternative authentication method"

---

## 📋 Checklist

- [ ] Zkusil jsem GitHub App v Streamlit Cloud Settings
- [ ] GitHub App je nainstalovaný a autorizovaný
- [ ] Zkusil jsem znovu deploy
- [ ] Pokud nefunguje, kontaktoval jsem organizačního admina
- [ ] Nebo vytvořil osobní fork pro deployment

---

## 💡 Tipy

1. **GitHub App je nejlepší řešení** - nevyžaduje deploy keys a je bezpečnější
2. **Osobní fork** je dobrá alternativa, pokud nemůžete použít GitHub App
3. **Kontaktujte admina** - často mohou rychle vyřešit problém v organizačních nastaveních
4. **Streamlit Support** může pomoci s enterprise řešeními

---

## 🔗 Užitečné odkazy

- [Streamlit Cloud GitHub App Documentation](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/connect-your-github-account)
- [GitHub Apps vs Deploy Keys](https://docs.github.com/en/apps/creating-github-apps/about-creating-github-apps)
- [Streamlit Community Forum](https://discuss.streamlit.io/)

---

**Poznámka:** Pokud OAuth už funguje, ale stále vidíte chybu o deploy key, zkuste v Streamlit Cloud Settings přepnout z "Use deploy key" na "Use OAuth token" nebo použít GitHub App.












