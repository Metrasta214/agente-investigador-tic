# Radar TIC · Agente investigador

Práctica 2.2 — Inteligencia artificial aplicada a las TIC.
Implementación propia basada en la guía de la práctica; no es el ZIP original del docente.

## Inicio en Windows

Necesitas Python 3.12 o 3.13 e Internet (se verificó Python 3.13.7). Abre la carpeta
`agente-investigador-tic` en VS Code. En su terminal PowerShell ejecuta:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edita **.env** y coloca tu clave exclusivamente allí:

```dotenv
OPENAI_API_KEY=tu_clave_real
OPENAI_MODEL=gpt-6-luna
APP_ACCESS_TOKEN=
CORS_ORIGINS=
```

El modelo conserva el nombre indicado en la guía. Su disponibilidad depende de tu
proyecto de OpenAI. Si devuelve un error de modelo, confirma con el profesor un
modelo de tu cuenta compatible con Responses API y Web Search y cambia
`OPENAI_MODEL`. Reinicia el servidor después de editar variables.

```powershell
.\.venv\Scripts\python.exe app.py
```

Abre **http://127.0.0.1:5000**. No uses Live Server ni abras index.html con doble clic.
No es necesario activar el entorno virtual con estos comandos.
Detén el servidor con Ctrl+C.

En macOS/Linux usa `python3 -m venv .venv`, `.venv/bin/python -m pip install -r requirements.txt`,
`cp .env.example .env` y `.venv/bin/python app.py`.

## Funcionalidades

- Pregunta validada de 8 a 2000 caracteres.
- Modos rápido, comparativo y profundo (distintas instrucciones de profundidad).
- Interruptor Web Search: la misma pregunta puede probarse sin herramientas y con búsqueda requerida.
- Resumen, hallazgos, coincidencias, diferencias, tendencias, conclusión y fuentes
  solicitados al modelo. El texto generado no está garantizado como un esquema rígido.
- Citas recibidas de OpenAI enlazadas dentro de la respuesta y lista de fuentes.
- Fecha de consulta, modelo, modo y confirmación de búsqueda realmente completada.
- Estado, tokens reportados y número de llamadas web. Cada solicitud admite como
  máximo tres llamadas de herramientas y 6000 tokens de salida; esto no sustituye
  un presupuesto por sesión o por cuenta.
- Descarga del resultado en TXT para conservar evidencia.
- Estados de carga y errores de clave, cuota, conexión y tiempo de espera.
- Interfaz adaptable sin dependencias externas de JavaScript.
- Código de acceso opcional para restringir consultas.

## Arquitectura y OOP

| Ruta | Responsabilidad |
|---|---|
| app.py | Exporta FastAPI e inicia Uvicorn en local |
| app/main.py | HTTP, endpoints, errores y archivos estáticos |
| app/core/config.py | Clase Settings y lectura de variables |
| app/models/investigacion.py | Modelos Pydantic de entrada, respuesta, citas y fuentes |
| app/services/investigador_service.py | Clase InvestigadorService: instrucciones, Responses API y procesamiento |
| index.html | Estructura de la interfaz |
| assets/css/styles.css | Diseño adaptable |
| assets/js/config.js | Clase Config: rutas y tiempo de espera |
| assets/js/api.js | Clase Api: comunicación HTTP |
| assets/js/app.js | Clase RadarApp: eventos y presentación segura |
| .env.example | Plantilla sin secretos |
| .gitignore | Exclusión de credenciales y archivos temporales |
| requirements.txt | Dependencias directas con versiones verificadas |
| vercel.json | Selección del framework FastAPI |
| docs/evidencias.md | Resultados reales y experimentos académicos pendientes |
| docs/evidencias/ | Registros de verificación sin credenciales |
| tests/test_app.py | Pruebas automatizadas sin consumir OpenAI |
| scripts/verificar_local.py | Auditoría HTTP, archivos e historial sin llamadas pagadas |
| scripts/publicar_github.py | Publicación usando la cuenta comprobada y credenciales de Git en memoria |

`Settings` encapsula configuración; Pydantic valida datos; `InvestigadorService`
construye instrucciones y procesa la respuesta. `Config`, `Api` y `RadarApp`
separan rutas, transporte y comportamiento de la interfaz. Los `__init__.py`
identifican paquetes Python. `.python-version` indica Python 3.12 para desplegar;
`.vercelignore` excluye secretos y archivos innecesarios del paquete de ejecución.
`requirements-dev.txt` incorpora las dependencias de pruebas.

Flujo: formulario → Api → POST /api/investigar → validación Pydantic →
InvestigadorService → OpenAI (con o sin herramienta) → texto y citas → interfaz.
La configuración y las credenciales nunca se devuelven al navegador.

## API

- `GET /api/health`: disponibilidad del backend y presencia de configuración,
  no verifica saldo ni acceso real al modelo.
- `POST /api/investigar`: JSON con `pregunta`, `modo` y `usar_web`.
- `GET /docs`: documentación interactiva.
- Cabecera opcional `X-Access-Token` si se configuró APP_ACCESS_TOKEN.

Ejemplo de cuerpo:

```json
{"pregunta":"Compara LoRaWAN y Wi-Fi para monitoreo agrícola.","modo":"comparativo","usar_web":true}
```

No hay base de datos ni historial persistente: descarga las respuestas que quieras
conservar antes de cerrar la página. El modo profundo es una consulta más extensa,
no una investigación autónoma de duración ilimitada.

## Pruebas de la práctica

1. Desactiva Internet en el interruptor de la interfaz (no desconectes tu computadora:
   OpenAI sigue necesitando conexión) y ejecuta una pregunta reciente.
2. Descarga el TXT y toma captura.
3. Activa el interruptor y repite exactamente la misma pregunta y el mismo modo.
4. Completa la comparación de `docs/evidencias.md`.
5. Prueba una consulta con perspectivas diferentes.
6. Haz una consulta temporal y evalúa tres fuentes de 1 a 3.

No se incluyen investigaciones ficticias ni conclusiones personales inventadas.

## Git/GitHub

Se recibió el proyecto sin historial. Esta revisión inicializó `main`, registró
el estado base y creó `feature/agente-investigador`. La identidad se tomó de la
configuración existente. Los commits corresponden al trabajo real de esta sesión.
La integración final en `main` queda pendiente de validar una investigación real.

```bash
git init
git branch -M main
git add .
git status
git commit -m "chore: incorpora implementación base de Radar TIC"
git checkout -b feature/agente-investigador
```

Verifica antes del commit que .env no aparezca. Configura tu nombre/correo si Git
lo solicita. Crea `agente-investigador-tic` en tu cuenta de GitHub y después:

```bash
git remote add origin https://github.com/TU_USUARIO/agente-investigador-tic.git
git push -u origin main
git push -u origin feature/agente-investigador
```

Después de las pruebas registra los cambios y documentación en la rama de desarrollo;
integra la versión validada en main. No fabriques commits de trabajo no realizado.

## Vercel

1. Primero verifica una investigación real completa en local.
2. Importa el repositorio de GitHub en Vercel. La raíz debe ser la carpeta que
   contiene app.py y requirements.txt; selecciona FastAPI si no se detecta.
3. No configures una carpeta de salida estática ni un comando de build de Node.
4. Agrega OPENAI_API_KEY y OPENAI_MODEL como variables de entorno del servidor.
5. Define obligatoriamente APP_ACCESS_TOKEN con un código aleatorio distinto de la
   API Key. Vercel bloquea consultas si falta o coincide con la clave. Guárdalo solo
   en variables del servidor o en .env, nunca en GitHub. La interfaz pedirá este
   código en el campo de acceso; quien lo conozca podrá generar consumo.
6. Despliega y verifica /api/health, la página principal y una investigación con citas.
7. Si modificas variables, vuelve a desplegar. Revisa logs ante errores.

La aplicación exporta `app` desde app.py y app/main.py. Vercel dispone de soporte
nativo para FastAPI; se evita una configuración antigua de builders y rewrites.
Las consultas dependen de los límites de duración de tu plan: ante timeouts usa
el modo rápido o ajusta la duración permitida desde Vercel según tu plan.
Todavía no se ha desplegado: falta presupuesto autorizado, una investigación
real validada en local y conectar Vercel. No se contrataron planes de pago.

## Seguridad y límites

Nunca subas .env. Solo assets se expone como carpeta estática; la raíz del proyecto
no se publica. Texto generado se inserta con textContent/text nodes, sin ejecutar
HTML del modelo, y solo se admiten enlaces HTTP(S).

Proteger la API Key no limita por sí solo el consumo de un endpoint público.
APP_ACCESS_TOKEN es una protección sencilla de demostración, no un sistema de
cuentas ni un límite distribuido. Para uso abierto añade autenticación y límites
de solicitudes/costos adecuados en tu infraestructura. No compartas la API Key
como código de acceso.

OpenAI requiere credenciales válidas, acceso al modelo y cuota disponible.
El servicio puede cobrar tokens y búsquedas. No hay respuestas de demostración
que se presenten como investigación real.

## Verificación automatizada

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
```

Las pruebas usan un proveedor simulado: verifican el contrato, citas, errores,
protección de archivos y activación/desactivación de herramientas sin cargos.
La consulta real a OpenAI y la publicación en Vercel siguen pendientes.

## Revisión del 12 de octubre de 2026

- Se analizaron backend, frontend, configuración, dependencias y pruebas.
- Faltaban pytest y httpx; se instalaron desde `requirements-dev.txt`.
  Las seis pruebas iniciales pasaron. La suite ampliada pasó **10 pruebas en 0.83 s**;
  `pip check` no encontró conflictos.
- El servidor existente respondió en 5000. Se inició otra instancia en
  `http://127.0.0.1:5001` para verificar el código corregido sin interrumpirlo.
  Reinicia tu proceso en 5000 para cargar los cambios.
- Se comprobaron rutas y recursos HTTP, validación 422, archivos privados 404,
  `.env` ignorado y ausencia de secretos existentes en archivos, historial y HTTP.
- La documentación oficial confirma compatibilidad de `gpt-6-luna` con Responses
  API y Web Search. Se conservó el modelo; no se verificaron saldo ni permisos reales.
- Se corrigió `/docs`: su política bloqueaba Swagger; ahora permite su CDN solo
  en esa ruta y protege el script de inicio con un nonce.
- Se añadieron pruebas para errores sin filtración, consumo reportado y bloqueo
  de Vercel sin un código de acceso separado.
- Navegador no disponible: envío del formulario, descarga TXT, capturas y diseño
  móvil/tableta/escritorio siguen pendientes de verificación visual.
- **Cero consultas pagadas**: presupuesto solicitado, todavía sin respuesta.

Con un servidor iniciado, repite las comprobaciones HTTP sin cargos:

```powershell
.\.venv\Scripts\python.exe scripts\verificar_local.py --url http://127.0.0.1:5001
```

El registro queda en `docs/evidencias/verificacion-local.json`. Las pruebas con
proveedor simulado no sustituyen los experimentos académicos A, B y C.

## Entrega

- URL GitHub: https://github.com/Metrasta214/agente-investigador-tic
- Avances revisados: https://github.com/Metrasta214/agente-investigador-tic/tree/feature/agente-investigador
- URL Vercel: pendiente.
- Conclusiones: borrador basado en lo comprobado en `docs/evidencias.md`; completar
  después de los experimentos reales y el despliegue.

## Referencias oficiales consultadas

- https://developers.openai.com/api/docs/guides/tools-web-search
- https://developers.openai.com/api/docs/models/gpt-6-luna
- https://vercel.com/docs/frameworks/backend/fastapi
