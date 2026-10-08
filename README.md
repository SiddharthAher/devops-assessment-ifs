# DevOps Take-Home Assessment – Kubernetes Notes API

## 1. Overview

This project demonstrates the deployment of a containerized FastAPI application and PostgreSQL database on a local Kubernetes cluster.

The application provides APIs to create and retrieve notes and includes a health endpoint. PostgreSQL data is stored using a Kubernetes PersistentVolumeClaim so that data remains available after PostgreSQL pod recreation.

## 2. Environment

| Component | Details |
|---|---|
| Operating System | Windows 11 |
| Kubernetes Distribution | Docker Desktop Kubernetes |
| Kubernetes Version | v1.29.1 |
| Application | FastAPI |
| Database | PostgreSQL 16 |
| Container Runtime | Docker |
| Namespace | `takehome` |

Docker Desktop Kubernetes was selected as the local Kubernetes distribution for running the assessment locally.

## 3. Architecture

```text
                    Windows 11
                        |
                 Docker Desktop
                        |
                Kubernetes v1.29.1
                        |
                  takehome namespace
                    /          \
                   /            \
          FastAPI Application   PostgreSQL
             2 replicas          1 replica
                  |                  |
             NodePort 30080       ClusterIP
                  |                  |
             HTTP API            PostgreSQL
                                     |
                                  1Gi PVC