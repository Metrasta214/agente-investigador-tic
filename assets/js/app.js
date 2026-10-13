import {Api} from "./api.js";
import {Config} from "./config.js";
const $ = id => document.getElementById(id);
const modos = {rapido: "Rápido", comparativo: "Comparativo", profundo: "Profundo"};
function textoConTitulos(parent, texto) {
  const lineas = texto.split("\n");
  for (const [index, linea] of lineas.entries()) {
    const match = linea.trim().match(/^(?:#{1,3}\s*)?(?:\*\*)?(Resumen|Hallazgos|Coincidencias|Diferencias|Tendencias|Conclusión|Fuentes):?(?:\*\*)?:?$/i);
    if (match) { const h = document.createElement("h3"); h.textContent = match[1]; parent.append(h); }
    else parent.append(document.createTextNode(linea + (index < lineas.length - 1 ? "\n" : "")));
  }
}
function enlace(url, titulo) {
  const node = document.createElement("a");
  const parsed = new URL(url);
  if (!["https:", "http:"].includes(parsed.protocol)) throw new Error("URL no admitida");
  node.href = parsed.href; node.textContent = titulo; node.target = "_blank"; node.rel = "noopener noreferrer";
  return node;
}
class RadarApp {
  constructor() {
    this.api = new Api(); this.resultado = null;
    $("research-form").addEventListener("submit", e => this.investigar(e));
    $("question").addEventListener("input", () => { this.contar(); $("question").removeAttribute("aria-invalid"); });
    document.querySelectorAll("[data-question]").forEach(button => button.addEventListener("click", () => {
      $("question").value = button.dataset.question; this.contar(); $("question").focus();
    }));
    $("download").addEventListener("click", () => this.descargar());
    this.conectar();
  }
  contar() { $("count").textContent = $("question").value.length + " / 2000"; }
  async conectar() {
    try {
      const response = await fetch(Config.health, {signal: AbortSignal.timeout(15000)});
      if (!response.ok) throw new Error();
      const state = await response.json();
      $("connection").textContent = state.configurada ? "● Servicio disponible" : "○ Servicio pendiente de configuración";
      $("connection").dataset.state = state.configurada ? "ready" : "offline";
      $("access-field").hidden = !state.acceso_requerido;
    } catch { $("connection").textContent = "○ Servicio no disponible"; $("connection").dataset.state = "offline"; }
  }
  async investigar(event) {
    event.preventDefault();
    const pregunta = $("question").value.trim();
    if (pregunta.length < 8) { $("error").textContent = "Escribe una pregunta de al menos 8 caracteres."; $("error").hidden = false; $("question").setAttribute("aria-invalid", "true"); $("question").focus(); return; }
    $("error").hidden = true; $("submit").disabled = true;
    $("submit").textContent = "Investigando…";
    $("empty").hidden = true;
    document.querySelector(".result-panel").setAttribute("aria-busy", "true");
    $("status").textContent = "Investigando… Esto puede tardar hasta dos minutos.";
    try {
      const data = await this.api.investigar({
        pregunta, modo: document.querySelector('[name="mode"]:checked').value,
        usar_web: $("use-web").checked
      }, $("access").value.trim());
      this.resultado = data; this.mostrar(data);
      $("status").textContent = "Investigación terminada.";
      $("result").focus({preventScroll: true});
      if (window.matchMedia("(max-width: 900px)").matches) $("result").scrollIntoView({block: "start", behavior: "auto"});
    } catch(error) {
      $("error").textContent = error.message; $("error").hidden = false;
      $("status").textContent = this.resultado ? "La nueva consulta falló. Conservamos tu último resultado." : "La investigación no pudo completarse.";
      $("empty").hidden = Boolean(this.resultado);
    } finally {
      $("submit").disabled = false;
      $("submit").textContent = "Iniciar investigación ↗";
      document.querySelector(".result-panel").setAttribute("aria-busy", "false");
    }
  }
  mostrar(data) {
    $("result-question").textContent = data.pregunta;
    $("metadata").textContent = new Date(data.fecha).toLocaleString("es-MX") + " · " + (modos[data.modo] || data.modo) + " · " + data.modelo + " · " + (data.web_utilizada ? "Búsqueda web realizada" : "Sin búsqueda web confirmada");
    $("answer").replaceChildren(); $("warnings").replaceChildren(); $("source-list").replaceChildren();
    for (const aviso of data.avisos) { const p = document.createElement("p"); p.textContent = aviso; $("warnings").append(p); }
    for (const bloque of data.bloques) {
      const div = document.createElement("div"); div.className = "block";
      // Los índices Python cuentan puntos de código, no unidades UTF-16.
      const chars = Array.from(bloque.texto); let cursor = 0;
      for (const cita of [...bloque.citas].sort((a,b) => a.inicio - b.inicio)) {
        if (cita.inicio < cursor || cita.fin > chars.length) continue;
        div.append(document.createTextNode(chars.slice(cursor, cita.inicio).join("")));
        try { div.append(enlace(cita.url, "[" + cita.titulo + "]")); } catch { div.append(document.createTextNode(chars.slice(cita.inicio, cita.fin).join(""))); }
        cursor = cita.fin;
      }
      div.append(document.createTextNode(chars.slice(cursor).join("")));
      for (const node of [...div.childNodes]) {
        if (node.nodeType !== Node.TEXT_NODE) continue;
        const fragment = document.createDocumentFragment();
        textoConTitulos(fragment, node.textContent); node.replaceWith(fragment);
      }
      $("answer").append(div);
    }
    for (const fuente of data.fuentes) {
      const li = document.createElement("li");
      try { li.append(enlace(fuente.url, fuente.titulo)); $("source-list").append(li); } catch { /* URL no segura */ }
    }
    $("sources").hidden = data.fuentes.length === 0;
    $("result").hidden = false; $("download").hidden = false;
  }
  descargar() {
    if (!this.resultado) return;
    const d = this.resultado;
    const text = ["RADAR TIC", d.pregunta, "Fecha: " + d.fecha, "Modo: " + d.modo,
      "Modelo: " + d.modelo, "Web solicitada: " + d.web_solicitada, "Web utilizada: " + d.web_utilizada,
      "Estado: " + d.estado, "Llamadas web: " + d.web_llamadas, "Tokens: " + JSON.stringify(d.tokens),
      ...d.avisos, "", ...d.bloques.map(b => b.texto), "", "FUENTES",
      ...d.fuentes.map(f => f.titulo + "\n" + f.url)].join("\n\n");
    const url = URL.createObjectURL(new Blob([text], {type:"text/plain;charset=utf-8"}));
    const a = document.createElement("a"); a.href = url; a.download = "radar-tic-" + d.fecha.slice(0,10) + ".txt";
    document.body.append(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
}
new RadarApp();
