# -*- coding: utf-8 -*-
"""
Gera data/countries.json com TODOS os países/territórios disponíveis na
tabela do Joshua Project (joshuaproject.net/global/countries), cruzados com
o ranking da Lista Mundial da Perseguição 2026 (Portas Abertas).

Cobre os 193 Estados-membros da ONU + Vaticano + Palestina (State of
Palestine / West Bank-Gaza) = 195 "países do mundo", mais alguns territórios
de relevância missionária (Taiwan, Hong Kong, Macau, Kosovo) claramente
marcados como não soberanos (isSovereignState = false) para quem quiser
filtrá-los.
"""
import json
import datetime

RAW_FILE = "jp_raw_table.txt"

# Tradução PT-BR + região + soberania (True = um dos 193 membros da ONU +
# Vaticano + Palestina; False = território/região autônoma)
META = {
    "Afghanistan": ("Afeganistão", "Ásia", True),
    "Albania": ("Albânia", "Europa", True),
    "Algeria": ("Argélia", "África", True),
    "American Samoa": ("Samoa Americana", "Oceania", False),
    "Andorra": ("Andorra", "Europa", True),
    "Angola": ("Angola", "África", True),
    "Anguilla": ("Anguilla", "América Latina", False),
    "Antigua and Barbuda": ("Antígua e Barbuda", "América Latina", True),
    "Argentina": ("Argentina", "América Latina", True),
    "Armenia": ("Armênia", "Ásia", True),
    "Aruba": ("Aruba", "América Latina", False),
    "Australia": ("Austrália", "Oceania", True),
    "Austria": ("Áustria", "Europa", True),
    "Azerbaijan": ("Azerbaijão", "Ásia", True),
    "Bahamas": ("Bahamas", "América Latina", True),
    "Bahrain": ("Bahrein", "Oriente Médio", True),
    "Bangladesh": ("Bangladesh", "Ásia", True),
    "Barbados": ("Barbados", "América Latina", True),
    "Belarus": ("Belarus", "Europa", True),
    "Belgium": ("Bélgica", "Europa", True),
    "Belize": ("Belize", "América Latina", True),
    "Benin": ("Benin", "África", True),
    "Bermuda": ("Bermudas", "América do Norte", False),
    "Bhutan": ("Butão", "Ásia", True),
    "Bolivia": ("Bolívia", "América Latina", True),
    "Bosnia-Herzegovina": ("Bósnia e Herzegovina", "Europa", True),
    "Botswana": ("Botsuana", "África", True),
    "Brazil": ("Brasil", "América Latina", True),
    "Brunei": ("Brunei", "Ásia", True),
    "Bulgaria": ("Bulgária", "Europa", True),
    "Burkina Faso": ("Burkina Faso", "África", True),
    "Burundi": ("Burundi", "África", True),
    "Cambodia": ("Camboja", "Ásia", True),
    "Cameroon": ("Camarões", "África", True),
    "Canada": ("Canadá", "América do Norte", True),
    "Cape Verde": ("Cabo Verde", "África", True),
    "Cayman Islands": ("Ilhas Cayman", "América Latina", False),
    "Central African Republic": ("República Centro-Africana", "África", True),
    "Chad": ("Chade", "África", True),
    "Chile": ("Chile", "América Latina", True),
    "China": ("China", "Ásia", True),
    "China, Hong Kong": ("Hong Kong", "Ásia", False),
    "China, Macau": ("Macau", "Ásia", False),
    "Colombia": ("Colômbia", "América Latina", True),
    "Comoros": ("Comores", "África", True),
    "Congo, Democratic Republic of": ("República Democrática do Congo", "África", True),
    "Congo, Republic of the": ("República do Congo", "África", True),
    "Costa Rica": ("Costa Rica", "América Latina", True),
    "Cote d'Ivoire": ("Costa do Marfim", "África", True),
    "Croatia": ("Croácia", "Europa", True),
    "Cuba": ("Cuba", "América Latina", True),
    "Curacao": ("Curaçao", "América Latina", False),
    "Cyprus": ("Chipre", "Europa", True),
    "Czechia": ("Tchéquia", "Europa", True),
    "Denmark": ("Dinamarca", "Europa", True),
    "Djibouti": ("Djibuti", "África", True),
    "Dominica": ("Dominica", "América Latina", True),
    "Dominican Republic": ("República Dominicana", "América Latina", True),
    "Ecuador": ("Equador", "América Latina", True),
    "Egypt": ("Egito", "África", True),
    "El Salvador": ("El Salvador", "América Latina", True),
    "Equatorial Guinea": ("Guiné Equatorial", "África", True),
    "Eritrea": ("Eritreia", "África", True),
    "Estonia": ("Estônia", "Europa", True),
    "Eswatini": ("Essuatíni", "África", True),
    "Ethiopia": ("Etiópia", "África", True),
    "Fiji": ("Fiji", "Oceania", True),
    "Finland": ("Finlândia", "Europa", True),
    "France": ("França", "Europa", True),
    "Gabon": ("Gabão", "África", True),
    "Gambia": ("Gâmbia", "África", True),
    "Georgia": ("Geórgia", "Ásia", True),
    "Germany": ("Alemanha", "Europa", True),
    "Ghana": ("Gana", "África", True),
    "Greece": ("Grécia", "Europa", True),
    "Grenada": ("Granada", "América Latina", True),
    "Guatemala": ("Guatemala", "América Latina", True),
    "Guinea": ("Guiné", "África", True),
    "Guinea-Bissau": ("Guiné-Bissau", "África", True),
    "Guyana": ("Guiana", "América Latina", True),
    "Haiti": ("Haiti", "América Latina", True),
    "Honduras": ("Honduras", "América Latina", True),
    "Hungary": ("Hungria", "Europa", True),
    "Iceland": ("Islândia", "Europa", True),
    "India": ("Índia", "Ásia", True),
    "Indonesia": ("Indonésia", "Ásia", True),
    "Iran": ("Irã", "Oriente Médio", True),
    "Iraq": ("Iraque", "Oriente Médio", True),
    "Ireland": ("Irlanda", "Europa", True),
    "Israel": ("Israel", "Oriente Médio", True),
    "Italy": ("Itália", "Europa", True),
    "Jamaica": ("Jamaica", "América Latina", True),
    "Japan": ("Japão", "Ásia", True),
    "Jordan": ("Jordânia", "Oriente Médio", True),
    "Kazakhstan": ("Cazaquistão", "Ásia", True),
    "Kenya": ("Quênia", "África", True),
    "Kiribati": ("Kiribati", "Oceania", True),
    "Korea, North": ("Coreia do Norte", "Ásia", True),
    "Korea, South": ("Coreia do Sul", "Ásia", True),
    "Kosovo": ("Kosovo", "Europa", False),
    "Kuwait": ("Kuwait", "Oriente Médio", True),
    "Kyrgyzstan": ("Quirguistão", "Ásia", True),
    "Laos": ("Laos", "Ásia", True),
    "Latvia": ("Letônia", "Europa", True),
    "Lebanon": ("Líbano", "Oriente Médio", True),
    "Lesotho": ("Lesoto", "África", True),
    "Liberia": ("Libéria", "África", True),
    "Libya": ("Líbia", "África", True),
    "Liechtenstein": ("Liechtenstein", "Europa", True),
    "Lithuania": ("Lituânia", "Europa", True),
    "Luxembourg": ("Luxemburgo", "Europa", True),
    "Madagascar": ("Madagascar", "África", True),
    "Malawi": ("Malawi", "África", True),
    "Malaysia": ("Malásia", "Ásia", True),
    "Maldives": ("Maldivas", "Ásia", True),
    "Mali": ("Mali", "África", True),
    "Malta": ("Malta", "Europa", True),
    "Marshall Islands": ("Ilhas Marshall", "Oceania", True),
    "Mauritania": ("Mauritânia", "África", True),
    "Mauritius": ("Maurício", "África", True),
    "Mexico": ("México", "América Latina", True),
    "Micronesia, Federated States": ("Micronésia", "Oceania", True),
    "Moldova": ("Moldávia", "Europa", True),
    "Monaco": ("Mônaco", "Europa", True),
    "Mongolia": ("Mongólia", "Ásia", True),
    "Montenegro": ("Montenegro", "Europa", True),
    "Morocco": ("Marrocos", "África", True),
    "Mozambique": ("Moçambique", "África", True),
    "Myanmar (Burma)": ("Mianmar", "Ásia", True),
    "Namibia": ("Namíbia", "África", True),
    "Nauru": ("Nauru", "Oceania", True),
    "Nepal": ("Nepal", "Ásia", True),
    "Netherlands": ("Países Baixos", "Europa", True),
    "New Zealand": ("Nova Zelândia", "Oceania", True),
    "Nicaragua": ("Nicarágua", "América Latina", True),
    "Niger": ("Níger", "África", True),
    "Nigeria": ("Nigéria", "África", True),
    "North Macedonia": ("Macedônia do Norte", "Europa", True),
    "Norway": ("Noruega", "Europa", True),
    "Oman": ("Omã", "Oriente Médio", True),
    "Pakistan": ("Paquistão", "Ásia", True),
    "Palau": ("Palau", "Oceania", True),
    "Panama": ("Panamá", "América Latina", True),
    "Papua New Guinea": ("Papua-Nova Guiné", "Oceania", True),
    "Paraguay": ("Paraguai", "América Latina", True),
    "Peru": ("Peru", "América Latina", True),
    "Philippines": ("Filipinas", "Ásia", True),
    "Poland": ("Polônia", "Europa", True),
    "Portugal": ("Portugal", "Europa", True),
    "Qatar": ("Catar", "Oriente Médio", True),
    "Romania": ("Romênia", "Europa", True),
    "Russia": ("Rússia", "Europa", True),
    "Rwanda": ("Ruanda", "África", True),
    "Saint Kitts and Nevis": ("São Cristóvão e Névis", "América Latina", True),
    "Saint Lucia": ("Santa Lúcia", "América Latina", True),
    "Samoa": ("Samoa", "Oceania", True),
    "San Marino": ("San Marino", "Europa", True),
    "Sao Tome and Principe": ("São Tomé e Príncipe", "África", True),
    "Saudi Arabia": ("Arábia Saudita", "Oriente Médio", True),
    "Senegal": ("Senegal", "África", True),
    "Serbia": ("Sérvia", "Europa", True),
    "Seychelles": ("Seicheles", "África", True),
    "Sierra Leone": ("Serra Leoa", "África", True),
    "Singapore": ("Singapura", "Ásia", True),
    "Slovakia": ("Eslováquia", "Europa", True),
    "Slovenia": ("Eslovênia", "Europa", True),
    "Solomon Islands": ("Ilhas Salomão", "Oceania", True),
    "Somalia": ("Somália", "África", True),
    "South Africa": ("África do Sul", "África", True),
    "South Sudan": ("Sudão do Sul", "África", True),
    "Spain": ("Espanha", "Europa", True),
    "Sri Lanka": ("Sri Lanka", "Ásia", True),
    "St Vincent and Grenadines": ("São Vicente e Granadinas", "América Latina", True),
    "Sudan": ("Sudão", "África", True),
    "Suriname": ("Suriname", "América Latina", True),
    "Sweden": ("Suécia", "Europa", True),
    "Switzerland": ("Suíça", "Europa", True),
    "Syria": ("Síria", "Oriente Médio", True),
    "Taiwan": ("Taiwan", "Ásia", False),
    "Tajikistan": ("Tajiquistão", "Ásia", True),
    "Tanzania": ("Tanzânia", "África", True),
    "Thailand": ("Tailândia", "Ásia", True),
    "Timor-Leste": ("Timor-Leste", "Ásia", True),
    "Togo": ("Togo", "África", True),
    "Tonga": ("Tonga", "Oceania", True),
    "Trinidad and Tobago": ("Trinidad e Tobago", "América Latina", True),
    "Tunisia": ("Tunísia", "África", True),
    "Turkiye (Turkey)": ("Turquia", "Oriente Médio", True),
    "Turkmenistan": ("Turcomenistão", "Ásia", True),
    "Tuvalu": ("Tuvalu", "Oceania", True),
    "Uganda": ("Uganda", "África", True),
    "Ukraine": ("Ucrânia", "Europa", True),
    "United Arab Emirates": ("Emirados Árabes Unidos", "Oriente Médio", True),
    "United Kingdom": ("Reino Unido", "Europa", True),
    "United States": ("Estados Unidos", "América do Norte", True),
    "Uruguay": ("Uruguai", "América Latina", True),
    "Uzbekistan": ("Uzbequistão", "Ásia", True),
    "Vanuatu": ("Vanuatu", "Oceania", True),
    "Venezuela": ("Venezuela", "América Latina", True),
    "Vietnam": ("Vietnã", "Ásia", True),
    "West Bank / Gaza": ("Palestina", "Oriente Médio", True),
    "Yemen": ("Iêmen", "Oriente Médio", True),
    "Zambia": ("Zâmbia", "África", True),
    "Zimbabwe": ("Zimbábue", "África", True),
    "Vatican City": ("Vaticano", "Europa", True),
}

# Código numérico ISO 3166-1 (como string, sem zeros à esquerda) - usado para
# ligar cada país ao mapa-múndi (topojson world-atlas, que identifica cada
# país pelo seu código numérico ISO). Kosovo não tem código ISO 3166-1
# oficial (status contestado) e fica sem mapa colorido, mas continua listado
# normalmente nas demais abas do app.
ISO_NUMERIC = {
    "Afghanistan": "4", "Albania": "8", "Algeria": "12", "American Samoa": "16",
    "Andorra": "20", "Angola": "24", "Anguilla": "660", "Antigua and Barbuda": "28",
    "Argentina": "32", "Armenia": "51", "Aruba": "533", "Australia": "36",
    "Austria": "40", "Azerbaijan": "31", "Bahamas": "44", "Bahrain": "48",
    "Bangladesh": "50", "Barbados": "52", "Belarus": "112", "Belgium": "56",
    "Belize": "84", "Benin": "204", "Bermuda": "60", "Bhutan": "64",
    "Bolivia": "68", "Bosnia-Herzegovina": "70", "Botswana": "72", "Brazil": "76",
    "Brunei": "96", "Bulgaria": "100", "Burkina Faso": "854", "Burundi": "108",
    "Cambodia": "116", "Cameroon": "120", "Canada": "124", "Cape Verde": "132",
    "Cayman Islands": "136", "Central African Republic": "140", "Chad": "148",
    "Chile": "152", "China": "156", "China, Hong Kong": "344", "China, Macau": "446",
    "Colombia": "170", "Comoros": "174", "Congo, Democratic Republic of": "180",
    "Congo, Republic of the": "178", "Costa Rica": "188", "Cote d'Ivoire": "384",
    "Croatia": "191", "Cuba": "192", "Curacao": "531", "Cyprus": "196",
    "Czechia": "203", "Denmark": "208", "Djibouti": "262", "Dominica": "212",
    "Dominican Republic": "214", "Ecuador": "218", "Egypt": "818", "El Salvador": "222",
    "Equatorial Guinea": "226", "Eritrea": "232", "Estonia": "233", "Eswatini": "748",
    "Ethiopia": "231", "Fiji": "242", "Finland": "246", "France": "250",
    "Gabon": "266", "Gambia": "270", "Georgia": "268", "Germany": "276",
    "Ghana": "288", "Greece": "300", "Grenada": "308", "Guatemala": "320",
    "Guinea": "324", "Guinea-Bissau": "624", "Guyana": "328", "Haiti": "332",
    "Honduras": "340", "Hungary": "348", "Iceland": "352", "India": "356",
    "Indonesia": "360", "Iran": "364", "Iraq": "368", "Ireland": "372",
    "Israel": "376", "Italy": "380", "Jamaica": "388", "Japan": "392",
    "Jordan": "400", "Kazakhstan": "398", "Kenya": "404", "Kiribati": "296",
    "Korea, North": "408", "Korea, South": "410", "Kosovo": None, "Kuwait": "414",
    "Kyrgyzstan": "417", "Laos": "418", "Latvia": "428", "Lebanon": "422",
    "Lesotho": "426", "Liberia": "430", "Libya": "434", "Liechtenstein": "438",
    "Lithuania": "440", "Luxembourg": "442", "Madagascar": "450", "Malawi": "454",
    "Malaysia": "458", "Maldives": "462", "Mali": "466", "Malta": "470",
    "Marshall Islands": "584", "Mauritania": "478", "Mauritius": "480", "Mexico": "484",
    "Micronesia, Federated States": "583", "Moldova": "498", "Monaco": "492",
    "Mongolia": "496", "Montenegro": "499", "Morocco": "504", "Mozambique": "508",
    "Myanmar (Burma)": "104", "Namibia": "516", "Nauru": "520", "Nepal": "524",
    "Netherlands": "528", "New Zealand": "554", "Nicaragua": "558", "Niger": "562",
    "Nigeria": "566", "North Macedonia": "807", "Norway": "578", "Oman": "512",
    "Pakistan": "586", "Palau": "585", "Panama": "591", "Papua New Guinea": "598",
    "Paraguay": "600", "Peru": "604", "Philippines": "608", "Poland": "616",
    "Portugal": "620", "Qatar": "634", "Romania": "642", "Russia": "643",
    "Rwanda": "646", "Saint Kitts and Nevis": "659", "Saint Lucia": "662",
    "Samoa": "882", "San Marino": "674", "Sao Tome and Principe": "678",
    "Saudi Arabia": "682", "Senegal": "686", "Serbia": "688", "Seychelles": "690",
    "Sierra Leone": "694", "Singapore": "702", "Slovakia": "703", "Slovenia": "705",
    "Solomon Islands": "90", "Somalia": "706", "South Africa": "710",
    "South Sudan": "728", "Spain": "724", "Sri Lanka": "144",
    "St Vincent and Grenadines": "670", "Sudan": "729", "Suriname": "740",
    "Sweden": "752", "Switzerland": "756", "Syria": "760", "Taiwan": "158",
    "Tajikistan": "762", "Tanzania": "834", "Thailand": "764", "Timor-Leste": "626",
    "Togo": "768", "Tonga": "776", "Trinidad and Tobago": "780", "Tunisia": "788",
    "Turkiye (Turkey)": "792", "Turkmenistan": "795", "Tuvalu": "798",
    "Uganda": "800", "Ukraine": "804", "United Arab Emirates": "784",
    "United Kingdom": "826", "United States": "840", "Uruguay": "858",
    "Uzbekistan": "860", "Vanuatu": "548", "Venezuela": "862", "Vietnam": "704",
    "West Bank / Gaza": "275", "Yemen": "887", "Zambia": "894", "Zimbabwe": "716",
    "Vatican City": "336",
}

RELIGION_PT = {
    "Islam": "Islamismo",
    "Christianity": "Cristianismo",
    "Buddhism": "Budismo",
    "Hinduism": "Hinduísmo",
    "Judaism": "Judaísmo",
    "Non-Religious": "Não religioso / ateísmo",
    "Ethnic Religions": "Religiões étnicas/tradicionais",
}

# ---------------------------------------------------------------------------
# Ranking da Lista Mundial da Perseguição (LMP) 2026 - Portas Abertas
# (pesquisa 01/10/2024 a 30/09/2025; lançada 13/01/2026)
# Níveis aproximados: 1-15 Extrema; 16-42 Muito Alta; 43-50 Alta.
# ---------------------------------------------------------------------------
lmp_rank_pt = {
    "Coreia do Norte": 1, "Somália": 2, "Iêmen": 3, "Sudão": 4, "Eritreia": 5,
    "Síria": 6, "Nigéria": 7, "Paquistão": 8, "Líbia": 9, "Irã": 10,
    "Afeganistão": 11, "Índia": 12, "Arábia Saudita": 13, "Mianmar": 14,
    "Mali": 15, "Burkina Faso": 16, "China": 17, "Iraque": 18, "Maldivas": 19,
    "Argélia": 20, "Mauritânia": 21, "República Centro-Africana": 22,
    "Marrocos": 23, "Cuba": 24, "Uzbequistão": 25, "Níger": 26,
    "Tajiquistão": 27, "Laos": 28, "República Democrática do Congo": 29,
    "México": 30, "Tunísia": 31, "Nicarágua": 32, "Bangladesh": 33,
    "Butão": 34, "Turcomenistão": 35, "Etiópia": 36, "Camarões": 37,
    "Omã": 38, "Moçambique": 39, "Quirguistão": 40, "Turquia": 41,
    "Egito": 42, "Comores": 43, "Catar": 44, "Cazaquistão": 45, "Nepal": 46,
    "Colômbia": 47, "Chade": 48, "Jordânia": 49, "Brunei": 50,
}

def lmp_level(rank):
    if rank is None:
        return None
    if rank <= 15:
        return "Extrema"
    if rank <= 42:
        return "Muito Alta"
    return "Alta"

def parse_line(line):
    parts = [p.strip() for p in line.strip().split("|")]
    if len(parts) != 4:
        return None
    name_en, pop_str, primary_en, rest = parts
    # rest holds "evangelical | christian" but we already split on 4 pipes;
    # need to re-split since evangelical/christian were two more fields
    return None

countries = []
skipped = []
with open(RAW_FILE, encoding="utf-8") as f:
    for raw in f:
        raw = raw.strip()
        if not raw:
            continue
        cols = [c.strip() for c in raw.split("|")]
        if len(cols) != 5:
            skipped.append(raw)
            continue
        name_en, pop_str, primary_en, ev_str, ch_str = cols
        if name_en not in META:
            skipped.append(name_en)
            continue
        name_pt, region, sovereign = META[name_en]
        population = int(pop_str.replace(",", ""))
        ev = None if ev_str == "-1" else float(ev_str)
        ch = float(ch_str)
        other = round(100 - ch, 1)
        primary_pt = RELIGION_PT.get(primary_en, primary_en)
        rank = lmp_rank_pt.get(name_pt)
        countries.append({
            "name": name_pt,
            "nameEn": name_en,
            "isoNumeric": ISO_NUMERIC.get(name_en),
            "region": region,
            "isSovereignState": sovereign,
            "population": population,
            "pctEvangelical": ev,
            "pctChristianTotal": ch,
            "pctOtherReligions": other,
            "primaryReligion": primary_pt,
            "persecutionRank2026": rank,
            "persecutionLevel": lmp_level(rank),
        })

if skipped:
    print("AVISO - linhas/países não mapeados (ignorados):", skipped)

countries.sort(key=lambda c: (c["persecutionRank2026"] is None, c["persecutionRank2026"] or 999, c["name"]))

sovereign_count = sum(1 for c in countries if c["isSovereignState"])
territory_count = len(countries) - sovereign_count

output = {
    "meta": {
        "title": "Painel de Missões Mundiais",
        "countrySummary": f"{sovereign_count} países soberanos (193 Estados-membros da ONU + Vaticano + Palestina) e {territory_count} territórios/regiões administrativas adicionais de relevância missionária (ex.: Hong Kong, Macau, Taiwan, Kosovo).",
        "sources": [
            {
                "name": "Joshua Project - All Countries",
                "url": "https://joshuaproject.net/global/countries",
                "fields": ["population", "pctEvangelical", "pctChristianTotal", "primaryReligion"],
                "retrievedAt": "2026-09-21",
            },
            {
                "name": "Portas Abertas - Lista Mundial da Perseguição 2026",
                "url": "https://portasabertas.org.br/lista-mundial/paises-da-lista/",
                "fields": ["persecutionRank2026", "persecutionLevel"],
                "retrievedAt": "2026-09-21",
                "note": "Pesquisa realizada entre 01/10/2024 e 30/09/2025; lançada em 13/01/2026. Níveis (Extrema/Muito Alta/Alta) aproximados a partir das faixas de colocação divulgadas; para o detalhamento oficial de pontuação por país, consulte o site da Portas Abertas.",
            },
        ],
        "generatedAt": datetime.datetime.utcnow().isoformat() + "Z",
        "howToUpdate": "Edite este arquivo (ou data/countries.json diretamente) sempre que houver nova pesquisa do Joshua Project ou nova edição da Lista Mundial da Perseguição (geralmente lançada em janeiro).",
    },
    "countries": countries,
}

with open("../data/countries.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Gerados {len(countries)} países/territórios em data/countries.json "
      f"({sovereign_count} soberanos + {territory_count} territórios)")
