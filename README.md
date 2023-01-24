# Small Company CRM - SCC Project

![visitors](https://visitor-badge.laobi.icu/badge?page_id=MKraynikov.small_company_CRM)
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=102)](https://github.com/ellerbrock/open-source-badge/)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/MKraynikov/small_company_CRM/admin.yml?label=admin_panel)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/MKraynikov/small_company_CRM/backend.yml?label=backend)
![GitHub branch checks state](https://img.shields.io/github/checks-status/MKraynikov/small_company_CRM/master)

CRM for small companies (up to 50 people). Designed to manage the structure 
of the company, organize tasks, inventory control, directories and internal
communication.

## 🔧 Technologies & Tools
![](https://img.shields.io/badge/Code-Python-informational?style=flat&logo=python&logoColor=white&color=2bbc8a)
![](https://img.shields.io/badge/Code-Django-informational?style=flat&logo=django&logoColor=white&color=2bbc8a)
![](https://img.shields.io/badge/Code-FastAPI-informational?style=flat&logo=FastAPI&logoColor=white&color=2bbc8a)
![](https://img.shields.io/badge/Shell-Bash-informational?style=flat&logo=gnu-bash&logoColor=white&color=2bbc8a)
![](https://img.shields.io/badge/Tools-PostgreSQL-informational?style=flat&logo=postgresql&logoColor=white&color=2bbc8a)
![](https://img.shields.io/badge/Tools-Docker-informational?style=flat&logo=docker&logoColor=white&color=2bbc8a)
![](https://img.shields.io/badge/Tools-Redis-informational?style=flat&logo=redis&logoColor=white&color=2bbc8a)
![](https://img.shields.io/badge/Tools-Elasticsearch-informational?style=flat&logo=elasticsearch&logoColor=white&color=2bbc8a)

## Build project

Clone the repository
```
git clone git@github.com:MKraynikov/small_company_CRM.git
```

Go to the project folder
```
cd csmall_company_CRM
```

Copy the settings file and make the necessary changes
```
cp .env.example .env_docker
```

Run the containers
```
docker compose up -d --build
```

## Project URLS
Admin panel: [http://localhost:8086/admin](http://localhost:8086/admin)
```
login: admin
pass: admin
```
Documentation: [http://localhost:8086/docs](http://localhost:8086/docs)<br>
API endpoints: [http://localhost:8086/api/openapi](http://localhost:8086/api/openapi)
