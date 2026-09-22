(function () {
  "use strict";

  const TIMEZONE = "America/Sao_Paulo";
  const STALE_DAYS_COUNTRIES = 400; // dados de religião/perseguição mudam pouco: aviso após ~13 meses
  const STALE_DAYS_MISSIONARY = 45; // pedidos de oração devem ser revisados com mais frequência

  let countriesData = null;
  let missionariesData = null;

  // ---------- Relógio em tempo real (data/hora atual, fuso do usuário) ----------
  function updateClock() {
    const now = new Date();
    const dateFmt = new Intl.DateTimeFormat("pt-BR", {
      timeZone: TIMEZONE, weekday: "long", day: "2-digit", month: "long", year: "numeric"
    });
    const timeFmt = new Intl.DateTimeFormat("pt-BR", {
      timeZone: TIMEZONE, hour: "2-digit", minute: "2-digit", second: "2-digit"
    });
    document.getElementById("clockDate").textContent = capitalize(dateFmt.format(now));
    document.getElementById("clockTime").textContent = timeFmt.format(now);
  }
  function capitalize(s) { return s.charAt(0).toUpperCase() + s.slice(1); }

  // ---------- Utilitários de data ----------
  function daysBetween(dateStr) {
    const then = new Date(dateStr + "T00:00:00");
    const now = new Date();
    return Math.floor((now - then) / (1000 * 60 * 60 * 24));
  }
  function formatDateBR(dateStr) {
    if (!dateStr) return "—";
    const d = new Date(dateStr + "T00:00:00");
    return new Intl.DateTimeFormat("pt-BR", { timeZone: TIMEZONE, day: "2-digit", month: "2-digit", year: "numeric" }).format(d);
  }

  // ---------- Carregamento dos dados ----------
  async function loadData() {
    const [cRes, mRes] = await Promise.all([
      fetch("data/countries.json", { cache: "no-store" }),
      fetch("data/missionaries.json", { cache: "no-store" }),
    ]);
    countriesData = await cRes.json();
    missionariesData = await mRes.json();
  }

  function renderFreshnessBar() {
    const bar = document.getElementById("freshnessBar");
    const text = document.getElementById("freshnessText");
    const genDate = countriesData.meta.generatedAt.slice(0, 10);
    const days = daysBetween(genDate);
    const stale = days > STALE_DAYS_COUNTRIES;
    bar.classList.toggle("stale", stale);
    const now = new Date();
    const nowFmt = new Intl.DateTimeFormat("pt-BR", {
      timeZone: TIMEZONE, day: "2-digit", month: "2-digit", year: "numeric", hour: "2-digit", minute: "2-digit"
    }).format(now);
    text.textContent = stale
      ? `⚠️ Dados de países/perseguição gerados em ${formatDateBR(genDate)} (${days} dias atrás). Revise as fontes originais. Consulta feita agora: ${nowFmt}.`
      : `✅ Dados de países/perseguição gerados em ${formatDateBR(genDate)}. Consulta feita agora, ${nowFmt} (${TIMEZONE}).`;
    document.getElementById("footerGenDate").textContent = formatDateBR(genDate);
  }

  // ---------- Aba Países ----------
  function renderStats() {
    const list = countriesData.countries;
    const sovereign = list.filter(c => c.isSovereignState).length;
    const avgEvangelical = average(list.map(c => c.pctEvangelical).filter(v => v !== null && v !== undefined));
    const persecuted = list.filter(c => c.persecutionRank2026).length;
    const extreme = list.filter(c => c.persecutionLevel === "Extrema").length;

    const tiles = [
      { num: sovereign, lbl: "Países soberanos cobertos" },
      { num: avgEvangelical.toFixed(1) + "%", lbl: "Média de evangélicos" },
      { num: persecuted, lbl: "Na Lista de Perseguição 2026" },
      { num: extreme, lbl: "Em perseguição extrema" },
    ];
    document.getElementById("statsRow").innerHTML = tiles.map(t =>
      `<div class="stat-tile"><div class="num">${t.num}</div><div class="lbl">${t.lbl}</div></div>`
    ).join("");
  }
  function average(arr) {
    if (!arr.length) return 0;
    return arr.reduce((a, b) => a + b, 0) / arr.length;
  }

  function populateRegionFilter() {
    const regions = [...new Set(countriesData.countries.map(c => c.region))].sort();
    const sel = document.getElementById("regionFilter");
    regions.forEach(r => {
      const opt = document.createElement("option");
      opt.value = r; opt.textContent = r;
      sel.appendChild(opt);
    });
  }

  function levelClass(level) {
    if (level === "Extrema") return "level-extrema";
    if (level === "Muito Alta") return "level-muitoalta";
    if (level === "Alta") return "level-alta";
    return "";
  }

  function countryCard(c) {
    const ev = c.pctEvangelical;
    const other = c.pctOtherReligions;
    const evLabel = (ev === null || ev === undefined) ? "sem dado" : ev + "%";
    const evWidth = (ev === null || ev === undefined) ? 0 : Math.min(ev, 100);
    const otherLabel = (other === null || other === undefined) ? "sem dado" : other + "%";
    const otherWidth = (other === null || other === undefined) ? 0 : Math.min(other, 100);
    const persec = c.persecutionRank2026
      ? `<span class="badge ${levelClass(c.persecutionLevel)}">#${c.persecutionRank2026} · ${c.persecutionLevel}</span>`
      : "";
    const territoryTag = c.isSovereignState ? "" : `<span class="badge level-muitoalta" title="Território/região administrativa, não é um Estado soberano">Território</span>`;
    return `
      <div class="country-card">
        <h3>${c.name} <span class="region-tag">${c.region}</span></h3>
        ${territoryTag}
        <div class="rel-primary">Religião predominante: <strong>${c.primaryReligion}</strong></div>
        <div class="bar-row">
          <div class="bar-label"><span>Evangélicos</span><span>${evLabel}</span></div>
          <div class="bar-track"><div class="bar-fill evangelical" style="width:${evWidth}%"></div></div>
        </div>
        <div class="bar-row">
          <div class="bar-label"><span>Outras religiões / sem religião</span><span>${otherLabel}</span></div>
          <div class="bar-track"><div class="bar-fill other" style="width:${otherWidth}%"></div></div>
        </div>
        ${persec ? `<div class="persec-tag">${persec}</div>` : ""}
        <div class="pop">População: ${c.population ? c.population.toLocaleString("pt-BR") : "—"}</div>
      </div>`;
  }

  function getFilteredSortedCountries() {
    const q = document.getElementById("searchCountry").value.trim().toLowerCase();
    const region = document.getElementById("regionFilter").value;
    const sort = document.getElementById("sortSelect").value;
    const includeTerritories = document.getElementById("includeTerritories").checked;

    let list = countriesData.countries.filter(c => {
      const matchQ = !q || c.name.toLowerCase().includes(q) || c.primaryReligion.toLowerCase().includes(q);
      const matchR = !region || c.region === region;
      const matchSov = includeTerritories || c.isSovereignState;
      return matchQ && matchR && matchSov;
    });

    const byNum = (v) => (v === null || v === undefined ? -1 : v);
    switch (sort) {
      case "evangelical-asc": list.sort((a, b) => byNum(a.pctEvangelical) - byNum(b.pctEvangelical)); break;
      case "evangelical-desc": list.sort((a, b) => byNum(b.pctEvangelical) - byNum(a.pctEvangelical)); break;
      case "population-desc": list.sort((a, b) => byNum(b.population) - byNum(a.population)); break;
      case "persecution-asc": list.sort((a, b) => (a.persecutionRank2026 || 999) - (b.persecutionRank2026 || 999)); break;
      default: list.sort((a, b) => a.name.localeCompare(b.name, "pt-BR"));
    }
    return list;
  }

  function renderCountries() {
    const list = getFilteredSortedCountries();
    const grid = document.getElementById("countryGrid");
    const empty = document.getElementById("countryEmpty");
    grid.innerHTML = list.map(countryCard).join("");
    empty.hidden = list.length !== 0;
  }

  // ---------- Aba Perseguição ----------
  function renderPersecutionList() {
    const list = countriesData.countries
      .filter(c => c.persecutionRank2026)
      .sort((a, b) => a.persecutionRank2026 - b.persecutionRank2026);
    const container = document.getElementById("persecutionList");
    container.innerHTML = list.map(c => `
      <div class="persecution-card">
        <span class="rank">#${c.persecutionRank2026}</span>
        <span class="pname">${c.name} <span class="pregion">· ${c.region}</span></span>
        <span class="badge ${levelClass(c.persecutionLevel)}">${c.persecutionLevel}</span>
      </div>
    `).join("");
  }

  // ---------- Aba Missionários ----------
  function missionaryCard(m) {
    const days = daysBetween(m.lastUpdated);
    const stale = days > STALE_DAYS_MISSIONARY;
    return `
      <div class="missionary-card">
        <h3>${m.name}</h3>
        <div class="agency">${m.agency}</div>
        <div class="field">📍 ${m.field} ${m.fieldCountry ? `(${m.fieldCountry})` : ""} · desde ${m.since}</div>
        <div class="focus">${m.focus}</div>
        <div class="prayer-title">Pedidos de oração</div>
        <ul class="prayer-list">${m.prayerRequests.map(p => `<li>${p}</li>`).join("")}</ul>
        <div class="updated ${stale ? "stale" : ""}">
          ${stale ? "⚠️" : "🕒"} Atualizado em ${formatDateBR(m.lastUpdated)} (${days} dia${days === 1 ? "" : "s"} atrás)
        </div>
      </div>`;
  }

  function renderMissionaries() {
    const q = document.getElementById("searchMissionary").value.trim().toLowerCase();
    const list = missionariesData.missionaries.filter(m => {
      if (!q) return true;
      return [m.name, m.agency, m.field, m.fieldCountry].join(" ").toLowerCase().includes(q);
    });
    const grid = document.getElementById("missionaryGrid");
    const empty = document.getElementById("missionaryEmpty");
    grid.innerHTML = list.map(missionaryCard).join("");
    empty.hidden = list.length !== 0;
  }

  // ---------- Aba Sobre ----------
  function renderSources() {
    const ul = document.getElementById("sourcesList");
    ul.innerHTML = countriesData.meta.sources.map(s => `
      <li><strong>${s.name}</strong> — <a href="${s.url}" target="_blank" rel="noopener">${s.url}</a>
        <br><span style="font-size:.8rem;color:var(--ink-soft)">Consultado em ${formatDateBR(s.retrievedAt)}${s.note ? " · " + s.note : ""}</span>
      </li>
    `).join("");
  }

  // ---------- Abas ----------
  function setupTabs() {
    document.querySelectorAll(".tab-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
        document.querySelectorAll(".tab-panel").forEach(p => p.classList.remove("active"));
        btn.classList.add("active");
        document.getElementById("tab-" + btn.dataset.tab).classList.add("active");
      });
    });
  }

  // ---------- Inicialização ----------
  async function init() {
    updateClock();
    setInterval(updateClock, 1000);
    setupTabs();

    try {
      await loadData();
    } catch (err) {
      document.getElementById("freshnessText").textContent = "❌ Não foi possível carregar os dados (data/countries.json ou data/missionaries.json).";
      console.error(err);
      return;
    }

    renderFreshnessBar();
    renderStats();
    populateRegionFilter();
    renderCountries();
    renderPersecutionList();
    renderMissionaries();
    renderSources();

    // Avisa outros scripts (mapa) que os dados já estão prontos
    window.missoesData = { countries: countriesData, missionaries: missionariesData };
    document.dispatchEvent(new CustomEvent("missoes:data-ready", { detail: countriesData }));

    document.getElementById("countrySummaryNote").textContent = countriesData.meta.countrySummary || "";
    document.getElementById("searchCountry").addEventListener("input", renderCountries);
    document.getElementById("regionFilter").addEventListener("change", renderCountries);
    document.getElementById("sortSelect").addEventListener("change", renderCountries);
    document.getElementById("includeTerritories").addEventListener("change", renderCountries);
    document.getElementById("searchMissionary").addEventListener("input", renderMissionaries);
  }

  document.addEventListener("DOMContentLoaded", init);
})();
