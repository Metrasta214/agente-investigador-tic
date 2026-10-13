# Radar TIC: instalación de skills y propuesta de diseño

Fecha de revisión: 12 de octubre de 2026, America/Mexico_City.
Estado: propuesta para aprobación; no se implementó ningún cambio de interfaz.

## Instalación y comprobaciones

Raíz del proyecto: `Unidad_2/2.2 Agente investigador`, dentro del workspace de códigos.
Las skills no estaban presentes en esa carpeta. No se instalaron globalmente.

| Skill | Ubicación en el proyecto | Método y versión |
|---|---|---|
| Apple Design | `.agents/skills/apple-design/SKILL.md` | Submódulo Git, método documentado por el repositorio; commit `904b0eedc7cc778152f545506075d5bb5219ce77` |
| UI/UX Pro Max | `.agents/skills/ui-ux-pro-max/SKILL.md` | CLI oficial npm `ui-ux-pro-max-cli@2.15.0`, generación para Codex en staging y copia de la skill principal |

Requisitos verificados: Node.js v24.21.0, npm 11.19.0 y Python 3.13.7 desde
`.venv/Scripts/python.exe`. Python no está disponible como `python` en el PATH
de la terminal examinada; no se necesita otra instalación para este proyecto.

Se revisaron README, SKILL.md, instrucciones Codex, scripts y paquetes de los
instaladores antes de ejecutarlos. La descarga inicial de Apple falló por conexión
a GitHub y el reintento funcionó; no queda un bloqueo de instalación.

Apple se instaló con el método oficial de submódulo, ajustando su destino a la
ubicación que Codex descubre automáticamente:

```powershell
git submodule add https://github.com/dickwu/apple-design-skill.git .agents/skills/apple-design
```

Se creó `.gitmodules`; no había un archivo previo que sobrescribir. Git dejó
preparados el submódulo y `.gitmodules`, comportamiento normal de este método.
No se creó un commit ni se publicaron estos cambios.

Para UI/UX Pro Max, se descargó el paquete con `npm pack --ignore-scripts`, se
inspeccionó su código y se ejecutó su entrada oficial `dist/index.js` con
`init --ai codex --offline` en una carpeta temporal. El CLI genera además seis
skills auxiliares; únicamente se copió `ui-ux-pro-max` al destino local vacío.
No se copiaron banner-design, brand, design, design-system, slides ni ui-styling.
No se usaron opciones globales, de sobrescritura, actualización o desinstalación.

### Scripts y dependencias inspeccionados

- Apple `pull-hig.mjs`: Node 18+, módulos estándar, consulta developer.apple.com,
  escribe referencias y puede eliminar páginas retiradas. No se ejecutó su
  actualización; solo se comprobó sintaxis con `node --check`.
- Instalador alternativo de Apple `skills@1.7.2`: requiere Node >=22.20 y declara
  tar/yaml; contiene telemetría y limpieza de destinos. Se inspeccionó, pero no se
  ejecutó para instalar: se prefirió el submódulo documentado.
- CLI de UI/UX Pro Max: declara chalk, commander, ora y prompts, incluidos en el
  bundle ejecutado. Su instalación por plantillas copia datos/scripts y escribe
  SKILL.md. Las ramas de actualización/desinstalación y descargas legacy no se
  ejecutaron. Tampoco se ejecutaron scripts de lifecycle npm.
- UI/UX `search.py`, `core.py`, `design_system.py` y `reasoning_contract.py`:
  búsqueda BM25 en CSV locales, biblioteca estándar de Python, sin llamadas de
  red ni modelos. La opción de persistencia puede escribir un sistema de diseño;
  no se usó `--persist` ni `--force`.

Validaciones: frontmatter con nombre/descripción, scripts y referencias presentes;
124 archivos de referencia HIG de Apple; 34 catálogos requeridos por UI/UX Pro Max
presentes, sin faltantes. Las búsquedas locales terminaron correctamente.
Se verificó la estructura de descubrimiento, no el selector de la extensión en una
sesión de VS Code abierta.

## Uso desde Codex en VS Code

Abre específicamente la carpeta **2.2 Agente investigador** como proyecto, o
inicia Codex con ella como directorio de trabajo. Si abres solo la carpeta superior
`códigos`, Codex no tiene por qué descubrir skills alojadas en proyectos hijos.

En el chat escribe `$` y selecciona la skill, o consulta `/skills` si está disponible:

```text
$ui-ux-pro-max Revisa distribución, tipografía, colores y responsive de Radar TIC.
Entrega propuestas; no modifiques archivos de la interfaz.

$apple-design Revisa claridad, consistencia, accesibilidad y facilidad de uso.
Aplica criterios pertinentes para web; no convenciones exclusivas de iOS/macOS.
```

Las skills estarán disponibles en la siguiente interacción. Codex puede detectar
los cambios automáticamente; si no aparecen, reinicia la sesión de Codex o recarga
VS Code con `Developer: Reload Window`. No se modificó configuración global.

Ejemplo de búsqueda local con el Python existente:

```powershell
.\.venv\Scripts\python.exe .agents/skills/ui-ux-pro-max/scripts/search.py "error summary validation" --domain ux -n 2
```

## Resumen de la revisión

Evaluación: **requiere correcciones de accesibilidad**. La función principal es
formular una pregunta, elegir profundidad y consultar evidencia. El radar es un
elemento de identidad pertinente; puede mantenerse de forma discreta.

Esta es una revisión de HTML, CSS y JavaScript, con contraste calculado desde sus
colores. No se realizaron investigaciones, no se abrió un navegador ni se tomaron
capturas. Los posibles desbordamientos requieren validación visual; no se presentan
como fallos observados en un dispositivo real. Los tamaños nativos en pt/dp de las
skills no se trasladan como requisitos normativos a CSS: se aplican principios de
legibilidad, adaptación y facilidad de interacción.

Se utilizó realmente UI/UX Pro Max mediante búsquedas de sistema de diseño,
legibilidad, contraste, errores, etiquetas compactas y tipografía. La primera
recomendación sugirió FAQ/documentación, poco pertinente; un reintento encontró
AI-Native UI, más cercano al producto, pero seguía proponiendo una landing page
y colores morado/cian. Se descartaron esas partes por su desajuste con la tarea y
la preferencia del usuario. La elección de colores sobrios y distribución de
herramienta es juicio de diseño, no una salida textual del generador.

Las recomendaciones del catálogo html-tailwind se usaron solo por sus criterios
generales de HTML/foco/adaptación. El proyecto usa CSS nativo y no se propone
incorporar Tailwind ni un framework.

Apple Design se utilizó leyendo las referencias de accesibilidad, layout, color,
tipografía, escritura, carga, entrada de datos, IA generativa y traducción entre
plataformas. Se excluyeron barras nativas, Dynamic Type nativo, Liquid Glass,
haptics, tecnologías Apple y reglas de navegación que no corresponden a esta web.

## Problemas prioritarios

### 1. Crítico: contraste insuficiente en información útil

**Qué:** ayuda `#7b8477` sobre blanco: 3.88:1; aviso de consumo `#7c8578` sobre
blanco: 3.83:1; metadatos `#73806b` sobre blanco: 4.18:1; pie `#8a9184` sobre
`#f4f5ef`: 2.96:1. Son textos pequeños: se adopta objetivo 4.5:1.

**Por qué:** `accessibility.md › Vision`: “Strive to meet color contrast minimum standards.”
UI/UX Pro Max: `ux-guidelines.csv`, Color Contrast y Contrast Readability.

**Propuesta:** texto secundario `#526475` sobre blanco (6.11:1), con avisos de
consumo legibles antes del botón. El borde del textarea contrasta solo 1.43:1
con su fondo: revisar también límites visibles y estados de foco de los campos.

**Archivos:** `assets/css/styles.css`; `index.html` para asociar ayudas y avisos.

### 2. Alta: escala tipográfica demasiado pequeña

**Qué:** ayudas y descripciones a 9–10 px, metadatos y botones a 11 px; cuerpo
de investigación a 14 px. Los modos reducen sus nombres a 10 px en móvil.

**Por qué:** `typography.md › Ensuring legibility`: “Use font sizes that most people can read easily.”
UI/UX: Readable Font Size. No se interpreta el tamaño nativo Apple como píxeles web.

**Propuesta:** cuerpo y campos 16 px, ayudas 14 px, datos secundarios 13–14 px,
secciones 20 px, título 28–36 px. Definir escala en rem y pesos 400/500/600.
Usar tipografía del sistema, sin descargar fuentes ni cambiar políticas del servidor.

**Archivo:** `assets/css/styles.css`.

### 3. Alta: riesgo de controles apretados en pantallas pequeñas

**Qué:** los tres modos conservan columnas iguales incluso por debajo de 480 px;
se reduce el texto para hacerlos caber. Chips y descarga no definen altura mínima
cómoda; las ayudas comparten una fila. No se ha observado el desbordamiento real.

**Por qué:** `layout.md › Adaptability`: “Be prepared for text-size changes.”
UI/UX: Compact Label Overflow, content priority y horizontal-scroll.

**Propuesta:** modos en una columna hasta 480 px, sin reducir letras; ayudas que
puedan envolver. Controles con objetivo cómodo de 44 px de alto y separación de
8 px, como decisión de usabilidad, no afirmación de un mínimo WCAG universal.
Validar a 320/375/768/1024/1440 px y con zoom al 200 % antes de aceptar.

**Archivos:** `index.html`, `assets/css/styles.css`.

### 4. Alta: carga y errores pueden ocultar resultados útiles

**Qué:** al enviar otra consulta se ocultan respuesta y descarga anteriores; si
falla, no se restaura ese resultado. El error aparece después del formulario y
no se asocia al campo ni se gestiona el foco. Sí existe role="alert".

**Por qué:** `entering-data.md › Best practices` y `loading.md › Best practices`;
UI/UX: Focusable Error Summary y error-feedback.

**Propuesta:** conservar el último resultado hasta recibir uno nuevo; indicar
“Investigando…” también en el botón; asociar validación mediante aria-describedby
y aria-invalid y mover foco al campo apropiado. Mantener un estado de espera
honesto, sin inventar etapas de búsqueda ni porcentajes de avance. No añadir
cancelación que prometa detener consumo sin soporte real del backend.

**Archivos:** `index.html`, `assets/js/app.js`, `assets/css/styles.css`.

### 5. Media: el encabezado y el vacío ocupan demasiado espacio

**Qué:** título de hasta 52 px, ilustración radar y panel de resultados con altura
mínima 585 px aun vacío. Compiten con la pregunta y alargan el recorrido móvil.

**Por qué:** `layout.md › Visual hierarchy`: “Order content by relative importance.”
Reducir decoración y dar prioridad a la tarea es juicio de diseño aplicado al producto.

**Propuesta:** encabezado compacto con “Investiga tecnología con fuentes”, radar
pequeño como firma y dos paneles 40/60 en escritorio; una columna en tableta/móvil.
Vacío breve: “Tus resultados aparecerán aquí”. Sin menús o secciones nuevas.

**Archivos:** `index.html`, `assets/css/styles.css`.

### 6. Media: resultados con poca jerarquía y términos técnicos visibles

**Qué:** la respuesta se muestra como bloques de texto preformateado; sus
encabezados no se convierten en títulos semánticos. El modo aparece como `rapido`.

**Por qué:** `typography.md › Conveying hierarchy`, `writing.md › Best practices`
y `generative-ai.md › Outputs`. La información debe ser escaneable y
mantener claras sus limitaciones y fuentes.

**Propuesta:** reconocer solo los encabezados conocidos y presentarlos como
secciones HTML, preservando texto y citas con creación segura de nodos. Mostrar
“Rápido” en pantalla sin cambiar el valor enviado; mantener modelo/fecha en una
fila secundaria legible y una lista de fuentes numerada. Preservar el TXT completo.

**Archivos:** `assets/js/app.js`, `index.html`, `assets/css/styles.css`.

## Propuesta visual concreta

Dirección: **mesa de investigación tecnológica**, sobria, clara y centrada en evidencia.
Mantener el radar, la pregunta, los tres modos, Web Search, fuentes y descarga TXT.

| Rol | Color propuesto | Comprobación |
|---|---|---|
| Fondo general | `#F5F7FA` | Gris frío suave |
| Superficie | `#FFFFFF` | Paneles legibles |
| Texto principal | `#172B3A` | 14.55:1 sobre blanco |
| Texto secundario | `#526475` | 6.11:1 sobre blanco |
| Acción y foco | `#245C70` | Blanco sobre acción: 7.39:1; foco sobre fondo: 6.89:1 |
| Límites de campos | `#7D8995` | Confirmar contraste con cada superficie en implementación |

Fuente: `system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`.
Espaciado: 8/16/24/32 px; paneles con radios 12 px y sombras muy suaves.
No aplicar glassmorphism, brillos, degradados intensos ni animaciones decorativas.

Escritorio: encabezado compacto → pregunta/opciones a la izquierda → resultados
a la derecha, fuentes debajo de la respuesta. Móvil: encabezado → pregunta → modos
verticales → búsqueda web/acceso → acción → resultado → fuentes → descarga.
La interfaz debe seguir visible y operable con ampliación de texto.

Se conservan las decisiones correctas: etiquetas visibles, fieldset/legend,
foco existente, aviso de IA/costos, textos españoles, estados accesibles y
construcción de resultados sin ejecutar HTML del modelo.

## Alcance de la implementación pendiente

Solo después de aprobación: `index.html`, `assets/css/styles.css` y
`assets/js/app.js`. Opcionalmente `assets/favicon.svg` si se aprueba ajustar
el radar a la nueva paleta. No cambiar `api.js`, `config.js`, endpoints, backend,
modelo, variables de entorno ni Vercel. No hacer investigaciones pagadas para
comprobar diseño. No se implementó esta propuesta.

## Fuentes

- https://github.com/dickwu/apple-design-skill
- https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- https://learn.chatgpt.com/docs/build-skills
- Referencias locales Apple: `accessibility.md`, `layout.md`, `typography.md`,
  `color.md`, `writing.md`, `loading.md`, `entering-data.md`, `generative-ai.md`.
- Catálogos locales UI/UX Pro Max: `ux-guidelines.csv`, `typography.csv` y
  `stacks/html-tailwind.csv`; uso exclusivo de criterios pertinentes a web.
