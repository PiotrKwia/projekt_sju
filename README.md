<!-- LTeX: language=pl-PL -->

# Projekt Sieć Jako Usługa

Repozytorium stanowi punkt startowy projektu z przedmiotu "Sieć Jako Usługa".
Przedmiotem projektu jest przygotowanie kontenera zawierającego narzędzia developerskie, konfiguracja prostego przepływu CI/CD, a następnie wykorzystanie przygotowanego środowiska do realizacji raportu.
Do realizacji zadania nie jest potrzebna instalacja lokalna żadnych narzędzi — wystarczy przeglądarka internetowa. Wszystkie pozostałe zasoby są dostępne nieodpłatnie i znajdują się w chmurze.

Dalej znajdziesz instrukcje jak osiągnąć kolejne kamienie milowe.

## 1. Przygotowanie repozytorium projektu na [GitHub](https://github.com)

- Załóż konto na `GitHub` skojarzone z Twoim uczelnianym adresem e-mail.
- Wykonaj **Fork** niniejszego repozytorium na Swoje konto.
- Sprawdź, czy obraz Docker'a buduje się poprawnie (czyli bez błędów):
  - otwórz repozytorium w Codespaces,
  - Uruchom terminal. W terminalu wydaj komendę
    ```bash
    docker build -t sjuprojekt .
    ```
  - Wejdź do kontenera komendą.
    ```bash
    docker run -it --rm -v .:/home/vscode/workspace sjuprojekt bash
    ```
    Sprawdź komendą `ls /home/vscode/workspace`, czy widoczne są pliki projektu.
- Jeżeli budowanie zakończyło się sukcesem, możesz przystąpić realizacji następnego etapu.

## 2. Modyfikacja Dockerfile

- W Codespace zainstaluj rozszerzenie Docker, która znacznie ułatwia pracę z plikami konfiguracyjnymi Docker'a oraz umożliwia zarządzanie obrazami i kontenerami.
- Zmodyfikuj plik `Dockerfile`, aby zawierał instalację pakietów: `Qiskit`, `Matplotlib`, `Pillow`, `Pycryptodomex`, `Cryptography`. Możesz użyć polecenia `pip install` w odpowiedniej sekcji `Dockerfile`.
- Ponownie zbuduj obraz. Możesz przejść do następnego punktu, gdy obraz buduje się poprawnie.

## 3. Kontener developerski

- Utwórz plik `.devcontainer/devcontainer.json` o treści
  ```json
  {
    "workspaceMount": "source=${localWorkspaceFolder},target=/home/vscode/workspace,type=bind,consistency=cached",
    "workspaceFolder": "/home/vscode/workspace",
    "name": "Projekt-SJU",
    "image": "sjuprojekt",
    "customizations": {
      "vscode": {
        "extensions": ["ms-python.python", "ms-toolsai.jupyter"]
      }
    },
    "postCreateCommand": "pip install --no-cache-dir -r requirements.txt && uname -a && python --version && pip --version",
    "remoteUser": "vscode"
  }
  ```
- Otwórz repozytorium w kontenerze developerskim: `Ctrl+Shift+P` i wpisz `devcontainer`.
- Otwórz rozszerzenia i dodaj następujące rozszerzenia do kontenera: `Markdown All in One`, `Marp for VS Code`, `GitHub Actions`.
- Wybierz `Rebuild Container`.
- Jeżeli kontener zbudował się poprawnie, możesz wypchnąć wszystkie modyfikacje do repozytorium i zakończyć pracę z Codespaces. Nie zapomnij zatrzymać i ewentualnie skasować wirtualnej maszyny w chmurze.

## 4. GitHub Action

- Otwórz repozytorium w przeglądarce.
- Dodaj akcję `Build and Publish Docker Image`. Jako rejestr obrazów wybierz `ghcr.io`. W przeciwnym razie byłoby konieczne założenie konta na Docker Hub.
- Skonfiguruj akcję tak, aby uruchamiała się automatycznie po utworzeniu znacznika wersji (`release`) lub ręcznie (`workflow_dispatch`). W razie potrzeby skorzystaj z gotowych szablonów GitHub Actions.
- Doprowadź do sytuacji, w której wszystko przebiega bezbłędnie.
- Dodaj do akcji test sprawdzający poprawność zbudowanego obrazu:

  - w katalogu głównym repozytorium utwórz plik `test.py` o treści

    ```python
    def test_imports():
    packages = [
        "qiskit",
        "matplotlib",
        "PIL",  # Pillow
        "Cryptodome",  # Pycryptodomex
        "cryptography"
    ]

    for pkg in packages:
        try:
            __import__(pkg)
            print(f"✅ {pkg} - OK")
        except ImportError:
            print(f"❌ {pkg} - MISSING")
            exit(1)

    if __name__ == "__main__":
        test_imports()
    ```

  - W pliku akcji w miejscu po przygotowaniu środowiska budowania a przed jego wysłaniem do rejestru dodaj fragment

    ```yml
      - name: Set up Docker
        uses: docker/setup-buildx-action@v3
      # początek testu
      - name: Build Docker image
        run: docker build -t sjuprojekt .

      - name: Run test script inside container
        run: |
          docker run --rm sjuprojekt python /home/vscode/workspace/test.py
          - name: Build Docker image
        run: docker build -t sjuprojekt .

      - name: Run test script inside container
        run: |
          docker run --rm sjuprojekt python /home/vscode/workspace/test.py
      # koniec testu
      - name: Log into registry ${{ env.REGISTRY }}
    ```

- Ponownie uruchom akcję i w logach sprawdź, czy sprawdzenie przebiegło poprawnie.
- W pliku `.devcontainer/devcontainer.json` zmień wpis `image:` na taki, który wskazuje nowo zbudowany obraz w rejestrze `GitHub`.

### Notka nt. interfejsu użytkownika `GitHub Action`

<!-- LTeX: language=en-US -->

When **at least one workflow already exists** in `.github/workflows/`, GitHub **hides the “template gallery”** on the **Actions** tab.

But no worries — here are **3 alternative ways** to access and use GitHub’s official Action templates, even when one is already defined:

#### ✅ Option 1: Manually add a new workflow file

1. Go to your repo's `Code` tab.
2. Navigate to `.github/workflows/`.
3. Click **“Add file” → “Create new file”**.
4. Name it, e.g., `docker-publish.yml`.
5. Paste a template from the [GitHub Actions starter workflows library](https://github.com/actions/starter-workflows).
6. Commit the new file.

💡 _Starter workflows for Docker:_

- https://github.com/actions/starter-workflows/blob/main/ci/docker-publish.yml

#### ✅ Option 2: Use "New workflow" link directly

Even if the tab hides the gallery, you can **force it** to show the template UI by navigating here manually:

👉 **`https://github.com/<user>/<repo>/actions/new`**

> Replace `<user>` and `<repo>` with your GitHub username and repository name.

This takes you to the **template selection view**, regardless of existing workflows.

#### ✅ Option 3: Copy from GitHub's template repository

GitHub maintains an open-source repo with dozens of ready-to-use action templates:

🔗 [https://github.com/actions/starter-workflows](https://github.com/actions/starter-workflows)

From there, you can:

- Browse templates for CI, Docker, Python, etc.
- Copy-paste the full YAML file into your own `.github/workflows/` folder.

<!-- LTeX: language=pl-PL -->

## 5. Praca z repozytorium w kontenerze developerskim

- Otwórz repozytorium, korzystając z [https://vscode.dev](https://vscode.dev) i aktywuj kontener developerski.
- Załóż podkatalog `sample`, umieść w nim notatnik Jupyter'a, np. używany na przedmiocie `Kwantowe Systemy Teleinformatyki`, i sprawdź, czy się wykonuje.
- Jeżeli wszystko działa możesz przejść do sporządzania **Raportu**.

## 6. Przygotowanie **Raportu**

Raport końcowy należy przygotować w formie prezentacji `MARP`.
Danymi wejściowymi do systemu są nieco zmodyfikowane pliki `Markdown`.
Skład odbywa się w trybie WYSIWYG, tzn. tekst źródłowy `Markdown` jest na bieżąco interpretowany a podgląd aktualizowany.

Szablon prezentacji ma postać

```markdown
---
marp: true
math: mathjax
title: Raport z projektu
size: 16:9
paginate: true
transition: fade
backgroundImage: url("page-background.png")
footer: "**Raport SJU**"
style: |
  @import url('https://unpkg.com/tailwindcss@^2/dist/utilities.min.css');
---

# Slajd 1

## Nagłówek 1

![w:600](obraz.png)

- punkt 1
- punkt 2
- punkt 3

---

# Slajd 2

## Dwie kolumny

<div class="grid grid-cols-2 gap-4 items-start">
<div class="col-span-1">

Kolumna 1

</div><div class="col-span-1">

Kolumna 2

</div>
</div>

<!--
1. Pierwszy komentarz dla prezentującego.
2. Drugi komentarz dla prezentującego.
-->

---

# Slajd 3

## Fragment wycentrowany w poziomie

<div class="flex justify-center">

![W:600](https://some.where.io/some.picture.png)

</div>
```

- W repozytorium utwórz podkatalog `doc`.
- Korzystając z szablonu, utwórz prezentację zawierającą:
  - wypunktowane kroki prowadzące do skutecznej realizacji każdego etapu,
  - szczegóły konfiguracji `Dockerfile`, `GitHub Actions` oraz `devcontainer`,
  - Wstaw diagram Mermaid, np. diagram zależności lub przepływu pracy, używając składni Markdown zgodnej z MARP. W razie trudności skorzystaj z [Mermaid Live Editor](https://mermaid.live).
  - Dodaj slajd z krótkim podsumowaniem, co było najtrudniejsze, czego się nauczyłeś (-aś), co byś zmienił (-a) w konfiguracji. Opcjonalnie: napisz, jak można by rozbudować środowisko, aby poprawić jego walor dydaktyczny.
- Upewnij się, że raport jest przejrzysty i zawiera wszystkie istotne informacje dotyczące projektu.

## 7. Publikacja Raportu

- Wyeksportuj prezentację do pliku HTML.
- W ustawieniach repozytorium aktywuj `GitHub Pages`. Jako metodę publikacji wybierz `GitHub Actions` i wybierz akcję `Static HTML`. Jako publikowany katalog wskaż `doc`. Aktywuj akcję. Sprawdź, czy strona jest dostępna.
- Jeżeli tak, wyeksportuj prezentację to pliku PDF.
- Wykonaj `git rebase` na gałęzi `main`, aby zlinearyzować historię zmian w głównej gałęzi repozytorium. Upewnij się, że nie występują konflikty. Wykonaj `Rebase` na gałęzi `main` repozytorium. Wgraj plik prezentacji na PZE. W adnotacji podaj link do opublikowanej prezentacji.

<!-- LTeX: language=en-US -->

## License

[GNU General Public License v3.0](LICENSE)

This license ensures that all modifications to the software remain open source, prohibiting the creation of closed-source derivatives.
