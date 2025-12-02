# Proyecto Final – Sistemas Distribuidos  
## Generación de Números Primos por Microservicios

Este proyecto implementa un sistema distribuido basado en **microservicios**, **colas de tareas**, **workers**, **almacenamiento persistente**, y comunicación entre servicios para generar números **primos grandes (12 dígitos o más)** garantizando:

- Algoritmo **100% determinista** para primalidad  
- No repetir números dentro de una misma solicitud  
- Escalabilidad agregando más workers  
- Separación real por servicios: `New`, `Status`, `Result`

---

# 🏗 Arquitectura del Sistema

El sistema está compuesto por:

### **1. Microservicios**
- **New Service (puerto 8001)**  
  Recibe solicitudes indicando cuántos primos y de cuántos dígitos generar.  
  Encola la tarea en Redis.  

- **Status Service (puerto 8002)**  
  Consulta cuántos primos se han generado para una solicitud.  

- **Result Service (puerto 8003)**  
  Devuelve todos los primos generados para un `request_id`.

---

### **2. Cola de Mensajes**
- **Redis**  
  Contiene la cola `prime_tasks`.  
  Los workers extraen tareas desde allí, garantizando desacoplamiento.

---

### **3. Worker**
- Toma tareas de Redis (`BLPOP`).
- Genera números primos usando Miller–Rabin determinista para < 2^64.
- Inserta resultados en PostgreSQL.
- Evita duplicados con un `UNIQUE(request_id, prime)`.

---

### **4. Base de Datos**
- **PostgreSQL**
- Tabla única:
  ```sql
  CREATE TABLE primes (
    id SERIAL PRIMARY KEY,
    request_id VARCHAR(64),
    prime TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(request_id, prime)
  );
   
### 5. Contenedores
- todo corre con Docker Compose, que levanta:
    PostgreSQL
    Redis
    Worker
    New Service
    Status Service
    Result Service