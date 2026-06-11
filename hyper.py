import sys
print("--> Python script has successfully initialized execution.", flush=True)

import os
import subprocess
import platform
import shutil
import urllib.parse
import urllib.request
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

# --- CONFIGURATION & VERSION CONTROL ---
ONLINE_FILE_URL = "https://srayanayt.github.io/hyperproxysite/hyper.py"
PORT = 8080

# --- PATH SETUP ---
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
os.chdir(BASE_DIR)
PROFILES_DIR = os.path.join(BASE_DIR, "profiles")
MENU_DATA_DIR = os.path.join(BASE_DIR, "menu_state")
PNG_ICON_PATH = os.path.join(BASE_DIR, "favicon.png")

if not os.path.exists(PROFILES_DIR):
    os.makedirs(PROFILES_DIR)

if not os.listdir(PROFILES_DIR):
    os.makedirs(os.path.join(PROFILES_DIR, "Default"))

def get_edge_path():
    system = platform.system()
    if system == "Windows":
        paths = [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                 r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"]
        return next((p for p in paths if os.path.exists(p)), None)
    return "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" if system == "Darwin" else None

def check_is_latest_version():
    import ssl
    try:
        local_file_path = os.path.realpath(__file__)
        with open(local_file_path, 'r', encoding='utf-8') as f:
            local_code = f.read()

        context = ssl._create_unverified_context()
        https_handler = urllib.request.HTTPSHandler(context=context)
        proxy_handler = urllib.request.ProxyHandler({})
        opener = urllib.request.build_opener(proxy_handler, https_handler)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Cache-Control': 'no-cache, no-store, must-revalidate, max-age=0',
            'Pragma': 'no-cache',
            'Expires': '0'
        }
        
        cache_buster_url = f"{ONLINE_FILE_URL}?t={int(time.time())}"
        req = urllib.request.Request(cache_buster_url, headers=headers)
        
        with opener.open(req, timeout=5) as response:
            online_code = response.read().decode('utf-8')
            
        local_clean = local_code.replace('\r\n', '\n').strip()
        online_clean = online_code.replace('\r\n', '\n').strip()

        local_lines = [line for line in local_clean.splitlines() if "ONLINE_FILE_URL =" not in line]
        online_lines = [line for line in online_clean.splitlines() if "ONLINE_FILE_URL =" not in line]

        if local_lines == online_lines:
            return True
        return False
    except Exception:
        return False

# --- UI TEMPLATE (Your Original Glassmorphism Layout Unaltered) ---
def get_html(show_update_prompt=False):
    profiles = sorted([d for d in os.listdir(PROFILES_DIR) if os.path.isdir(os.path.join(PROFILES_DIR, d))])
    profile_html = ""
    for p in profiles:
        profile_html += f'''
        <div class="profile-card">
            <span class="profile-name">{p}</span>
            <div class="action-row">
                <a href="/launch?name={p}" class="btn btn-launch">Launch Session</a>
                <a href="/delete?name={p}" class="btn btn-delete" onclick="return confirm('Delete all data?')">
                    <svg viewBox="0 0 24 24"><path d="M3 6v18h18v-18h-18zm5 14c0 .552-.448 1-1 1s-1-.448-1-1v-10c0-.552.448-1 1-1s1 .448 1 1v10zm5 0c0 .552-.448 1-1 1s-1-.448-1-1v-10c0-.552.448-1 1-1s1 .448 1 1v10zm5 0c0 .552-.448 1-1 1s-1-.448-1-1v-10c0-.552.448-1 1-1s1 .448 1 1v10zm4-18v2h-20v-2h5.711c.9 0 1.631-1.099 1.631-2h5.315c0 .901.73 2 1.631 2h5.712z"/></svg>
                </a>
            </div>
        </div>'''
    
    alert_script = '<script>alert("Outdated Build! Your file does not match the server master code. Please pull down the update.");</script>' if show_update_prompt else ''
    
    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
    <title>Edge Session Manager</title>
    <link rel="icon" href="/favicon.png" type="image/png">
    <style>
        body {{ margin: 0; min-height: 100vh; display: flex; flex-direction: column; align-items: center; font-family: "Segoe UI", sans-serif; color: white; padding: 40px 20px;
               background: radial-gradient(circle at 20% 20%, #ff6b6b55, transparent 40%), radial-gradient(circle at 80% 30%, #4dabf755, transparent 45%), radial-gradient(circle at 40% 80%, #51cf6655, transparent 50%), linear-gradient(135deg, #0f172a, #1e293b 40%, #0b1220); }}
        .main-container {{ width: 100%; max-width: 1000px; }}
        .header-panel {{ display: flex; justify-content: space-between; align-items: center; padding: 25px; margin-bottom: 30px; border-radius: 24px; background: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0OCIgaGVpZ2h0PSI0OCI+PGRlZnM+PGZpbHRlciBpZD0ibm9pc2UiPjxmZVR1cmJ1bGVuY2UgdHlwZT0idHVyYnVsZW5jZSIgYmFzZUZyZXF1ZW5jeT0iMi4yIiBzZWVkPSIyIi8+PC9maWx0ZXI+PC9kZWZzPjxyZWN0IHdpZHRoPSI0OCIgaGVpZ2h0PSI0OCIgZmlsdGVyPSJ1cmwoI25vaXNlKSIgb3BhY2l0eT0iMC40NSIvPjwvc3ZnPg=="), rgba(255,255,255,0.06); backdrop-filter: blur(16px); border: 1px solid rgba(255,255,255,0.16); box-shadow: 0 15px 35px rgba(0,0,0,0.3); }}
        .profile-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 20px; }}
        .profile-card {{ padding: 20px; border-radius: 24px; background: rgba(255,255,255,0.04); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.1); display: flex; flex-direction: column; transition: 0.3s; }}
        .profile-card:hover {{ transform: translateY(-5px); border-color: rgba(255,255,255,0.2); }}
        .profile-name {{ font-size: 1.1rem; font-weight: 600; color: #7cc7ff; margin-bottom: 18px; }}
        .action-row {{ display: flex; gap: 10px; width: 100%; }}
        .btn {{ display: flex; align-items: center; justify-content: center; border-radius: 14px; border: 1px solid rgba(255,255,255,0.18); background: rgba(255,255,255,0.08); color: white; font-weight: 600; cursor: pointer; text-decoration: none; transition: 0.2s; }}
        .btn:active {{ transform: scale(0.95); }}
        .btn-new {{ padding: 10px 20px; background: rgba(81, 207, 102, 0.25); border-color: rgba(81, 207, 102, 0.4); }}
        .btn-launch {{ flex-grow: 1; padding: 12px; background: rgba(124, 199, 255, 0.15); }}
        .btn-delete {{ width: 45px; height: 45px; flex-shrink: 0; background: rgba(255, 107, 107, 0.1); border-color: rgba(255, 107, 107, 0.3); }}
        .btn-delete svg {{ width: 18px; height: 18px; fill: #ff6b6b; }}
    </style>
    </head><body>
    <div class="main-container">
        <div class="header-panel"><h2>Edge Session Manager</h2><button class="btn btn-new" onclick="createAccount()">+ New Account</button></div>
        <div class="profile-grid">{profile_html}</div>
    </div>
    {alert_script}
    <script>
        function createAccount() {{
            let name = prompt("Account Name:");
            if (name) window.location.href = "/create?name=" + encodeURIComponent(name);
        }}
    </script></body></html>'''

# --- SERVER LOGIC ---
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed_path.query)
        
        if parsed_path.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(get_html().encode())

        elif parsed_path.path == "/favicon.png":
            if os.path.exists(PNG_ICON_PATH):
                self.send_response(200)
                self.send_header("Content-type", "image/png")
                self.end_headers()
                with open(PNG_ICON_PATH, "rb") as icon_file:
                    self.wfile.write(icon_file.read())
            else:
                self.send_response(404)
                self.end_headers()

        elif parsed_path.path == "/update-required":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(get_html(show_update_prompt=True).encode())

        elif parsed_path.path == "/create":
            name = query.get('name', [''])[0].strip().replace(" ", "_")
            if name: os.makedirs(os.path.join(PROFILES_DIR, name), exist_ok=True)
            self.redirect_home()

        elif parsed_path.path == "/launch":
            if not check_is_latest_version():
                self.send_response(303)
                self.send_header("Location", "/update-required")
                self.end_headers()
                return

            name = query.get('name', [''])[0]
            edge_path = get_edge_path()
            if edge_path:
                subprocess.Popen([edge_path, f"--user-data-dir={os.path.join(PROFILES_DIR, name)}", 
                                  "--no-proxy-server", "--no-first-run", "--start-maximized", "--new-window"])
            self.redirect_home()

        elif parsed_path.path == "/delete":
            name = query.get('name', [''])[0]
            shutil.rmtree(os.path.join(PROFILES_DIR, name), ignore_errors=True)
            self.redirect_home()

    def redirect_home(self):
        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()

    def log_message(self, format, *args): return

def run_server():
    try:
        HTTPServer(("127.0.0.1", PORT), RequestHandler).serve_forever()
    except Exception as e:
        print(f"Server error: {e}")

def open_embedded_window(url):
    edge_executable = get_edge_path()
    if edge_executable and platform.system() == "Windows":
        subprocess.Popen([
            edge_executable, 
            f"--app={url}",
            f"--user-data-dir={MENU_DATA_DIR}",
            # Assigns a unique window shell registration ID so Windows decouples the taskbar grouping
            "--app-id=edge.session.manager.launcher",
            "--window-size=950,720",
            "--no-first-run",
            "--enable-gpu-rasterization",
            "--ignore-gpu-blocklist",
            "--disable-features=WindowControlsOverlay"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        import webbrowser
        webbrowser.open(url)

if __name__ == '__main__':
    server_thread = Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    print(f"Server online on port {PORT}. Registering unique app handle...", flush=True)
    time.sleep(0.5) 
    
    open_embedded_window(f"http://127.0.0.1:{PORT}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down engine cleanly.")
