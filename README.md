# Bike Zone — Base de Datos
Sistema de gestión de órdenes para una cadena de tiendas de bicicletas. Desarrollado con PostgreSQL en Supabase y operaciones CRUD en Python.

Fuente de datos: Bike Store Sample Database — Kaggle: https://www.kaggle.com/datasets/dillonmyrick/bike-store-sample-database
Los datos fueron adaptados y estructurados en PostgreSQL con tablas, constraints, claves primarias y foráneas propias.


---

## Estructura del proyecto

```
bike-zone/
│
├── README.md
├── .gitignore
├── squema.sql
├── crud.py
│
├── images/                    
│   ├── erd.png
│   ├── categorias.png
│   ├── clientes.png
│   ├── tiendas.png
│   ├── productos.png
│   ├── ordenes.png
│   └── detalle_ordenes.png
│
```

---

## Diagrama Entidad-Relación (ERD)

> Generado desde el Schema Visualizer de Supabase

<img width="952" height="742" alt="595107241-2b136d6e-7c6b-4559-8af6-393302425b9e" src="https://github.com/user-attachments/assets/a207b710-a0e4-4345-a1c9-109f675a9c3a" />


---

## Tablas

| Tabla | Descripción |
|---|---|
| `categorias` | Tipos de productos (Mountain Bikes, Road Bikes, etc.) |
| `productos` | Catálogo de bicicletas y accesorios con precio y stock |
| `clientes` | Compradores registrados con teléfono único de 10 dígitos |
| `tiendas` | Sucursales de la cadena Bike Zone |
| `ordenes` | Pedidos realizados por clientes en una tienda |
| `detalle_ordenes` | Productos específicos dentro de cada orden |

---

## Datos de las tablas

### categorias
<img width="572" height="417" alt="Captura de pantalla 2026-05-20 212703" src="https://github.com/user-attachments/assets/61721a0a-57c8-41b0-9b4d-dc5424ba7fd6" />


### clientes
<img width="1182" height="372" alt="Captura de pantalla 2026-05-20 212722" src="https://github.com/user-attachments/assets/29ea5b92-a22d-459d-ae8f-012313274a91" />


### tiendas
<img width="1162" height="413" alt="Captura de pantalla 2026-05-20 212819" src="https://github.com/user-attachments/assets/6704146e-e4a6-4b96-8ed6-7acaa379541e" />


### productos
<img width="1097" height="412" alt="Captura de pantalla 2026-05-20 212807" src="https://github.com/user-attachments/assets/0f7d1df0-631b-40b7-bed7-d06fa3a93d89" />


### ordenes
<img width="1223" height="415" alt="Captura de pantalla 2026-05-20 212755" src="https://github.com/user-attachments/assets/d404d35a-6b8b-402e-bf2b-c59340ce9e71" />


### detalle_ordenes
<img width="1017" height="421" alt="Captura de pantalla 2026-05-20 212738" src="https://github.com/user-attachments/assets/ec056464-1336-4d7e-9fb5-a7018432bf4c" />


---

## Schema SQL

Ver archivo (https://github.com/sofiaduque024/TrabajoFinalBD/blob/main/schema.sql)
---

## Constraints aplicados

| Tabla | Columna | Tipo | Detalle |
|---|---|---|---|
| `clientes` | `telefono_cliente` | `UNIQUE` + `CHECK` | Único y exactamente 10 dígitos |
| `tiendas` | `telefono_tienda` | `UNIQUE` + `NOT NULL` | Único y obligatorio |
| `productos` | `precio_producto` | `CHECK > 0` | No puede ser negativo ni cero |
| `productos` | `stock` | `CHECK >= 0` | No puede ser negativo |
| `ordenes` | `estado_orden` | `CHECK IN (...)` | Solo: Pendiente, Procesando, Enviado, Entregado, Cancelado |
| `detalle_ordenes` | `cantidad_compra` | `CHECK > 0` | Debe ser mayor a cero |
| `detalle_ordenes` | `precio_unitario` | `CHECK > 0` | Debe ser mayor a cero |

---

## Claves Foráneas

| Tabla | Columna FK | Tabla referenciada | Columna referenciada |
|---|---|---|---|
| `productos` | `id_categoria` | `categorias` | `id_categoria` |
| `ordenes` | `id_cliente` | `clientes` | `id_cliente` |
| `ordenes` | `id_tienda` | `tiendas` | `id_tienda` |
| `detalle_ordenes` | `id_orden` | `ordenes` | `id_orden` |
| `detalle_ordenes` | `id_producto` | `productos` | `id_producto` |

---

## Relaciones

```
categorias ──< productos
clientes   ──< ordenes
tiendas    ──< ordenes
ordenes    ──< detalle_ordenes
productos  ──< detalle_ordenes
```

---

## CRUD en Python


---

## Procedimientos almacenados, Triggers e Índices



---

## Stack tecnológico

- **Base de datos:** PostgreSQL (Supabase)
- **CRUD:** Python con `psycopg2`
- **Plataforma:** Supabase

---
