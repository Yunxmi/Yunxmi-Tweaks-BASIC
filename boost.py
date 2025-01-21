import platform
import subprocess
from requests import session
from datetime import datetime
from hashlib import sha256, md5
import rgbprint
from rgbprint import gradient_print, Color 
import time

service = 1160  # Your service ID, this is used to identify your service.
secret = "8d591368-9294-4137-a5f8-fc7db45de843"  # Make sure to obfuscate this if you want to ensure security.
use_nonce = True  # Use a nonce to prevent replay attacks and request tampering.
def clear():
    subprocess.Popen("cls" if platform.system() == "Windows" else "clear", shell=True)


class Boost:
    def __init__(self, callback=None):
        self.session = session()
        self.session.headers.update({"User-Agent": "Platoboost Python Client/1.0"})
        self.session.headers.update({"Content-Type": "application/json"})
        self.session.headers.update({"Accept": "application/json"})
        self.callback = callback

        self.hostname = "https://api.platoboost.com"

        try:
            response = self.session.get(self.hostname + "/public/connectivity")
            if response.status_code != 200 or not (response.json()["success"] == True):
                raise Exception("Main domain is offline, falling back..")
        except:
            self.hostname = "https://api.platoboost.net"

        self._identifier = self._gethwid()
        self._cached_link = None
        self._cached_time = None
        self._cache_link()

    def _gethwid(self):
        try:
            if platform.system() == "Windows":
                command = "wmic csproduct get uuid"
                uuid = subprocess.check_output(command, shell=True).decode().split("\n")[1].strip()
            elif platform.system() == "Linux":
                try:
                    # Intentar leer el archivo machine-id estándar
                    uuid = subprocess.check_output("cat /etc/machine-id", shell=True).decode().strip()
                except:
                    # Ruta alternativa en Termux o sistemas limitados
                    uuid = subprocess.check_output("cat $HOME/dbus/machine-id", shell=True).decode().strip()
            elif platform.system() == "Darwin":
                uuid = subprocess.check_output(
                    "ioreg -rd1 -c IOPlatformExpertDevice | grep IOPlatformSerialNumber",
                    shell=True
                ).decode().split('=')[1].strip().replace('"', '')
            else:
                raise OSError("Unsupported operating system")

            return sha256(uuid.encode()).hexdigest()

        except Exception as e:
            if self.callback:
                self.callback(f"Error obtaining HWID: {e}")
            raise

    def _cache_link(self):
        if self._cached_link is None or self._cached_time is None or (datetime.now() - self._cached_time).total_seconds() > 5 * 60:
            response = self.session.post(self.hostname + "/public/start", json={
                "service": service,
                "identifier": self._identifier,
            })

            if response.status_code == 200:
                decoded = response.json()

                if decoded["success"] == True:
                    self._cached_link = decoded["data"]["url"]
                    self._cached_time = datetime.now()
                else:
                    if self.callback is not None:
                        self.callback(decoded["message"])
                    return False
            elif response.status_code == 429:
                if self.callback is not None:
                    self.callback("You are being rate-limited, please wait 20 seconds and try again.")
                return False
            else:
                if self.callback is not None:
                    self.callback("Failed to cache link.")
                return False
        else:
            return self._cached_link

    def _generate_nonce(self):
        if use_nonce:
            return md5(str(datetime.now().timestamp()).encode()).hexdigest()
        else:
            return "empty"

    def get_link(self):
        link = self._cache_link()

        if link:
            return self._cached_link

    def _redeem_key(self, key):
        nonce = self._generate_nonce()
        endpoint = self.hostname + "/public/redeem/" + str(service)

        body = {
            "identifier": self._identifier,
            "key": key
        }

        if use_nonce:
            body["nonce"] = nonce

        response = self.session.post(endpoint, json=body)

        if response.status_code == 200:
            decoded = response.json()

            if decoded["success"] == True:
                valid = decoded["data"]["valid"]

                if valid:
                    if use_nonce:
                        if decoded["data"]["hash"] == sha256((str.lower(str(valid)) + "-" + nonce + "-" + secret).encode()).hexdigest():
                            return valid
                        else:
                            if self.callback is not None:
                                self.callback("Failed to verify integrity.")
                            return False
                    else:
                        return True
                else:
                    if self.callback is not None:
                        self.callback("Key is invalid.")
                    return False
            else:
                if "unique constraint violation" in decoded["message"]:
                    if self.callback is not None:
                        self.callback("You already have an active key, please wait for it to expire before redeeming it.")
                else:
                    if self.callback is not None:
                        self.callback(decoded["message"])

                return False
        elif response.status_code == 429:
            if self.callback is not None:
                self.callback("You are being rate-limited, please wait 20 seconds and try again.")
            return False
        else:
            if self.callback is not None:
                self.callback("Server returned an invalid status code, please try again later.")
            return False

    def get_flag(self, name):
        nonce = self._generate_nonce()
        endpoint = self.hostname + "/public/flag/" + str(service) + "?name=" + name

        if use_nonce:
            endpoint += "&nonce=" + nonce

        response = self.session.get(endpoint)

        if response.status_code == 200:
            decoded = response.json()

            if decoded["success"] == True:
                value = decoded["data"]["value"]
                str_value = type(value) == bool and str.lower(str(value)) or str(value)

                if use_nonce:
                    if decoded["data"]["hash"] == sha256((str_value + "-" + nonce + "-" + secret).encode()).hexdigest():
                        return value
                    else:
                        if self.callback is not None:
                            self.callback("Failed to verify integrity.")
                        return None
                else:
                    return value
            else:
                if self.callback is not None:
                    self.callback(decoded["message"])
                return None
        else:
            return None

    def verify_key(self, key):
        nonce = self._generate_nonce()
        endpoint = self.hostname + "/public/whitelist/" + str(service) + "?identifier=" + self._identifier + "&key=" + key

        if use_nonce:
            endpoint += "&nonce=" + nonce

        response = self.session.get(endpoint)

        if response.status_code == 200:
            decoded = response.json()

            if decoded["success"] == True:
                valid = decoded["data"]["valid"]

                if valid:
                    if use_nonce:
                        if decoded["data"]["hash"] == sha256((str.lower(str(valid)) + "-" + nonce + "-" + secret).encode()).hexdigest():
                            return valid
                        else:
                            if self.callback is not None:
                                self.callback("Failed to verify integrity.")
                            return False
                    else:
                        return True
                else:
                    if str.startswith(key, "KEY_"):
                        return self._redeem_key(key)
                    else:
                        if self.callback is not None:
                            self.callback("Key is invalid.")
                        return False
            else:
                if self.callback is not None:
                    self.callback(decoded["message"])
                return False
        elif response.status_code == 429:
            if self.callback is not None:
                self.callback("You are being rate-limited, please wait 20 seconds and try again.")
            return False
        else:
            if self.callback is not None:
                self.callback("Server returned an invalid status code, please try again later.")
            return False


# Callback example
def callback(message):
    print(message)

# Display the header with a gradient effect
gradient_print("""
██╗   ██╗██╗   ██╗███╗   ██╗███████╗██╗  ██╗
██║   ██║╚██╗ ██╔╝████╗  ██║██╔════╝╚██╗██╔╝
██║   ██║ ╚████╔╝ ██╔██╗ ██║█████╗   ╚███╔╝ 
╚██╗ ██╔╝  ╚██╔╝  ██║╚██╗██║██╔══╝   ██╔██╗ 
 ╚████╔╝    ██║   ██║ ╚████║███████╗██╔╝ ██╗
  ╚═══╝     ╚═╝   ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
                                            """
                                            , start_color=Color.magenta, 
                                            end_color=Color.dark_blue)

# Display the "Features" and "Requirements" table
print("\n💡 **Features:**")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("| Basic version: Boost your phone to the max 🚀 |")
print("| Performance optimized for the best results ⚡️ |")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

print("\n📋 **Requirements:**")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("| Xiaomi device only 📱        |")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

# Prompt to continue
gradient_print("\n[+]Press Enter to continue...", start_color=Color.blue, end_color=Color.dark_blue)

# Wait for the user to press Enter
input()

# Example usage
boost = Boost(callback)
print("Get key here:", boost.get_link())
key = input("Enter key: ")

if boost.verify_key(key):
    print("Key is valid!")
    clear()
    time.sleep(2)
    
else:
    print("Key is invalid!")
    exit()
    
input("press enter to continue!")

gradient_print("""
██╗   ██╗██╗   ██╗███╗   ██╗███████╗██╗  ██╗
██║   ██║╚██╗ ██╔╝████╗  ██║██╔════╝╚██╗██╔╝
██║   ██║ ╚████╔╝ ██╔██╗ ██║█████╗   ╚███╔╝ 
╚██╗ ██╔╝  ╚██╔╝  ██║╚██╗██║██╔══╝   ██╔██╗ 
 ╚████╔╝    ██║   ██║ ╚████║███████╗██╔╝ ██╗
  ╚═══╝     ╚═╝   ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
                                            """
                                            , start_color=Color.magenta, 
                                            end_color=Color.dark_blue)

# Display the "Features" and "Requirements" table
print("\n💡 **Features:**")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("| Basic version: Boost your phone to the max 🚀 |")
print("| Performance optimized for the best results ⚡️ |")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

print("\n📋 **Requirements:**")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("| Xiaomi device only 📱        |")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
input("Enter to continue")

def run_adb_command(command):
    """
    Runs an ADB command and returns the output or error.
    """
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout, result.stderr
    except FileNotFoundError:
        return "", "❌ ADB is not installed or not found in the system PATH."

def uninstall_app(package_name):
    """
    Uninstalls the app using ADB.
    """
    print(f"📱 Cleaning phone!")
    uninstall_command = ["adb", "shell", "pm", "uninstall", "--user", "0", package_name]
    stdout, stderr = run_adb_command(uninstall_command)

    if "Success" in stdout:
        print(f"✅ Boosted your phone! 🎉")
    else:
        print(f"❌ Failed to boost, are you connected to adb?")
        print(f"Error: {stderr or stdout}")

def main():
    print("📱 Welcome to Yunxmi Tweaker! 🚀")
    print("Ensure your device is already connected via ADB.\n")

    # Uninstall the first app
    uninstall_app("com.miui.powerkeeper")

    # Wait for user input to continue
    input("\nPress Enter to continue...\n")

    # Uninstall the second app
    uninstall_app("com.xiaomi.joyose")

if __name__ == "__main__":
    main()


