self.addEventListener("push", function (event) {
    let data = {};

    if (event.data) {
        data = event.data.json();
    }

    const title = data.title || "Inkspire";
    const options = {
        body: data.body || "A new story has been published. Read it now!",
        icon: "/static/images/icon.png",
        data: {
            url: data.url || "/"
        }
    };

    event.waitUntil(
        self.registration.showNotification(title, options)
    );
});

self.addEventListener("notificationclick", function (event) {
    event.notification.close();

    event.waitUntil(
        clients.openWindow(event.notification.data.url || "/")
    );
});