<h1 align="center">drAIn Backend 🌧️</h1>
<a id="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
<a href="https://github.com/eliseoalcaraz/drAIn-backend/blob/main/LICENSE">
<img alt="License" src="https://img.shields.io/badge/License-GPL--2.0-blue?style=for-the-badge" />
</a>

<div align="center">
  <a href="https://github.com/4Chronosx/BACKEND-DrAin">
    <img src="logo.png" alt="drAIn Backend logo" width="40%" height="35%">
  </a>
  <br />
  <p align="center">
    <a href="#"><img alt="Status" src="https://img.shields.io/badge/status-Beta-yellow?style=flat&color=yellow" /></a>
    <a href="https://www.python.org/"><img alt="Python" src="https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white&style=flat" /></a>
    <a href="https://github.com//4Chronosx/BACKEND-DrAin/commits/main"><img alt="Last commit" src="https://img.shields.io/github/last-commit/4Chronosx/BACKEND-DrAin/?color=coral&logo=git&logoColor=white" /></a>
  </p>
  <a href="https://github.com/4Chronosx/BACKEND-DrAin/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
  &middot;
  <a href="https://github.com/4Chronosx/BACKEND-DrAin/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
</div>

---

## 🗺️ Overview

The **drAIn Backend** powers the simulation engine and API infrastructure for the drAIn platform. Built with **FastAPI** and **PySWMM**, it provides RESTful endpoints for running **SWMM (Storm Water Management Model)** hydraulic simulations, processing drainage system data, and delivering real-time flood vulnerability analytics to the frontend.

This backend transforms complex hydrological modeling into accessible API services, enabling engineers and planners to run sophisticated urban drainage simulations through simple HTTP requests.

---

### 💡 Why This Backend?

Urban flood modeling typically requires specialized software and technical expertise. The drAIn backend democratizes access to SWMM simulations by:

* **Abstracting Complexity**: Wraps SWMM's Python API in intuitive REST endpoints
* **Enabling Real-Time Simulation**: Supports interactive "what-if" scenarios for infrastructure planning
* **Processing at Scale**: Handles data preprocessing and result analysis automatically
* **Cloud-Ready Architecture**: Deployed on Railway for reliable, scalable API access

#### ⚙️ Core Capabilities

* 🌊 **SWMM Simulation Engine**: Python-based hydraulic and hydrological modeling using PySWMM
* 🚀 **High-Performance API**: FastAPI endpoints optimized for concurrent simulation requests
* 📊 **Data Pipeline**: Automated preprocessing of raw drainage data for SWMM inputs
* 🔄 **Scenario Management**: Support for multiple rainfall scenarios and infrastructure configurations
* 📈 **Result Analytics**: Post-processing of simulation outputs for vulnerability ranking

---

## 📚 Tech Stack

### Core Framework
<p align="left">
  <a href="https://fastapi.tiangolo.com/"><img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white&style=flat" /></a>
  <a href="https://www.python.org/"><img alt="Python" src="https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white&style=flat" /></a>
  <a href="https://www.uvicorn.org/"><img alt="Uvicorn" src="https://img.shields.io/badge/Uvicorn-2094F3?logo=gunicorn&logoColor=white&style=flat" /></a>
</p>

### Simulation & ML
<p align="left">
  <a href="https://www.epa.gov/water-research/storm-water-management-model-swmm"><img alt="PySWMM" src="https://img.shields.io/badge/PySWMM-0078D4?logo=python&logoColor=white&style=flat" /></a>
  <a href="https://scikit-learn.org/"><img alt="scikit-learn" src="https://img.shields.io/badge/scikit--learn-F7931E?logo=scikitlearn&logoColor=white&style=flat" /></a>
  <a href="https://numpy.org/"><img alt="NumPy" src="https://img.shields.io/badge/NumPy-013243?logo=numpy&logoColor=white&style=flat" /></a>
  <a href="https://pandas.pydata.org/"><img alt="Pandas" src="https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white&style=flat" /></a>
</p>

### Data Processing
<p align="left">
  <a href="https://colab.research.google.com/"><img alt="Google Colab" src="https://img.shields.io/badge/Google_Colab-F9AB00?logo=googlecolab&logoColor=white&style=flat" /></a>
  <a href="https://jupyter.org/"><img alt="Jupyter" src="https://img.shields.io/badge/Jupyter-F37626?logo=jupyter&logoColor=white&style=flat" /></a>
</p>

### Deployment
<p align="left">
  <a href="https://railway.app/"><img alt="Railway" src="https://img.shields.io/badge/Railway-0B0D0E?logo=railway&logoColor=white&style=flat" /></a>
</p>

---

## 📁 Project Structure

```
BACKEND-DRAIN/
├── __pycache__/           # Python cache files
├── data/                  # SWMM model files and data
│   ├── Mandaue_Drainage_Network_mod.inp
│   ├── Mandaue_Drainage_Network_mod.out
│   ├── Mandaue_Drainage_Network_mod.rpt
│   ├── Mandaue_Drainage_Network.inp
│   ├── Mandaue_Drainage_Network.out
│   ├── Mandaue_Drainage_Network.rpt
│   └── vulnerability_model_k4.pkl
├── Python_Notebooks/      # Data preprocessing notebooks
│   ├── INP_FILE_GENERATOR.ipynb
│   └── KMEANS_MODEL.ipynb
├── tools/                 # Utility scripts
│   ├── __pycache__/
│   ├── swmm_extract.py   # SWMM data extraction
│   └── swmm_tools.py     # SWMM helper functions
├── venv/                  # Virtual environment
├── Procfile              # Process configuration
├── README.md             # This file
├── requirements.txt      # Python dependencies
├── server.py             # FastAPI server
└── test.py               # Test suite
```

---

## 💻 Getting Started

Follow these steps to set up and run the **drAIn Backend** locally.

### 🔧 Prerequisites

Make sure you have installed:

- [Python](https://www.python.org/) (v3.9+)
- [pip](https://pip.pypa.io/) or [conda](https://docs.conda.io/)
- [SWMM](https://www.epa.gov/water-research/storm-water-management-model-swmm) (for local simulations)

---

### 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/4Chronosx/BACKEND-DrAin.git
cd BACKEND-DrAin

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

### 🚀 Running the API

```bash
# Start the FastAPI server
uvicorn uvicorn server:app --reload

# Server will be available at:
# http://localhost:3000
```



## 🔌 API Endpoints

### Simulation Endpoints
- `POST /run-simulation` - Run a new SWMM simulation and Retrieve simulation results

---

## 📊 Data Processing

The `notebooks/` directory contains Google Colab notebooks for:

- **Data Preprocessing**: Converting raw drainage survey data into SWMM-compatible formats
- **Geospatial Processing**: Handling coordinate systems and network topology
- **Data Validation**: Ensuring data quality and completeness
- **Feature Engineering**: Creating inputs for ML-based vulnerability ranking

### 📁 Raw Data Access

Raw datasets used for SWMM simulations are available at:

**[View Raw Data on Google Drive](https://drive.google.com/drive/folders/17EH76KdZrbVCcVJ79D_JurgRywqROQ8E?usp=drive_link)** 📂

---



## 🚂 Railway Deployment

The backend is automatically deployed to Railway and serves the production API:

1. Connect your GitHub repository to Railway
2. Configure environment variables
3. Railway auto-deploys on every push to `main`

**Production API**: `https://pjdsc-drain-backend.up.railway.app`

---

## 📬 Contributing

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 📢 Contributors

<a href="https://github.com/4Chronosx/BACKEND-DrAin/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=4Chronosx/BACKEND-DrAin" alt="contrib.rocks image" />
</a>

---

## ⚖️ License

This project is licensed under the GNU General Public License v2.0 (GPL-2.0).
You may redistribute and/or modify it under the terms of the GNU GPL, as published by the Free Software Foundation - see the [LICENSE](LICENSE) file for details.

---

## 🔗 Related Repositories

- [drAIn Frontend](https://github.com/eliseoalcaraz/drAIn) - Next.js web application

---

<p align="center">Made with 💧 for flood-resilient cities</p>

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/4Chronosx/BACKEND-DrAin.svg?style=for-the-badge
[contributors-url]: https://github.com/4Chronosx/BACKEND-DrAin/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/4Chronosx/BACKEND-DrAin.svg?style=for-the-badge
[forks-url]: https://github.com/4Chronosx/BACKEND-DrAin/network/members
[stars-shield]: https://img.shields.io/github/stars/4Chronosx/BACKEND-DrAin.svg?style=for-the-badge
[stars-url]: https://github.com/4Chronosx/BACKEND-DrAin/stargazers
[issues-shield]: https://img.shields.io/github/issues/4Chronosx/BACKEND-DrAin.svg?style=for-the-badge
[issues-url]: https://github.com/4Chronosx/BACKEND-DrAin/issues

