document.addEventListener("DOMContentLoaded", () => {
    const chatbotToggleButton = document.getElementById("chatbot-toggle-btn");
    const chatbotContainer = document.getElementById("chatbot-container");
    const maximizeBtn = document.getElementById("chatbot-maximize-btn");

    // --- LOGIKA BUKA TUTUP CHATBOT ---
    chatbotToggleButton.addEventListener("click", () => {
        chatbotContainer.classList.toggle("show");
        chatbotToggleButton.classList.toggle("active");
    });

    // --- LOGIKA MAXIMIZE / RESTORE ---
    maximizeBtn.addEventListener("click", () => {
        chatbotContainer.classList.toggle("maximized");
    });

    // Semua logika untuk drag dan resize telah dihapus.
});