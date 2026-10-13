# Evidencias de la práctica 2.2

Revisión: 12 de octubre de 2026, referencia America/Mexico_City.
Implementación propia basada en la guía; no es el ZIP original del docente.

## Comprobaciones reales sin cargos

- Python 3.13.7 y pip check sin conflictos.
- Suite inicial: 6 aprobadas. Suite ampliada: **10 aprobadas en 0.83 s**.
- Servidor existente en 5000: health respondió 200. Código corregido verificado en 5001.
- Recursos públicos 200, entrada inválida 422 y archivos privados 404.
- .env ignorado y no versionado. Se revisaron archivos versionados, historial y
  respuestas HTTP buscando los secretos existentes, sin imprimirlos.
- Registro: [verificacion-local.json](evidencias/verificacion-local.json).
- Pruebas simuladas verificaron herramientas, citas, respuestas incompletas,
  errores sin filtración y bloqueo en Vercel sin código de acceso separado.
- No hubo consultas pagadas. Las pruebas simuladas no son investigaciones reales.

## Experimentos A y B: pendientes de presupuesto

Pregunta idéntica:

> ¿Cuáles son las tendencias de agentes de inteligencia artificial durante 2026?

Modelo: gpt-6-luna, conservado. Modo previsto para ambos: rapido.
Presupuesto: solicitado una sola vez, todavía sin respuesta.
Fecha de las investigaciones: pendiente; no se sustituye por la fecha de revisión.

| Criterio | A: sin Web Search | B: con Web Search |
|---|---|---|
| Actualidad | No evaluada: sin respuesta real | No evaluada: sin respuesta real |
| Presencia de fuentes | No evaluada | No evaluada |
| Evidencia verificable | No evaluada | No evaluada |
| Fechas | No evaluadas | No evaluadas |
| Profundidad | No evaluada | No evaluada |
| Posibilidad de comprobar afirmaciones | No evaluada | No evaluada |

Al ejecutarlos, conservar JSON y TXT con fecha UTC, modelo, modo, estado,
web solicitada/utilizada, llamadas, tokens y fuentes recibidas.

## Experimento C: distintas perspectivas

> ¿Qué perspectivas existen sobre el impacto de la IA generativa en el trabajo de los programadores?

Pendiente de presupuesto. No hay perspectivas observadas ni fuentes reales que analizar.

## Análisis temporal y evaluación de fuentes

Se reutilizará B sin duplicar la consulta. No se obtuvieron fuentes de esa
investigación: son insuficientes para asignar puntuaciones justificadas.
Escala: 1 = baja, 2 = media, 3 = alta.

| Fuente y URL | Publicación | Consulta | Autoridad | Actualidad | Confiabilidad | Justificación |
|---|---|---|---|---|---|---|
| Pendiente de B: fuente 1 | No comprobada | Pendiente | — | — | — | Sin fuente real |
| Pendiente de B: fuente 2 | No comprobada | Pendiente | — | — | — | Sin fuente real |
| Pendiente de B: fuente 3 | No comprobada | Pendiente | — | — | — | Sin fuente real |

La **fecha de publicación** corresponde al contenido; la **fecha de consulta**
registra cuándo se examinó. Si no hay publicación o actualización verificable,
se indicará “no disponible”, sin reemplazarla por la fecha de consulta.

## Interfaz y capturas

Navegador no disponible; no se tomaron capturas. Pendientes: A, B, C, diseño
móvil/tableta/escritorio, envío del formulario, citas y TXT desde navegador real.
No se sustituyen capturas por imágenes generadas o datos simulados.

## GitHub y Vercel

- GitHub: https://github.com/Metrasta214/agente-investigador-tic (público, publicado).
- Avances: https://github.com/Metrasta214/agente-investigador-tic/tree/feature/agente-investigador
- Vercel: no desplegado. Falta presupuesto, investigación real local y conectar
  la cuenta. No hay resultados de build, runtime ni investigación en producción.
- main conserva el estado base; los cambios están en feature/agente-investigador.
  La integración final queda pendiente de la investigación real validada.
- Configuración FastAPI contrastada con documentación oficial.
- Antes de desplegar: OPENAI_API_KEY, OPENAI_MODEL y APP_ACCESS_TOKEN en variables
  del servidor. El código debe ser distinto de la API Key y no estar en GitHub.
  Vercel bloquea consultas si falta el código o coincide con la clave.

## Borrador informal de conclusiones para revisar

Al revisar Radar TIC entendí cómo se separan la interfaz, las rutas de FastAPI,
la configuración y el servicio que usa OpenAI. Las clases ayudan a organizar esas
responsabilidades. También comprobé la validación de datos y que los archivos
privados no se entregan por HTTP. Registré el estado inicial y las correcciones
en Git, sin inventar un historial anterior. La búsqueda web está preparada para
aportar fuentes, pero todavía me falta comparar sus resultados reales. Para
publicar con seguridad no basta con ocultar la API Key: también hay que restringir
el acceso a las consultas. El despliegue y su validación siguen pendientes.
