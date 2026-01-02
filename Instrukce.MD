# Instrukce k projektu: Převod PDF objednávek do Excelu

## Cíl projektu
Převést PDF soubory s klientskými objednávkami do Excelové tabulky pro import do interního systému.

## Vstupní data
- PDF soubory s objednávkami (formát: `Købsrekvisition [číslo] [zkratka].pdf`)
- Každý PDF soubor představuje jednu objednávku

## Požadavky na řešení

### 1. Excelová šablona s Power Query
- Vytvořit Excelovou šablonu s Power Query pro automatické zpracování PDF souborů
- Umožnit konfiguraci cesty k PDF souborům (buď fixní složka, nebo konfigurovatelná cesta)
- Každé PDF se zpracuje do samostatného Excelového souboru (1 PDF = 1 Excel)
- Řešení musí umět zpracovávat více souborů postupně

### 2. Zpracování hlaviček (headers)
**DŮLEŽITÉ:** Headery v PDF souborech se mohou lišit podle jazyka:
- Některé PDF mají headery v **dánštině**
- Jiné PDF mají headery v **angličtině**
- **Řešení:** Headery musí být pojmenovány samostatně (ne spoléhat na původní názvy sloupců v PDF)

### 3. Zpracování víceřádkových položek
**DŮLEŽITÉ:** Některé položky v objednávkách obsahují **dva řádky**:
- První řádek: hlavní informace o položce
- Druhý řádek: upřesňující informace k položce
- **Řešení:** Transformace musí zajistit, že druhý řádek bude v **separátním sloupci**

### 4. Výstupní formát
- Každé PDF → samostatný Excel soubor
- Data strukturovaná tak, aby byla připravena pro import do interního systému
- Pojmenované sloupce (nezávisle na jazyce původních headerů)

## Výstup
Vytvořit dokumentaci a Excelovou šablonu tak, aby kolegyně, která na projektu bude pracovat:
1. Věděla, co má dělat
2. Rozuměla výstupu
3. Mohla na projektu okamžitě začít pracovat

## Technické požadavky
- Excel s podporou Power BI a Power Query
- Automatizované zpracování PDF → Excel
- Flexibilní řešení pro různé jazykové varianty
- Zpracování víceřádkových položek s upřesňujícími informacemi

## Budget
- 14 000 - 
