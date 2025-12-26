# Latent Platform

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Team](https://img.shields.io/badge/Team-Quantum%20Breaker-purple.svg)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)

## 📖 Project Overview

**Latent Platform** addresses a critical problem in the student developer ecosystem: **The GitHub Graveyard.**

Every year, thousands of incredible engineering projects are built for hackathons, capstones, and assignments. However, once the event is over, these projects sit dormant in repositories because they are difficult for recruiters, investors, or non-technical users to run. Testing a student project usually requires cloning code, installing dependencies, and resolving complex environment errors.

**Latent Platform solves this by combining a discovery marketplace with instant containerization.** It allows any user to browse student projects and launch them instantly in a sandboxed cloud environment. No `git clone`, no `npm install`—just click and test.

### 🚀 Key Features

* **Instant "Live" Demos:** Spins up temporary Docker containers for every project, allowing users to interact with the application immediately in their browser.
* **The "Graveyard" Marketplace:** A curated feed where student developers can revive their old projects and gain visibility.
* **Universal Sandbox:** Supports multiple stacks (Python, Node, Go) via standardized Docker configurations.
* **Recruiter-Ready Portfolios:** Generates interactive portfolios where hiring managers can see the code running live, proving the developer's skills.

---

## 🛠️ Tech Stack

* **Containerization:** Docker & Docker Compose
* **Backend:** Python (FastAPI)
* **Database:** PostgreSQL


---

## ⚙️ Installation & Setup

This project is fully containerized. You do not need to install language runtimes or databases manually.

### Prerequisites

* **Git**
* **Docker Engine** (or Docker Desktop) - [Download Here](https://www.docker.com/products/docker-desktop/)

### Steps to Run

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/AmanGour83/GraveYard.git](https://github.com/AmanGour83/GraveYard.git)
    cd latent-platform
    ```


3.  **Build and Run with Docker**
    Run the following command to build the images and start the services:
    ```bash
    docker-compose up --build
    ```

4.  **Access the Application**
    * API Documentation: `http://localhost:8000/docs`
    * Web Interface: `http://localhost:8000` (or your configured port)

---

## 👥 Team Quantum Breaker

* **Karan Sahni** - *Lead Engineer, Architecture and Backend*
* **Aman Gour** - *Frontend Developer*
* **C. Suraj Kumar** - *Backend Developer*

---

## 🏆 Competitions & Goals

* **Microsoft Imagine Cup 2026** - *Target Submission*
* **Major League Hacking (MLH)** - *Hackathon Prototype*

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
