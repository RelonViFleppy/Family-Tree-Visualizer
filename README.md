# 🌳 Interactive Family Tree Visualizer (Tkinter & JSON)

This project is a desktop application developed in **Python** and **Tkinter**, designed to parse family data from a **JSON** file and visualize it in an interactive, navigable tree structure.

## 🛠️ Engineering Highlights
* **Dynamic Tree Rendering:** Built a sophisticated visualization engine within `map.py` that dynamically draws nodes (family members) and connects them with relationship lines based on parent/child relationships defined in JSON.
* **Modular Software Architecture:** Strict separation of concerns between data models (`character.py`), rendering logic (`map.py`), state management (`manager.py`), and the main GUI (`main_app.py`) for high maintainability.
* **Interactive UI:** Implemented navigation features, allowing users to scroll and zoom (isteğe bağlı, koda bağlı) through large family trees. Each character node is interactive, showing profile pictures (using `default_avatar.png`) and basic info.
* **Asset Integration:** Managed custom image assets and dynamic JSON parsing to ensure flexible data updates without code modification.

## 🧠 Key Challenges Solved
1. **Asynchronous Image Loading:** Solved a critical Tkinter garbage collection issue (within `character.py`), ensuring profile pictures are persisted and rendered correctly within the canvas.
2. **Flexible Positioning:** Developed a scalable grid-based positioning logic that adapts to different family sizes and tree depths.

## 🚀 Technologies Used
* **Python:** Core language.
* **Tkinter:** GUI and canvas-based visualization.
* **JSON:** Custom data persistence layer.
* **Pillow (PIL):** Advanced image processing for character avatars.

---
*Developed by Enes Malik Dincer as a demonstration of real-time data visualization and GUI engineering.*
