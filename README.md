# Patrones de software
Requiere Python 3.10 o superior. No requiere paquetes externos.
Aplicaciones de consola académicas: mantienen objetos en memoria; no incluyen base de datos ni servidor.

## Ejecutar en PowerShell
Desde la carpeta del proyecto:
~~~powershell
python --version
python caso1.py auto
python caso1.py camioneta --capacidad-kg 1000
python caso1.py camion --tonelaje 8
python caso1.py auto --placa ABC-1234 --marca Toyota --modelo Corolla --anio 2022 --avaluo 20000
python caso2.py
python -m unittest -v
~~~
Las fórmulas de matrícula son ejemplos académicos, no tarifas oficiales.
No hace falta desplegar un servidor: los comandos ejecutan los programas localmente.

## Caso 1: problema y justificación
El cliente selecciona un vehículo durante la ejecución. Construir clases concretas dentro del proceso de negocio lo acoplaría a cada variante.
Factory Method delega esa creación a creadores especializados; el cálculo utiliza el contrato Vehiculo.

Participantes:
- Producto abstracto: Vehiculo.
- Productos concretos: Auto, Camioneta y Camion.
- Creador abstracto: CreadorVehiculo.
- Creadores concretos: CreadorAuto, CreadorCamioneta y CreadorCamion.
- Cliente: main; procesar usa el método de fábrica y el contrato común.
- CREADORES centraliza la configuración de creadores.

Para añadir variantes se agregan producto, creador y registro. Si requieren nuevos argumentos de consola, también se amplía el parser; el proceso común permanece igual.

~~~mermaid
classDiagram
    Vehiculo <|-- Auto
    Vehiculo <|-- Camioneta
    Vehiculo <|-- Camion
    class Vehiculo {
        <<abstract>>
        +str placa
        +str marca
        +str modelo
        +int anio
        +float avaluo
        +calcular_matricula() float
    }
    class Camioneta {
        +float capacidad_kg
        +calcular_matricula() float
    }
    class Camion {
        +float tonelaje
        +calcular_matricula() float
    }
    class Auto {
        +calcular_matricula() float
    }
    class CreadorVehiculo {
        <<abstract>>
        +crear_vehiculo(datos) Vehiculo
        +procesar(datos) tuple
    }
    CreadorVehiculo <|-- CreadorAuto
    CreadorVehiculo <|-- CreadorCamioneta
    CreadorVehiculo <|-- CreadorCamion
    CreadorAuto ..> Auto : crea
    CreadorCamioneta ..> Camioneta : crea
    CreadorCamion ..> Camion : crea
    Cliente --> CreadorVehiculo
    CreadorVehiculo ..> Vehiculo
~~~

### Uso crítico de IA (propuesta para revisión del grupo)
Prompt principal: Implementa en Python Factory Method para autos, camionetas y camiones, con datos comunes, cálculos polimórficos y selección durante la ejecución. Incluye validaciones, UML y pruebas. Identifica las fórmulas ilustrativas.
Recomendación aceptada: utilizar una abstracción Vehiculo y creadores concretos.
Justificación: concentra la construcción y mantiene el cálculo común desacoplado de las variantes.
Recomendación modificada: usar una estructura con todos los atributos, incluidos los que no aplican.
Justificación: cada producto recibe solo sus datos; se evita exigir tonelaje a un auto y se validan las capacidades correspondientes.

## Caso 2: problema y justificación
Los activos requieren tres datos obligatorios y múltiples opcionales. Una lista de parámetros posicionales o muchos constructores sobrecargados dificultaría la lectura.
Builder permite construirlos progresivamente con métodos explícitos y validar el resultado.

Participantes:
- Producto: ActivoFijo.
- Builder concreto: ActivoFijoBuilder.
- Cliente: main.
- Director: no se necesita en esta variante fluida.

El precio utiliza Decimal. El producto es inmutable y copia las características; reutilizar el builder no altera productos anteriores.

~~~mermaid
classDiagram
    class ActivoFijo {
        +str codigo
        +str descripcion
        +Decimal precio
        +str marca
        +str modelo
        +str numero_serie
        +str ubicacion
        +str custodio
        +date fecha_adquisicion
        +int garantia_meses
        +str proveedor
        +str observaciones
        +Mapping caracteristicas
    }
    class ActivoFijoBuilder {
        +__init__(codigo, descripcion, precio)
        +marca(valor) ActivoFijoBuilder
        +modelo(valor) ActivoFijoBuilder
        +numero_serie(valor) ActivoFijoBuilder
        +ubicacion(valor) ActivoFijoBuilder
        +custodio(valor) ActivoFijoBuilder
        +fecha_adquisicion(valor) ActivoFijoBuilder
        +garantia_meses(valor) ActivoFijoBuilder
        +proveedor(valor) ActivoFijoBuilder
        +observaciones(valor) ActivoFijoBuilder
        +caracteristica(nombre, valor) ActivoFijoBuilder
        +build() ActivoFijo
    }
    Cliente --> ActivoFijoBuilder
    ActivoFijoBuilder ..> ActivoFijo : construye
~~~

### Uso crítico de IA (propuesta para revisión del grupo)
Prompt principal: Implementa Builder fluido en Python para activos fijos, con código, descripción y precio obligatorios, atributos opcionales, ejemplos de computador y mesa, validaciones, UML y pruebas.
Recomendación aceptada: recibir los datos obligatorios al iniciar el builder y añadir opcionales con métodos encadenables.
Justificación: hace explícito el significado de cada dato y evita parámetros vacíos.
Recomendación modificada o rechazada: compartir el diccionario mutable del builder con los productos creados.
Justificación: se usa una copia de solo lectura para que las modificaciones posteriores del builder no cambien un activo existente.

## Publicar en GitHub
1. Crear en GitHub un repositorio vacío llamado PatronesDeSoftware, sin README ni .gitignore.
2. Desde esta carpeta, ejecutar (sustituir TU_USUARIO):
~~~powershell
git add caso1.py caso2.py test_patrones.py README.md .gitignore
git commit -m "Implementar Factory Method y Builder en Python"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/PatronesDeSoftware.git
git push -u origin main
~~~
Git puede solicitar autenticación mediante el navegador.
Si Git solicita identidad, configurar el nombre y correo propios con git config user.name y git config user.email antes del commit.
Para cambios posteriores:
~~~powershell
git add .
git commit -m "Actualizar ejemplos"
git push
~~~
Publicar el código en GitHub no equivale a alojar una aplicación web.
