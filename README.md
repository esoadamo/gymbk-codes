# Kód do programování @ GymBk.cz

Základní kódy probírané v hodinách

## Jak začít

### 1. Naklonování repozitáře

Otevři terminál (PowerShell) a spusť:

```powershell
git clone https://github.com/esoadamo/gymbk-codes.git
cd gymbk-codes
```

Pokud nemáš nainstalovaný Git, stáhni si ho z [git-scm.com](https://git-scm.com/download/win).

### 2. Instalace uv (správce Python balíčků)

V PowerShellu spusť:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Po instalaci zavři a znovu otevři terminál, aby se `uv` přidalo do PATH.

Ověření instalace:

```powershell
uv --version
```

### 3. Spuštění projektu

```powershell
uv run main.py
```

`uv` automaticky vytvoří virtuální prostředí a nainstaluje potřebné závislosti.