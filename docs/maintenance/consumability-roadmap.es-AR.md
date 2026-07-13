# Roadmap de Consumibilidad

## Resumen ejecutivo

RAG Knowledge Model ya demostro que se puede construir: existe una arquitectura conceptual, schemas, validaciones, registries y tooling operativo para mantener el repositorio con disciplina.

La pregunta siguiente es distinta: **como lo convertimos en algo consumible por otros**.

La respuesta corta es que RKM necesita pasar de ser una base tecnica solida a ser un paquete entendible, usable y verificable por personas y sistemas externos. Para eso hacen falta ejemplos, fixtures, datos representativos, exportacion a grafo, documentacion para consumidores y releases versionadas.

El estado actual es bueno como fundacion, pero todavia no conviene presentarlo como producto terminado. La madurez general esta alrededor de 3.1 / 5. El modelo conceptual y el tooling estan bastante mas avanzados que el contenido poblado y la experiencia de consumo.

## Estado actual

RKM cuenta con una base importante:

- Arquitectura del dominio y del modelo de entidades.
- Modelo de relaciones, evidencia, metadata, naming y versionado.
- Schemas JSON Schema Draft 2020-12.
- Definitions reutilizables para conceptos compartidos.
- Registries para tipos de entidad y tipos de relacion.
- Validacion de contratos de schema.
- Validacion de relaciones en documentacion.
- Comandos operativos como `make validate`, `make cockpit-summary`, `make autopilot`, `make autocycle`, `make safe-push`, `make recovery-plan` y `make autopilot-recover`.
- Control de presupuesto, force mode, working target cap, budget grace y ledger operativo.
- Automatizacion de commits con soporte para un archivo o multiples archivos coherentes.

Esto ubica al proyecto por encima de un prototipo. Ya hay estructura, reglas y automatizacion real.

El punto debil principal es que todavia falta convertir esa base en una experiencia clara para terceros. Hoy el repo es entendible para quien viene trabajando en el proyecto, pero todavia requiere demasiado contexto para una persona nueva, un equipo consumidor o una integracion automatizada.

## Que valor tiene

RKM aporta valor porque busca representar el ecosistema RAG como conocimiento estructurado, no como una coleccion de notas.

Ese enfoque permite:

- Describir tecnicas, frameworks, modelos, datasets, benchmarks, proveedores, herramientas y patrones con identificadores estables.
- Relacionar entidades mediante predicados controlados.
- Asociar claims con evidencia y referencias.
- Separar metadata de conocimiento del dominio.
- Validar cambios antes de aceptarlos.
- Preparar el contenido para busqueda, RAG, analisis semantico, JSONB, grafos y otros consumos tecnicos.

Para equipos tecnicos, el valor esta en tener una fuente estructurada y versionable sobre el ecosistema RAG. Para liderazgo, el valor esta en transformar conocimiento disperso en un activo mantenible, auditable y reutilizable.

## Que falta para que lo usen otros

Para que RKM sea consumible por otros, faltan piezas concretas:

- Ejemplos completos que muestren entidades, relaciones, claims, evidencia y referencias validas.
- Fixtures, es decir, datos pequenos y representativos que sirvan para pruebas, demos e integraciones.
- Un dataset inicial con contenido real suficiente para demostrar utilidad.
- Graph export documentado, con reglas claras para nodos, aristas, identificadores, labels, relaciones, evidencia y procedencia.
- Guia de consumidor que explique como validar, cargar, inspeccionar y consultar el contenido.
- Guia de contribucion orientada a personas nuevas, no solo a asistentes automatizados.
- Releases versionadas con notas, alcance y compatibilidad esperada.
- Ejemplos de uso en escenarios concretos, como busqueda semantica, carga en base de grafos o uso como corpus RAG.

La clave es que alguien externo pueda responder sin ayuda estas preguntas:

- Que es RKM.
- Que problema resuelve.
- Como valido el repo.
- Donde estan los schemas.
- Como se ve un registro valido.
- Como cargo los datos.
- Como exporto a grafo.
- Que partes son estables.
- Que partes todavia estan en evolucion.

## Roadmap por fases

### Fase 1: Paquete minimo consumible

Objetivo: que una persona tecnica pueda entender y validar RKM en menos tiempo.

Entregables:

- Fixture minimo con entidades, relaciones, claims, evidencia y referencias.
- Guia breve para validar el repo con `make validate`.
- Guia breve para interpretar schemas, definitions y registries.
- Ejemplos de registros validos.
- Mapa actualizado del repo y comandos operativos.

Resultado esperado: RKM deja de depender tanto del contexto oral o del historial de trabajo.

### Fase 2: Consumo tecnico basico

Objetivo: que un consumidor pueda usar RKM en una prueba real.

Entregables:

- Dataset inicial pequeno pero representativo.
- Script o procedimiento de carga documentado.
- Validacion aplicada sobre fixtures y datos de ejemplo.
- Documentacion de errores comunes y como corregirlos.
- Separacion clara entre arquitectura, schemas, fixtures y datos poblados.

Resultado esperado: otro equipo puede probar RKM sin tener que reconstruir las decisiones de modelado.

### Fase 3: Graph export

Objetivo: habilitar el uso de RKM como fuente para grafos de conocimiento.

Entregables:

- Contrato de exportacion a grafo.
- Definicion de nodos, aristas, labels, identificadores y propiedades.
- Reglas para claims, evidencia, referencias y provenance.
- Ejemplo de export sobre fixtures.
- Documentacion de consultas esperadas.

Resultado esperado: RKM puede conectarse con herramientas de grafo o pipelines analiticos sin interpretaciones ambiguas.

### Fase 4: Release inicial

Objetivo: publicar una version utilizable con alcance claro.

Entregables:

- Version inicial etiquetada.
- Release notes.
- Validacion reproducible.
- Guia de uso para consumidores.
- Matriz de alcance que diga que incluye y que no incluye la release.
- Criterios de compatibilidad para cambios futuros.

Resultado esperado: RKM puede ser evaluado como artefacto versionado, no solo como repo en desarrollo.

### Fase 5: Expansion controlada

Objetivo: aumentar contenido y adopcion sin perder coherencia.

Entregables:

- Mas entidades reales sobre tecnicas, frameworks, modelos, datasets, benchmarks y herramientas.
- Mejores ejemplos de tradeoffs, limitaciones, problemas y casos de uso.
- Tests y validaciones adicionales sobre contenido poblado.
- Documentacion de integraciones frecuentes.
- Proceso de revision mas claro para contribuciones externas.

Resultado esperado: RKM crece como base de conocimiento sin degradar el modelo.

## Riesgos

**Duplicacion conceptual**

Si se agregan schemas y definitions sin revisar el modelo, el mismo concepto puede aparecer en varios lugares con nombres o estructuras distintas. Eso reduce consistencia y complica el consumo.

**Definitions embebidas que se comportan como entidades**

Algunas definitions pueden acumular identidad, relaciones o evidencia. Cuando eso pasa, quizas deban pasar a ser entidades de primera clase o relaciones explicitas.

**Falta de ejemplos**

Sin ejemplos completos, el repo puede ser correcto pero dificil de entender. Los ejemplos son parte de la interfaz del proyecto.

**Falta de graph export**

El modelo apunta a ser base para grafo de conocimiento, pero sin export documentado cada consumidor podria interpretarlo de manera distinta.

**Complejidad del tooling**

El tooling es potente, pero cockpit, autopilot, budget guard, force mode y recovery pueden intimidar a usuarios nuevos. Hay que explicarlos como una capa de seguridad operativa, no como requisitos conceptuales para entender RKM.

**Onboarding**

RKM mezcla modelado conceptual, JSON Schema, validaciones, automatizacion y flujo de trabajo asistido por IA. Sin una ruta de entrada clara, la barrera de adopcion sube.

## Proximos entregables

Los proximos entregables recomendados son:

1. Fixture minimo validado.
2. Guia de consumidor para validar, cargar e inspeccionar RKM.
3. Ejemplos completos de entidades y relaciones.
4. Contrato inicial de graph export.
5. Dataset inicial pequeno con contenido real representativo.
6. Release notes para una primera version consumible.
7. Guia corta para explicar el repo a nuevos colaboradores.

Estos entregables deberian priorizar claridad y uso real antes que volumen. Es mejor tener pocos ejemplos completos y validados que muchos registros incompletos.

## Respuesta corta para direccion

Ya tenemos una base tecnica fuerte para RKM: modelo conceptual, schemas, validacion, registries y automatizacion. No es solo una idea ni un prototipo suelto.

Lo que falta para que otros lo usen es empaquetarlo como producto consumible: ejemplos, fixtures, dataset inicial, exportacion a grafo, documentacion de uso y una release versionada.

La recomendacion es invertir el proximo tramo en consumibilidad, no solamente en ampliar el modelo. Eso convierte el trabajo actual en un activo reutilizable por equipos tecnicos, liderazgo y sistemas externos.
