const API_BASE = "http://127.0.0.1:5000/api";

const commodities = [
    { en: "Tomato", kn: "ಟೊಮೇಟೋ", hi: "टमाटर", value: "tomato" },
    { en: "Onion", kn: "ಈರುಳ್ಳಿ", hi: "प्याज़", value: "onion" },
    { en: "Potato", kn: "ಆಲೂಗಡ್ಡೆ", hi: "आलू", value: "potato" },
    { en: "Chilli", kn: "ಮೆಣಸಿನಕಾಯಿ", hi: "मिर्च", value: "chilli" },
    { en: "Groundnut", kn: "ಕಡಲೆಕಾಯಿ", hi: "मूंगफली", value: "groundnut" }
    // 👉 add all 50+ commodities here
];

let currentLang = "en";

const labels = {
    en: "Search commodity...",
    kn: "ಬೆಳೆ ಹುಡುಕಿ...",
    hi: "फसल खोजें..."
};

function setLang(lang) {
    currentLang = lang;
    document.getElementById("searchInput").placeholder = labels[lang];
}

function filterCommodities() {
    const query = document.getElementById("searchInput").value.toLowerCase();
    const box = document.getElementById("suggestions");
    box.innerHTML = "";

    if (!query) return;

    commodities
        .filter(c => c[currentLang].toLowerCase().includes(query))
        .forEach(c => {
            const div = document.createElement("div");
            div.className = "suggestion";
            div.innerText = c[currentLang];
            div.onclick = () => fetchAdvisory(c.value, c[currentLang]);
            box.appendChild(div);
        });
}

function fetchAdvisory(value, displayName) {
    document.getElementById("suggestions").innerHTML = "";
    document.getElementById("searchInput").value = displayName;

    fetch(`${API_BASE}/advisory/${value}`)
        .then(res => res.json())
        .then(data => {
            document.getElementById("result").innerHTML = `
        <div class="card">
          <h2>${data.emoji} ${displayName} (${data.state})</h2>
          <p><b>Today Price:</b> ₹${data.today_price}</p>
          <p><b>Recommendation:</b>
            <span class="badge ${data.recommendation}">
              ${data.recommendation}
            </span>
          </p>
          <p><b>Duration:</b> ${data.store_days} days</p>
          <p><b>Expected Price:</b> ₹${data.expected_price}</p>
          <p><b>Price Range:</b> ₹${data.price_range_low} – ₹${data.price_range_high}</p>
          <p><b>Extra Profit:</b> ₹${data.extra_profit}</p>
          <p><b>Confidence:</b> ${data.confidence}</p>
        </div>
      `;
        });
}
