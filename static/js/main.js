// main.js — students will add JavaScript here as features are built

// ------------------------------------------------------------------ //
// "See how it works" video modal (landing page)                       //
// ------------------------------------------------------------------ //

(function () {
    const modal = document.getElementById("video-modal");
    const openBtn = document.querySelector("[data-video-open]");
    if (!modal || !openBtn) return;

    const iframe = modal.querySelector("iframe");
    const closeBtn = modal.querySelector("[data-video-close]");

    openBtn.addEventListener("click", function (event) {
        event.preventDefault();
        // Load the video only when the modal opens, and start it playing.
        iframe.src = iframe.dataset.src + "?autoplay=1&rel=0";
        modal.showModal();
    });

    closeBtn.addEventListener("click", function () {
        modal.close();
    });

    // Clicks on the backdrop land on the <dialog> itself, not its children.
    modal.addEventListener("click", function (event) {
        if (event.target === modal) modal.close();
    });

    // Fires for every way of closing (button, backdrop, Escape key).
    // Unloading the iframe is what guarantees the video stops.
    modal.addEventListener("close", function () {
        iframe.src = "about:blank";
        openBtn.focus();
    });
})();
