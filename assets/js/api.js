import {Config} from "./config.js";
export class Api {
  async investigar(payload, access = "") {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), Config.timeout);
    try {
      const response = await fetch(Config.endpoint, {
        method: "POST",
        headers: {"Content-Type": "application/json", ...(access ? {"X-Access-Token": access} : {})},
        body: JSON.stringify(payload), signal: controller.signal
      });
      let data;
      try { data = await response.json(); } catch { throw new Error("El servidor no devolvió una respuesta válida. Revisa su estado o los logs de Vercel."); }
      if (!response.ok) {
        throw new Error(typeof data.detail === "string" ? data.detail : "Verifica que la pregunta tenga de 8 a 2000 caracteres y el modo sea válido.");
      }
      return data;
    } catch (error) {
      if (error.name === "AbortError") throw new Error("La consulta excedió el tiempo de espera. Prueba el modo rápido. El servidor podría seguir procesándola.");
      if (error instanceof TypeError) throw new Error("No se pudo conectar con el servidor. Abre la aplicación desde http://127.0.0.1:5000.");
      throw error;
    } finally { clearTimeout(timer); }
  }
}
