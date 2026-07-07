# Study RAG Platform Backend

Backend del proyecto Study RAG Platform, una plataforma de apoyo al aprendizaje basada en Retrieval-Augmented Generation (RAG), diseñada para permitir la gestión de documentos académicos, salas de estudio colaborativas, generación de flashcards, exámenes y consultas inteligentes mediante modelos de lenguaje.

## Arquitectura

El proyecto sigue los principios de Arquitectura Hexagonal (Ports and Adapters), promoviendo:

* Separación de responsabilidades.
* Bajo acoplamiento entre capas.
* Facilidad de pruebas.
* Escalabilidad y mantenibilidad.
* Independencia de frameworks y proveedores externos.

## Stack Tecnológico

### Backend

* Python 3.11
* FastAPI
* Pydantic
* SQLAlchemy
* Alembic

### Base de Datos

* PostgreSQL 16

### Inteligencia Artificial

* LangChain
* OpenAI
* Sentence Transformers

### Vector Database

* ChromaDB

### Infraestructura

* Docker
* Docker Compose

## Estructura del Proyecto

```text
app/
├── adapters/
├── application/
├── domain/
├── infrastructure/
├── config/
└── main.py
```

### Domain

Contiene las entidades de negocio, servicios de dominio, repositorios y objetos de valor.

### Application

Contiene casos de uso, comandos, consultas y puertos.

### Adapters

Contiene los controladores y endpoints de FastAPI.

### Infrastructure

Implementaciones concretas de persistencia, autenticación, almacenamiento, RAG y proveedores de IA.


1. Lenin Ramon Lopez Cordova
2. Josue Abraham Un Hernandez
3. Kevin Javier Velazquez
4. Kevin Alejandro Chuc
5. Ramon Avila Mayo
6. Joel Isaac Rodriguez Pech

El proyecto utiliza un flujo de trabajo basado en Git Flow simplificado.

La rama main representa versiones estables y listas para entrega.

La rama develop concentra la integración continua del desarrollo antes de promover cambios a producción.

Las ramas feature/* permiten desarrollar funcionalidades de manera aislada, evitando afectar el código estable.

Las ramas release/* se utilizan para preparar entregas académicas o versiones importantes.

Las ramas hotfix/* permiten corregir errores críticos de forma rápida sin interrumpir el desarrollo principal.

Este flujo facilita el trabajo colaborativo, mejora la trazabilidad de cambios y reduce riesgos durante la integración de nuevas funcionalidades.

## Ejecución Local

### Levantar servicios

```bash
docker compose up --build
```

### Servicios disponibles

Backend:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

PostgreSQL:

```text
localhost:5432
```

ChromaDB:

```text
http://localhost:8001
```

## Git Flow

El proyecto utiliza Git Flow simplificado.

### Ramas principales

```text
main
develop
```

### Ramas de trabajo

```text
feature/*
release/*
hotfix/*
```

## Integración Continua

GitHub Actions ejecuta automáticamente:

* Instalación de dependencias.
* Validación de imports.
* Verificación básica del proyecto FastAPI.

Workflow:

```text
.github/workflows/backend-ci.yml
```

## Estado Actual

### Fase 1

* Arquitectura Hexagonal inicializada.
* Docker configurado.
* Docker Compose configurado.
* FastAPI configurado.
* PostgreSQL configurado.
* ChromaDB configurado.
* Git Flow configurado.
* CI/CD configurado.

## Licencia

Proyecto académico para fines educativos, saludos cordiales profe unu
