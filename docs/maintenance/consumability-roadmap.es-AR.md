# Roadmap de Consumibilidad

## Resumen ejecutivo

RAG Knowledge Model ya demostró que se puede construir: existe una arquitectura conceptual, schemas, validaciones, registries y tooling operativo para mantener el repositorio con disciplina.

La pregunta siguiente es distinta: **cómo lo convertimos en algo consumible por otros**.

La respuesta corta es que RKM necesita pasar de ser una base técnica sólida a ser un paquete entendible, usable y verificable por personas y sistemas externos. Para eso hacen falta ejemplos, fixtures, datos representativos, exportación a grafo, documentación para consumidores y releases versionadas.

El estado actual es bueno como fundación, pero todavía no conviene presentarlo como producto terminado. La madurez general está alrededor de 3.1 / 5. El modelo conceptual y el tooling están bastante más avanzados que el contenido poblado y la experiencia de consumo.

## Estado actual

RKM cuenta con una base importante:

- Arquitectura del dominio y del modelo de entidades.
- Modelo de relaciones, evidencia, metadata, naming y versionado.
- Schemas JSON Schema Draft 2020-12.
- Definitions reutilizables para conceptos compartidos.
- Registries para tipos de entidad y tipos de relación.
- Validación de contratos de schema.
- Validación de relaciones en documentación.
- Comandos operativos como `make validate`, `make cockpit-summary`, `make autopilot`, `make autocycle`, `make safe-push`, `make recovery-plan` y `make autopilot-recover`.
- Control de presupuesto, force mode, working target cap, budget grace y ledger operativo.
- Automatización de commits con soporte para un archivo o múltiples archivos coherentes.

Esto ubica al proyecto por encima de un prototipo. Ya hay estructura, reglas y automatización real.

El punto débil principal es que todavía falta convertir esa base en una experiencia clara para terceros. Hoy el repo es entendible para quien viene trabajando en el proyecto, pero todavía requiere demasiado contexto para una persona nueva, un equipo consumidor o una integración automatizada.

## Qué valor tiene

RKM aporta valor porque busca representar el ecosistema RAG como conocimiento estructurado, no como una colección de notas.

Ese enfoque permite:

- Describir técnicas, frameworks, modelos, datasets, benchmarks, proveedores, herramientas y patrones con identificadores estables.
- Relacionar entidades mediante predicados controlados.
- Asociar claims con evidencia y referencias.
- Separar metadata de conocimiento del dominio.
- Validar cambios antes de aceptarlos.
- Preparar el contenido para búsqueda, RAG, análisis semántico, JSONB, grafos y otros consumos técnicos.

Para equipos técnicos, el valor está en tener una fuente estructurada y versionable sobre el ecosistema RAG. Para liderazgo, el valor está en transformar conocimiento disperso en un activo mantenible, auditable y reutilizable.

## Qué falta para que lo usen otros

Para que RKM sea consumible por otros, faltan piezas concretas:

- Ejemplos completos que muestren entidades, relaciones, claims, evidencia y referencias válidas.
- Fixtures, es decir, datos pequeños y representativos que sirvan para pruebas, demos e integraciones.
- Un dataset inicial con contenido real suficiente para demostrar utilidad.
- Graph export documentado, con reglas claras para nodos, aristas, identificadores, labels, relaciones, evidencia y procedencia.
- Guía de consumidor que explique cómo validar, cargar, inspeccionar y consultar el contenido.
- Guía de contribución orientada a personas nuevas, no solo a asistentes automatizados.
- Releases versionadas con notas, alcance y compatibilidad esperada.
- Ejemplos de uso en escenarios concretos, como búsqueda semántica, carga en base de grafos o uso como corpus RAG.

La clave es que alguien externo pueda responder sin ayuda estas preguntas:

- Qué es RKM.
- Qué problema resuelve.
- Cómo valido el repo.
- Dónde están los schemas.
- Cómo se ve un registro válido.
- Cómo cargo los datos.
- Cómo exporto a grafo.
- Qué partes son estables.
- Qué partes todavía están en evolución.

## MVP consumible

El mínimo paquete consumible debería permitir que otro equipo pruebe RKM sin depender de contexto oral ni de decisiones implícitas del equipo mantenedor.

Ese MVP debería incluir:

- Un fixture mínimo validado que muestre una entidad, una relación, un claim, evidencia y referencias conectadas de manera consistente.
- Un dataset inicial chico, con contenido real y representativo, suficiente para probar lectura, validación e inspección.
- Una guía de consumidor que explique cómo validar el repo, dónde mirar los schemas, cómo interpretar los registros y qué partes todavía están evolucionando.
- Un graph export inicial con contrato explícito para nodos, aristas, identificadores, labels, predicados, evidencia y procedencia.
- Un quickstart que permita clonar, validar, revisar un ejemplo y entender el flujo básico en pocos pasos.
- Un release tag con alcance claro, notas de release y expectativas de compatibilidad.

Ese paquete no convertiría a RKM en un producto maduro. Sí lo convertiría en algo evaluable por terceros: un equipo podría probarlo, hacer preguntas concretas y decidir si le sirve como base para una integración o una contribución.

## Roadmap por fases

### Fase 1: Paquete mínimo consumible

Objetivo: que una persona técnica pueda entender y validar RKM en menos tiempo.

Entregables:

- Fixture mínimo con entidades, relaciones, claims, evidencia y referencias.
- Guía breve para validar el repo con `make validate`.
- Guía breve para interpretar schemas, definitions y registries.
- Ejemplos de registros válidos.
- Mapa actualizado del repo y comandos operativos.

Resultado esperado: RKM deja de depender tanto del contexto oral o del historial de trabajo.

### Fase 2: Consumo técnico básico

Objetivo: que un consumidor pueda usar RKM en una prueba real.

Entregables:

- Dataset inicial pequeño pero representativo.
- Script o procedimiento de carga documentado.
- Validación aplicada sobre fixtures y datos de ejemplo.
- Documentación de errores comunes y cómo corregirlos.
- Separación clara entre arquitectura, schemas, fixtures y datos poblados.

Resultado esperado: otro equipo puede probar RKM sin tener que reconstruir las decisiones de modelado.

### Fase 3: Graph export

Objetivo: habilitar el uso de RKM como fuente para grafos de conocimiento.

Entregables:

- Contrato de exportación a grafo.
- Definición de nodos, aristas, labels, identificadores y propiedades.
- Reglas para claims, evidencia, referencias y provenance.
- Ejemplo de export sobre fixtures.
- Documentación de consultas esperadas.

Resultado esperado: RKM puede conectarse con herramientas de grafo o pipelines analíticos sin interpretaciones ambiguas.

### Fase 4: Release inicial

Objetivo: publicar una versión utilizable con alcance claro.

Entregables:

- Versión inicial etiquetada.
- Release notes.
- Validación reproducible.
- Guía de uso para consumidores.
- Matriz de alcance que diga qué incluye y qué no incluye la release.
- Criterios de compatibilidad para cambios futuros.

Resultado esperado: RKM puede ser evaluado como artefacto versionado, no solo como repo en desarrollo.

### Fase 5: Expansión controlada

Objetivo: aumentar contenido y adopción sin perder coherencia.

Entregables:

- Más entidades reales sobre técnicas, frameworks, modelos, datasets, benchmarks y herramientas.
- Mejores ejemplos de tradeoffs, limitaciones, problemas y casos de uso.
- Tests y validaciones adicionales sobre contenido poblado.
- Documentación de integraciones frecuentes.
- Proceso de revisión más claro para contribuciones externas.

Resultado esperado: RKM crece como base de conocimiento sin degradar el modelo.

## Qué le diría a un equipo interesado

RKM es una base estructurada para describir el ecosistema RAG: técnicas, frameworks, modelos, datasets, benchmarks, herramientas, claims, evidencia, referencias y relaciones entre esos conceptos. La intención es que ese conocimiento sea legible por personas, validable por tooling y reutilizable por sistemas externos.

RKM no es todavía un producto listo para adopción amplia. No es un catálogo completo del mercado RAG, no es una plataforma de búsqueda terminada y no reemplaza una implementación RAG. Hoy es una base de conocimiento y modelado con arquitectura sólida, validaciones y automatización, pero con contenido poblado y experiencia de consumo todavía limitados.

Lo que se puede probar ahora es la estructura: cómo están definidos los schemas, cómo funcionan las validaciones, cómo se modelan entidades y relaciones, y cómo el repo sostiene cambios con disciplina operativa. También se puede evaluar si el enfoque sirve como base para conocimiento estructurado, grafo de conocimiento o corpus RAG.

Lo que todavía necesita trabajo es el paquete consumible: fixtures claros, dataset inicial, guía de consumidor, graph export, quickstart y release tag. Por eso la próxima fase debería enfocarse en consumibilidad antes de expandir mucho más el modelo.

## Riesgos

**Duplicación conceptual**

Si se agregan schemas y definitions sin revisar el modelo, el mismo concepto puede aparecer en varios lugares con nombres o estructuras distintas. Eso reduce consistencia y complica el consumo.

**Definitions embebidas que se comportan como entidades**

Algunas definitions pueden acumular identidad, relaciones o evidencia. Cuando eso pasa, quizás deban pasar a ser entidades de primera clase o relaciones explícitas.

**Falta de ejemplos**

Sin ejemplos completos, el repo puede ser correcto pero difícil de entender. Los ejemplos son parte de la interfaz del proyecto.

**Falta de graph export**

El modelo apunta a ser base para grafo de conocimiento, pero sin export documentado cada consumidor podría interpretarlo de manera distinta.

**Complejidad del tooling**

El tooling es potente, pero cockpit, autopilot, budget guard, force mode y recovery pueden intimidar a usuarios nuevos. Hay que explicarlos como una capa de seguridad operativa, no como requisitos conceptuales para entender RKM.

**Onboarding**

RKM mezcla modelado conceptual, JSON Schema, validaciones, automatización y flujo de trabajo asistido por IA. Sin una ruta de entrada clara, la barrera de adopción sube.

## Próximos entregables

Los próximos entregables recomendados son:

1. Fixture mínimo validado.
2. Guía de consumidor para validar, cargar e inspeccionar RKM.
3. Ejemplos completos de entidades y relaciones.
4. Contrato inicial de graph export.
5. Dataset inicial pequeño con contenido real representativo.
6. Release notes para una primera versión consumible.
7. Guía corta para explicar el repo a nuevos colaboradores.

Estos entregables deberían priorizar claridad y uso real antes que volumen. Es mejor tener pocos ejemplos completos y validados que muchos registros incompletos.

## Respuesta corta para dirección

Ya tenemos una base técnica fuerte para RKM: modelo conceptual, schemas, validación, registries y automatización. No es solo una idea ni un prototipo suelto.

Lo que falta para que otros lo usen es empaquetarlo como producto consumible: ejemplos, fixtures, dataset inicial, exportación a grafo, documentación de uso y una release versionada.

La recomendación es invertir el próximo tramo en consumibilidad, no solamente en ampliar el modelo. Eso convierte el trabajo actual en un activo reutilizable por equipos técnicos, liderazgo y sistemas externos.
