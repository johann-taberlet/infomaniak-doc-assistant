# Solving a problem on k Meet

Source: https://www.infomaniak.com/en/support/faq/289/solving-a-problem-on-kmeet

---

This guide explains how to resolve any potential issues during a meeting with [k Meet](https://infomaniak.com/gtl/meet), the secure, unlimited, and free videoconferencing solution from Infomaniak.

> **Note:** For a **video** issue, refer to [this other guide](https://www.infomaniak.com/en/support/faq/2452); for **audio**, [this other guide](https://www.infomaniak.com/en/support/faq/2441).

## Unable to see or hear the correspondent

If the conference is started, your correspondent has turned on the **webcam** and their **microphone**, but you still cannot see/hear them, ask them to check for the presence of a potential **firewall** on their machine or corporate network.

A **firewall** may allow solutions like Google Meet or Microsoft Teams without necessarily allowing k Meet streams.

In your firewall settings, here is what you need to allow:

- UDP Protocol: `443`.
- For the *turn server* (recommended), add the TCP port `443`.
- Allow the following IP addresses:185.125.24.0/24 (TCP)185.125.24.0/24 (UDP)

You can also switch connections (from Wi Fi to 4G/5G, for example) to check if a firewall is causing the desynchronizations.

## Screen sharing impossible

When using the k Meet videoconferencing solution, if the button to [share your screen](https://www.infomaniak.com/en/support/faq/2477) is not available and/or remains grayed out, check the **security settings** on your computer/operating system regarding…

- … the **k Meet** application
- … the browser (if you are using **k Meet** directly online without going through the application):

For example, on **macOS**, check and then activate the required permissions:

1. Go to **System Settings** under **Privacy and Security** then **Screen Recording**:

![image](https://faq.storage5.infomaniak.com/cd2a82ecc51847e2a1f06e844fad4d9bf26396b5.png)

2. Add your **browser** if necessary, or even **k Meet** if you have the desktop app on your computer:

![image](https://faq.storage5.infomaniak.com/6f95776ca53da45b862cee77a0b2c91a8348a4e1.png)

3. Then also take note of the icons present in your browser's address bar and detect any potential authorization issues by clicking on the symbols:

![image](https://faq.storage5.infomaniak.com/0bd6c32f1098d8b8d26f14c61555b9bb0a7eae11.png)