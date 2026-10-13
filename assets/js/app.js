import {Api} from "./api.js";
import {Config} from "./config.js";
const $ = id => document.getElementById(id);
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
    $("question").addEventListener("input", () => this.contar());
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
      $("connection").textContent = state.configurada ? "● Servidor configurado" : "○ Configura tu API Key en .env";
      $("access-field").hidden = !state.acceso_requerido;
    } catch { $("connection").textContent = "○ Servidor no disponible"; }
  }
  async investigar(event) {
    event.preventDefault();
    const pregunta = $("question").value.trim();
    if (pregunta.length < 8) { $("error").textContent = "Escribe una pregunta de al menos 8 caracteres."; $("error").hidden = false; return; }
    $("error").hidden = true; $("submit").disabled = true;
    $("empty").hidden = true; $("result").hidden = true; $("download").hidden = true;
    document.querySelector(".result-panel").setAttribute("aria-busy", "true");
    $("status").textContent = "Investigando… Esto puede tardar hasta dos minutos.";
    try {
      const data = await this.api.investigar({
        pregunta, modo: document.querySelector('[name="mode"]:checked').value,
        usar_web: $("use-web").checked
      }, $("access").value.trim());
      this.resultado = data; this.mostrar(data);
      $("status").textContent = "Investigación terminada.";
    } catch(error) {
      $("error").textContent = error.message; $("error").hidden = false;
      $("status").textContent = "La investigación no pudo completarse."; $("empty").hidden = false;
    } finally {
      $("submit").disabled = false;
      document.querySelector(".result-panel").setAttribute("aria-busy", "false");
    }
  }
  mostrar(data) {
    $("metadata").textContent = new Date(data.fecha).toLocaleString("es-MX") + " · " + data.modo + " · " + data.modelo + " · " + (data.web_utilizada ? "Búsqueda web realizada" : "Sin búsqueda web confirmada");
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
      div.append(document.createTextNode(chars.slice(cursor).join(""))); $("answer").append(div);
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
      ...d.avisos, "", ...d.bloques.map(b => b.texto), "", "FUENTES",
      ...d.fuentes.map(f => f.titulo + "\n" + f.url)].join("\n\n");
    const url = URL.createObjectURL(new Blob([text], {type:"text/plain;charset=utf-8"}));
    const a = document.createElement("a"); a.href = url; a.download = "radar-tic-" + d.fecha.slice(0,10) + ".txt";
    document.body.append(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
}
new RadarApp();
