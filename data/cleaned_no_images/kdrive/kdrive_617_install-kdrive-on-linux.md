# Install k Drive on Linux

Source: https://www.infomaniak.com/en/support/faq/617/install-kdrive-on-linux

---

This guide details the installation of the desktop app [k Drive](https://infomaniak.com/gtl/kdrive) Infomaniak on a computer with a **Linux** operating system. It will then allow you to synchronize your files with k Drive.

### Preamble

- On this OS, some k Drive features are not available, such as the **Lite Sync** option or the **right-click context menu**.
- The k Drive app is **officially supported** by Infomaniak only on the following systems: Ubuntu 22.04 LTS (and later)Desktop environments: GNOME or KDE
- The application may work on other Linux distributions or with other desktop environments; however, **Infomaniak provides no support for installing or running the application outside of the configurations mentioned above**.

## Installing k Drive on Linux

### Prerequisites

- [Download](https://infomaniak.com/gtl/apps.kdrive) the desktop app **k Drive** for Linux*(file of type . App Image)*
- Fuse2 (*required to run aappimage*): Since version 23.04 (and later) of Ubuntu, after double-clicking on the App Image file, nothing will happen. The latest versions of Ubuntu use a "too" recent version of FUSE (the "Filesystem in User Space" interface on which App Images rely to work) for which App Images are not designed. App Images need FUSE v2 to work: sudo apt install libfuse2
- D-Bus
- Gnome-keyring or kwallet(*in principle already present on your machine except with some light distributions)*

Then:

1. Place the file in a folder named for example "**Applications**".
2. Right-click on the file and select **Permissions**.
3. Check the box "**Allow executing file as a program**"

### Additional possible operations

With **Ubuntu**, to have k Drive run at startup, add the file in “*Startup Application Preferences*”

With **Gnome**, if the icon is missing, install [App Indicator](https://extensions.gnome.org/extension/615/appindicator-support/).