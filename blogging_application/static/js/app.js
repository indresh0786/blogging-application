document.addEventListener
    ("DOMContentLoaded",
        () => {
            document.querySelectorAll
            (".delete-form").
            forEach
            (f => f.addEventListener("submit", e => {
                if (!confirm("Delete this story permanently?"))
                    e.preventDefault()
            }));
            setTimeout(() => document.querySelectorAll(".message").
                forEach(x => x.remove()), 4000);
        });
function urlBase64ToUint8Array(base64String) {
    const padding = "=".repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
        .replace(/-/g, "+")
        .replace(/_/g, "/");

    const rawData = window.atob(base64);
    return Uint8Array.from([...rawData].map(char => char.charCodeAt(0)));
}

async function subscribeForNotifications() {
    if (!("serviceWorker" in navigator) || !("PushManager" in window)) {
        alert("Push notifications are not supported in this browser.");
        return;
    }

    const permission = await Notification.requestPermission();

    if (permission !== "granted") {
        alert("Notification permission was not allowed.");
        return;
    }

    const registration = await navigator.serviceWorker.register("/static/js/sw.js");

    const keyResponse = await fetch("/push/public-key/");
    const keyData = await keyResponse.json();

    const subscription = await registration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: urlBase64ToUint8Array(keyData.publicKey)
    });

    const response = await fetch("/push/subscribe/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(subscription)
    });

    if (response.ok) {
        alert("Notifications enabled successfully 🔔");
    } else {
        alert("Could not enable notifications.");
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const notifyButton = document.getElementById("notify-btn");

    if (notifyButton) {
        notifyButton.addEventListener("click", subscribeForNotifications);
    }
});