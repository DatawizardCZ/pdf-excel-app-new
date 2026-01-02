"""Debug test"""

import re

# Testovací řádky
test_lines = [
    '85533 2521844167325 Dværghamster - Blå 2,92 1 5 5',
    '85882 252130650420 Dværghamster - Marmor 3,19 1 5 5',
    '85064 2522428497128 Marsvin 8,03 4 1 4',
]

for line in test_lines:
    print(f"\nTestování řádku: {line}")
    parts = line.split()
    print(f"  Počet částí: {len(parts)}")
    print(f"  Části: {parts}")
    
    if len(parts) < 5:
        print("  ❌ Méně než 5 částí, přeskočeno")
        continue
    
    # První část: číslo položky
    if parts[0].isdigit():
        print(f"  ✓ Číslo položky: {parts[0]}")
        parts = parts[1:]
    else:
        print("  ❌ První část není číslo")
        continue
    
    # Druhá část: čárový kód
    if parts and parts[0].isdigit() and len(parts[0]) >= 10:
        print(f"  ✓ Čárový kód: {parts[0]} (délka: {len(parts[0])})")
        parts = parts[1:]
    else:
        print(f"  ❌ Druhá část není čárový kód: {parts[0] if parts else 'N/A'} (délka: {len(parts[0]) if parts and parts[0].isdigit() else 'N/A'})")
        continue
    
    # Zbytek
    remaining = ' '.join(parts)
    print(f"  Zbytek: {remaining}")
    
    numbers = re.findall(r'\d+[.,]\d+|\d+', remaining)
    print(f"  Nalezená čísla: {numbers}")
    
    if numbers:
        first_num = numbers[0]
        first_num_pos = remaining.find(first_num)
        print(f"  Pozice prvního čísla: {first_num_pos}")
        
        if first_num_pos >= 0:
            description = remaining[:first_num_pos].strip()
            print(f"  ✓ Popis: {description}")
        else:
            print("  ❌ Popis nenalezen")
    else:
        print("  ❌ Žádná čísla")

