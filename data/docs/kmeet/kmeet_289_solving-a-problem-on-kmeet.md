# Solving a problem on kMeet

Source: https://www.infomaniak.com/en/support/faq/289/solving-a-problem-on-kmeet

---

This guide explains how to resolve any potential issues during a meeting with kMeet, the secure, unlimited, and free videoconferencing solution from Infomaniak.

> **Note:** For a **video** issue, refer to [this other guide](https://www.infomaniak.com/en/support/faq/2452); for **audio**, [this other guide](https://www.infomaniak.com/en/support/faq/2441).

## Unable to see or hear the correspondent

If the conference is started, your correspondent has turned on the **webcam** and their **microphone**, but you still cannot see/hear them, ask them to check for the presence of a potential **firewall** on their machine or corporate network.

A **firewall** may allow solutions like Google Meet or Microsoft Teams without necessarily allowing kMeet streams.

In your firewall settings, here is what you need to allow:

- UDP Protocol: `443`.
- For the *turn server* (recommended), add the TCP port `443`.
- Allow the following IP addresses:185.125.24.0/24 (TCP)185.125.24.0/24 (UDP)

You can also switch connections (from WiFi to 4G/5G, for example) to check if a firewall is causing the desynchronizations.

## Screen sharing impossible

When using the kMeet videoconferencing solution, if the button to [share your screen](https://www.infomaniak.com/en/support/faq/2477) is not available and/or remains grayed out, check the **security settings** on your computer/operating system regarding...

- ... the **kMeet** application
- ... the browser (if you are using **kMeet** directly online without going through the application):

For example, on **macOS**, check and then activate the required permissions:

1. Go to **System Settings** under **Privacy and Security** then **Screen Recording**:

2. Add your **browser** if necessary, or even **kMeet** if you have the desktop app on your computer:

3. Then also take note of the icons present in your browser's address bar and detect any potential authorization issues by clicking on the symbols:
