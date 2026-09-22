(function () {
  "use strict";

  // Cores da escala sequencial de gravidade de perseguição (claro -> escuro = mais grave)
  // Mesmos valores das variáveis CSS --lvl-*, lidos em runtime para já respeitar modo claro/escuro.
  function cssVar(name) {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  }

  const WIDTH = 960;
  const HEIGHT = 500;
  let rendered = false;

  function colorForCountry(c) {
    if (!c) return cssVar("--lvl-nodata") || "#9a978d";
    switch (c.persecutionLevel) {
      case "Extrema": return cssVar("--lvl-extrema") || "#7a1f17";
      case "Muito Alta": return cssVar("--lvl-muitoalta") || "#b5432f";
      case "Alta": return cssVar("--lvl-alta") || "#d98868";
      default: return cssVar("--lvl-none") || "#6b7a70";
    }
  }

  function buildIsoIndex(countries) {
    const byIso = new Map();
    countries.forEach(c => {
      if (c.isoNumeric) byIso.set(String(parseInt(c.isoNumeric, 10)), c);
    });
    return byIso;
  }

  async function renderMap(countriesData) {
    if (rendered || !window.d3 || !window.topojson) return;
    const container = document.getElementById("worldMap");
    const tooltip = document.getElementById("mapTooltip");
    if (!container) return;

    let world;
    try {
      world = await d3.json("https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json");
    } catch (err) {
      container.innerHTML = `<p style="padding:20px;color:var(--ink-soft)">Não foi possível carregar o mapa-múndi (é necessário estar conectado à internet). As demais abas continuam funcionando normalmente.</p>`;
      console.error(err);
      return;
    }

    const geo = topojson.feature(world, world.objects.countries);
    const byIso = buildIsoIndex(countriesData.countries);

    const svg = d3.select(container).append("svg")
      .attr("viewBox", `0 0 ${WIDTH} ${HEIGHT}`)
      .attr("preserveAspectRatio", "xMidYMid meet")
      .attr("role", "img")
      .attr("aria-label", "Mapa mundial colorido por nível de perseguição religiosa");

    const projection = d3.geoNaturalEarth1().fitSize([WIDTH, HEIGHT], geo);
    const path = d3.geoPath(projection);

    svg.selectAll("path")
      .data(geo.features)
      .join("path")
      .attr("d", path)
      .attr("fill", d => colorForCountry(byIso.get(String(parseInt(d.id, 10)))))
      .on("mousemove", function (event, d) {
        const c = byIso.get(String(parseInt(d.id, 10)));
        const rect = container.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        tooltip.hidden = false;
        tooltip.style.left = Math.min(x + 14, rect.width - 230) + "px";
        tooltip.style.top = Math.max(y - 10, 0) + "px";
        if (c) {
          const rank = c.persecutionRank2026 ? `#${c.persecutionRank2026} na LMP 2026 · ${c.persecutionLevel}` : "Fora da Lista de Perseguição 2026";
          const ev = (c.pctEvangelical === null || c.pctEvangelical === undefined) ? "sem dado" : c.pctEvangelical + "%";
          tooltip.innerHTML = `<strong>${c.name}</strong>${rank}<br>Evangélicos: ${ev}`;
        } else {
          tooltip.innerHTML = `<strong>${d.properties && d.properties.name ? d.properties.name : "Território"}</strong>Sem dado no painel`;
        }
      })
      .on("mouseleave", function () {
        tooltip.hidden = true;
      });

    rendered = true;

    // Nota de atualização (reaproveita a data de geração dos dados de perseguição)
    const note = document.getElementById("mapUpdateNote");
    if (note && countriesData.meta && countriesData.meta.generatedAt) {
      const genDate = countriesData.meta.generatedAt.slice(0, 10);
      const d = new Date(genDate + "T00:00:00");
      const formatted = new Intl.DateTimeFormat("pt-BR", { timeZone: "America/Sao_Paulo", day: "2-digit", month: "2-digit", year: "numeric" }).format(d);
      note.textContent = `Mapa baseado na Lista Mundial da Perseguição 2026 (Portas Abertas), dados gerados em ${formatted}. Atualize junto com data/countries.json quando sair uma nova edição da lista (normalmente em janeiro).`;
    }
  }

  function init() {
    if (window.missoesData) {
      renderMap(window.missoesData.countries);
    } else {
      document.addEventListener("missoes:data-ready", (e) => renderMap({ countries: e.detail.countries, meta: e.detail.meta }), { once: true });
    }
    // Garante que o mapa é desenhado corretamente na primeira vez que a aba é aberta
    document.querySelectorAll('.tab-btn[data-tab="mapa"]').forEach(btn => {
      btn.addEventListener("click", () => {
        if (window.missoesData) renderMap(window.missoesData.countries);
      });
    });
  }

  document.addEventListener("DOMContentLoaded", init);
})();
