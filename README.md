
![Bildschirmfoto 2025-04-13 um 01 08 20](https://github.com/user-attachments/assets/aa234b06-2e85-4351-92ff-cb46f264caeb)
![Bildschirmfoto 2025-04-13 um 01 08 42](https://github.com/user-attachments/assets/df3ff410-4f0b-486a-b7b2-36892d73d643)


# 💬 LANChat – Local Communication for LAN Parties

**LANChat** is a simple, browser-based chat and file-sharing system built using **Python Flask**. Designed for **LAN parties**, small gatherings, or offline events, it runs entirely within your local network – **no internet or external server required**.

Perfect for coordinating during game sessions or just chatting during the event!

---

### 🔧 Features

- 💡 **No Installation Required:** Just run the Python server and access it via browser.
- 🌐 **Locally Hosted:** Runs entirely in your LAN – no outside connections.
- 📁 **File Sharing:** Upload and download files (e.g. screenshots, configs, memes).
- 🎨 **Simple UI:** Built with Bootstrap for a clean and responsive interface.
- 🧠 **Name Memory:** Usernames are stored in cookies for a seamless experience.

---

### 📦 Use Case

Created for **LAN parties** or events where multiple users are connected to the same local network. LANChat offers a fast and distraction-free way to communicate without switching apps or relying on the internet.

---

### 🖥️ Tech Stack

- 🐍 **Backend:** Python 3 with Flask
- 💾 **Data Storage:** In-memory message list + JSON log file (`chat_log.json`)
- 🖼️ **Frontend:** HTML + Bootstrap 5 + JavaScript
- 📂 **Uploads:** File storage in local `uploads/` folder
- 🔒 **Privacy-Friendly:** All data stays in your local network

---

### 🚀 Getting Started

1. **Download the server.exe from the Downloads Folder**
2. **allow fierwall rules**
3. **Open your browser and go to**  
   `http://<your-local-ip>:5000`  
   (e.g., `http://192.168.0.100:5000`)

4. **Enter your name and start chatting & uploading!**

---

### 📂 File Uploads

- Uploaded files are stored in the `/uploads` folder.
- Download links are automatically embedded in the chat.
- Files are timestamped and safely named to avoid conflicts.

---

### ⚠️ Notes

- Messages are saved in `chat_log.json` – auto-loaded on restart.
- File uploads are not limited by type or size – adjust Flask config if needed.
- This is a lightweight local tool – not designed for public deployment.
