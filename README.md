# mFRR Profit Estimator

**Special thanks to PhD. Mario Kadastik, whose code I used, and the reason I made this was just to have a web interface.** 🎉


## Project Overview
mFRR Profit Estimator is a web application for estimating potential earnings from participating in the manual Frequency Restoration Reserve (mFRR) energy market.  Upload a CSV export from Qilowatt mFRR report and analyze the results directly in this web app.

---

## Installation Instructions

### **Option 1: APT Installation**  
On Debian/Ubuntu systems, install the mFRR Profit Estimator using APT:  
```sh
sudo apt update && sudo apt install -y python3-flask python3-pandas python3-numpy
```

### **Option 2: Virtual Environment (Alternative)**  
Alternatively, install the app in an isolated Python virtual environment:  
```sh
sudo apt install -y python3-venv
python3 -m venv venv
source venv/bin/activate
pip install flask pandas numpy
```

---

## Running as a systemd Service
To run the app continuously in the background, set it up as a **systemd service**:

1. **Create the service file**:
   ```sh
   sudo nano /etc/systemd/system/flask-app.service
   ```
2. **Paste this content** (update paths if needed):
   ```ini
   [Unit]
   Description=Flask mFRR Profit Estimator
   After=network.target

   [Service]
   WorkingDirectory=/opt/flask-app
   ExecStart=/usr/bin/python3 /opt/flask-app/app.py
   Restart=always
   User=root

   [Install]
   WantedBy=multi-user.target
   ```
3. **Enable and start the service**:
   ```sh
   sudo systemctl daemon-reload
   sudo systemctl enable --now flask-app
   ```

4. **Check the service status** (optional):
   ```sh
   sudo systemctl status flask-app
   ```
   If running correctly, it should show **"active (running)"**.

---

## Accessing the Web App

1. **Find the container’s IP**:
   ```sh
   ip a
   ```
2. **Open the interface in a browser**:
   ```
   http://[container-IP]:5000/
   ```

---

## License

This project is licensed under the **MIT License**.

---
