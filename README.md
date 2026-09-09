# 🕯️ Stranded: Hell's Maw

**Stranded: Hell's Maw** is a tense, text-based survival horror adventure written in Python. You are stranded on a cursed island after a horrific plane crash. Your objective is simple but deadly: find the scattered items needed to build a raft, rescue your brother Edwin, and escape before dawn breaks—or before the island's demonic resident finds you.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Rich](https://img.shields.io/badge/rich-%23323330.svg?style=for-the-badge&logo=terminal&logoColor=white)

## ✨ Features

- **Object-Oriented Design:** Clean and modular architecture divided into specific logic modules (`player.py`, `world.py`, `demon.py`, `game.py`).
- **Beautiful Console UI:** Powered by the `rich` library for an immersive, colorized, and stylized terminal experience.
- **Meaningful Characters:** Play as **Jonathan** (+3 Hours stamina) or **Daniella** (Higher chance to find items).
- **Dynamic Events & Demon Footprints:** Explore a physically connected map. Empty rooms hide random events, and you'll hear the demon's heavy footsteps when it prowls nearby.
- **Persistent Saving:** Quit and resume your nightmare at any time safely with JSON serialization.

## 🛠 Tech Stack

- **Python 3:** Core application logic and object-oriented structure.
- **Rich:** Module for immersive terminal formatting and colorized output.
- **JSON:** Persistent saving and state management.

## 🚀 Getting Started

If you want to play **Stranded: Hell's Maw** locally on your machine, follow these steps:

### Prerequisites
Make sure you have [Python 3](https://www.python.org/downloads/) installed on your machine.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/hells-maw.git
   cd hells-maw
   ```

2. **Install the dependencies:**
   The game requires the `rich` library for its UI.
   ```bash
   pip install rich
   ```

3. **Run the Game:**
   ```bash
   python Code.py
   ```

## 🎯 How to Play

You have a limited number of hours (turns) before dawn breaks, determined by your chosen difficulty level. Moving to a new location costs 1 hour.

- **Search:** Choose a location to search for essential items (Map, Compass, Raft, Oars, Torch).
- **Brother Rescue:** You must find the **Map** and **Torch** before your brother Edwin can be located.
- **Escape:** Once you have all items and have found Edwin, return to the **Bay** and type **SET SAIL**.
- **Avoid the Demon:** After a brief grace period, a demon will begin hunting you. Listen for footprint warnings. If you enter the same location as the demon, it's instant death.

## 📖 About

**Stranded: Hell's Maw** was created to explore text-based narrative mechanics, time management, and atmosphere through clean Python modularity. It challenges players to balance the urgency of an expiring clock against the creeping dread of an unseen hunter. Dare to step into the shadows and see if you have what it takes to survive.
