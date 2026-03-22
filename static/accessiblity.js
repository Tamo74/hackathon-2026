function toggleSection(id) {
    const section = document.getElementById(id);
    section.style.display = section.style.display === "block" ? "none" : "block";
}

async function saveAccessibility() {
    const payload = {
        text_size: parseInt(document.getElementById("textSize").value),
        icon_size: parseInt(document.getElementById("iconSize").value),
        tts: document.getElementById("tts").checked,
        autoscroll: document.getElementById("autoscroll").checked,
        dark_mode: document.getElementById("darkMode").checked,
        colour_filter: document.getElementById("colourFilter").value,
        language: document.getElementById("language").value
    };

    await fetch("/settings/accessibility/update", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    alert("Accessibility settings saved");
}
