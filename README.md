# 🛡️ AFK Guardian

<div align="center">

![AFK Guardian](https://img.shields.io/badge/AFK-Guardian-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-19.0-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Flask](https://img.shields.io/badge/Flask-3.1.2-000000?style=for-the-badge&logo=flask&logoColor=white)

**An intelligent, multi-modal employee activity monitoring system that tracks productivity in real-time**

[Features](#-features) • [Tech Stack](#-tech-stack) • [Installation](#-installation) • [Usage](#-usage) • [Architecture](#-architecture)

</div>

---

## 🌟 Overview

**AFK Guardian** is a comprehensive employee monitoring solution built for modern workplaces. It combines multiple tracking technologies to provide accurate insights into employee activity, productivity patterns, and work habits. The system uses computer vision, audio analysis, and input monitoring to detect when employees are actively working, away from their desks, or taking breaks.

### 🎯 Why AFK Guardian?

- **Multi-Modal Tracking**: Combines eye tracking, voice detection, keyboard/mouse activity, and window monitoring
- **Real-Time Insights**: Live dashboard with instant updates on employee status
- **Privacy-Focused**: Monitors activity patterns without recording screen content or keystrokes
- **Easy Integration**: Simple setup with REST API for seamless integration
- **Beautiful UI**: Modern, responsive dashboard built with React and Tailwind CSS

---

## ✨ Features

### 🔍 **Advanced Monitoring Capabilities**

- **👁️ Eye Tracking**: Detects user presence and attention using computer vision (MediaPipe)
- **🎤 Voice Detection**: Identifies when employees are in meetings or calls
- **⌨️ Activity Tracking**: Monitors keyboard and mouse interactions
- **🪟 Window Monitoring**: Tracks active applications and time spent on each
- **📊 Smart Analytics**: Automatic AFK detection with configurable thresholds

### 📈 **Dashboard Features**

- Real-time employee status monitoring
- Individual employee detail pages
- Activity timeline visualization
- Time tracking across different applications
- Speaking status indicators
- Beautiful, responsive UI with Tailwind CSS

### 🔧 **Technical Highlights**

- RESTful API for data management
- JSON-based data persistence
- Cross-platform Windows support
- Configurable monitoring intervals
- Modular architecture for easy extension

---

## 🛠️ Tech Stack

### **Backend**
- **Python 3.8+**: Core monitoring logic
- **Flask 3.1.2**: REST API server
- **OpenCV 4.13**: Computer vision processing
- **MediaPipe 0.10**: Eye and pose tracking
- **PyAutoGUI**: Activity monitoring
- **SoundDevice**: Audio/voice detection

### **Frontend**
- **React 19.0**: UI framework
- **Vite**: Build tool and dev server
- **Tailwind CSS 4.0**: Styling
- **Axios**: HTTP client
- **Recharts**: Data visualization
- **React Router**: Navigation
- **React Icons**: Icon library

### **Infrastructure**
- **Flask-CORS**: Cross-origin support
- **Vercel**: Frontend deployment
- **Render**: Backend hosting

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- Node.js 16+ and npm
- Windows OS (for PyWin32 and window tracking)
- Webcam (for eye tracking)
- Microphone (for voice detection)

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/Hackaway_AFK_Guardian.git
cd Hackaway_AFK_Guardian
```

### 2️⃣ Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Navigate to server directory
cd server

# Run the Flask server
python server.py
```

The server will start on `http://localhost:5000`

### 3️⃣ Client Setup

```bash
# Navigate to clients directory
cd clients

# Run the monitoring client
python main.py
```

### 4️⃣ Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

---

## 🚀 Usage

### Starting the System

1. **Start the Backend Server**
   ```bash
   cd server
   python server.py
   ```

2. **Launch the Monitoring Client**
   ```bash
   cd clients
   python main.py
   ```
   - The client will start tracking activity automatically
   - Default Employee ID: 1 (configurable in `main.py`)
   - AFK threshold: 5 minutes (300 seconds)

3. **Open the Dashboard**
   ```bash
   cd frontend
   npm run dev
   ```
   - Navigate to `http://localhost:5173` in your browser
   - View real-time employee activity and statistics

### Configuration

**Modify AFK Threshold**: Edit `clients/main.py`
```python
AFK_THRESHOLD = 300  # seconds (default: 5 minutes)
CHECK_INTERVAL = 1    # check frequency (default: 1 second)
```

**Change Employee ID**: Update in `clients/main.py`
```python
EMPLOYEE_ID = 1  # Set your employee ID
```

---

## 🏗️ Architecture

```
┌─────────────────┐
│  React Frontend │  ← User Dashboard
│   (Port 5173)   │
└────────┬────────┘
         │ HTTP/REST API
         ▼
┌─────────────────┐
│  Flask Server   │  ← Data Management
│   (Port 5000)   │
└────────┬────────┘
         │ JSON Storage
         ▼
┌─────────────────┐
│ employee_data   │  ← Persistent Storage
│     .json       │
└─────────────────┘
         ▲
         │ POST Updates
┌────────┴────────┐
│ Monitoring      │  ← Activity Tracking
│ Client          │
│  - Eye Tracker  │
│  - Voice        │
│  - Activity     │
│  - Window       │
└─────────────────┘
```

### Project Structure

```
Hackaway_AFK_Guardian/
├── clients/                    # Monitoring client
│   ├── main.py                # Main tracking logic
│   └── afk_checks/            # Tracking modules
│       ├── activity_tracker.py    # Keyboard/mouse
│       ├── eye_tracker.py         # Eye tracking
│       ├── pose_tracker.py        # Pose detection
│       ├── voice_tracker.py       # Voice detection
│       └── window_tracker.py      # Active window
│
├── server/                    # Backend API
│   ├── server.py             # Flask application
│   ├── employee_data.json    # Data storage
│   └── requirements.txt      # Python dependencies
│
├── frontend/                  # React dashboard
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── Home.jsx
│   │   │   ├── EmployeeDetail.jsx
│   │   │   └── Navbar.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
└── requirements.txt          # Root dependencies
```

---

## 🌐 API Endpoints

### `GET /employee/<employee_id>`
Get activity data for a specific employee

**Response:**
```json
{
  "status": "success",
  "data": {
    "time_spent": 3600,
    "activities": {
      "eye_movement": {"count": 1200, "text": "Active"},
      "speaking": {"count": 45, "text": "In Meeting"}
    }
  }
}
```

### `POST /employee/<employee_id>`
Update employee activity data

**Request Body:**
```json
{
  "time_spent": 3600,
  "activities": {
    "eye_movement": {"count": 1200, "text": "Active"}
  }
}
```

---

## 🎨 Screenshots

### Dashboard Overview
View all employees at a glance with real-time status indicators

### Employee Details
Detailed activity breakdown with charts and timelines

### Activity Timeline
Visual representation of work patterns throughout the day

---

## 🔒 Privacy & Ethics

AFK Guardian is designed with privacy in mind:

- ✅ **No Screen Recording**: Only tracks activity patterns, not content
- ✅ **No Keystroke Logging**: Monitors activity frequency, not actual keys pressed
- ✅ **Local Processing**: Eye and voice data processed locally, not stored
- ✅ **Transparent**: Employees can see what data is collected
- ✅ **Configurable**: Admins can adjust sensitivity and thresholds

**Important**: Always inform employees about monitoring and obtain proper consent. Use responsibly and in compliance with local labor laws.

---

## 🚧 Future Enhancements

- [ ] Multi-user authentication system
- [ ] PostgreSQL/MongoDB integration
- [ ] Productivity insights and AI recommendations
- [ ] Mobile app for managers
- [ ] Slack/Teams integration
- [ ] Custom alert notifications
- [ ] Export reports to PDF/Excel
- [ ] Multi-platform support (macOS, Linux)
- [ ] Docker containerization
- [ ] Advanced analytics dashboard

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👥 Team

Built with ❤️ during Hackaway Hackathon

---

## 📧 Contact

For questions, suggestions, or support, please open an issue on GitHub.

---

<div align="center">

**⭐ Star this repo if you find it useful!**

Made with 🔥 by the AFK Guardian Team

</div>
