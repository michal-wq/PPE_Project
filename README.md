# 🎬 Movdex – Interactive Film Recommendation System

**Movdex** is an interactive web app that lets users explore movies, select their favorites, and receive personalized recommendations – all within a clean and intuitive Dash interface.

Developed as part of a university project at the **University of Applied Sciences of the Grisons (FHGR)**.

## 📌 What is Movdex?

Movdex demonstrates how to build an intelligent movie recommendation system using:

- Python & Dash (Plotly)
- MovieLens metadata
- Dynamic user interaction and stateful session logic
- Clean frontend logic without traditional JavaScript frameworks

## 👨‍💻 Created By

- **Filip Vrlec**
- **Michał Ryszard Karczmarzyk**
- **Alessio Luigi De Icco**

> **University of Applied Sciences of the Grisons (FHGR)**  
> Pulvermühlestrasse 57  
> 7000 Chur, Switzerland

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/movdex.git
cd movdex
```

### 2. Set Up Python Environment

We recommend using a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If you don’t have the requirements.txt yet, download requirements.py from this repository and run:

```bash
python requirements.py > requirements.txt
```

### 4. Run the app

```bash
python -m src.main
```

Then open your browser at:

```
http://127.0.0.1:8050/
```

---

### 📂 Project Structure

```
.
├── Data/
│   ├── raw/                    # Original MovieLens data (movies, links, ratings, tags)
│   ├── preprocessed/           # Cleaned feature and label data
│   ├── preprocessed_cluster/   # Clustered feature data
│   └── visdata/                # Aggregated data for visualisation
├── src/
│   ├── main.py                 # Dash app entry point
│   ├── state.py                # Global app state (film cache, user inputs, etc.)
│   ├── proper_recoomendation.py
│   ├── assets/                 # Icons, logo, styles
│   └── pages/                  # Dash page modules
│       ├── home.py
│       ├── search.py
│       ├── evaluation.py
│       ├── visualisation.py
│       └── imprint.py
├── requirements.txt
├── requirements.py
├── README.md
└── unused/                     # (contains experiments, notebooks, old scripts) [not shown]
```

### 📚 Data Source

Movie metadata is based on MovieLens,
provided by the GroupLens research lab at the University of Minnesota.

All rights to the data remain with their original owners.

---

### ⚠️ Disclaimer

- This is a non-commercial student project.
- No personal user data is collected or stored.
- The site is intended purely for academic and demonstration purposes.

---

### Q&A

1. Wer wäre die Zielgruppe für dieses Tool?

- Die Zielgruppe sind technikinteressierte Filmfans sowie Studierende und Dozierende, die sich für Recommender-Systeme, interaktive Webapplikationen oder Datenvisualisierung im Bereich Film interessieren. Das Tool richtet sich auch an Personen, die gerne neue Filme entdecken und Empfehlungen auf Basis ihrer Präferenzen erhalten möchten – ohne Registrierung oder Dateneingabe.
  <br>
  <br>

2. Welche Analysen sind vorgesehen?

- Visualisierung von Genre-Verteilungen
- Auswertung von Nutzerpräferenzen über ausgewählte Filme
  <br>
  <br>

3. Wie gross sind die Daten?

- `movies.csv` an sich beinhaltet 87'585 Einträge
- `tags.csv` an sich beinhaltet 200'072 Einträge
- Es gibt 13 verschiedene Rating-Dateien, da es so viele gab, dass wir es splitten musste, damit wir es auf GitHub hochladen konnten
  <br>
  <br>

4. Warum wird Userdata ignoriert?

- Userdata wird ignoriert, weil sie nicht für alle Filme gleichmässig vorhanden sind. Bei manchen fehlen sie komplett, bei anderen gibt es sehr viele. Daher konzentrieren wir uns bewusst auf Genre-Informationen, um konsistente und vergleichbare Empfehlungen zu ermöglichen.“
  <br>
  <br>

### © License & Usage

© 2025 Filip Vrlec, Michał Ryszard Karczmarzyk, Alessio Luigi De Icco
All rights reserved unless otherwise stated.
