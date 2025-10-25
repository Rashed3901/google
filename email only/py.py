import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ============ DATA ============
with open("user_ids.txt", "r") as file:
    user_ids = [line.strip() for line in file if line.strip()]

default_password = "oman2025"
positions = [(0, 0), (1000, 0), (0, 600), (1000, 600)]  # positions for batch of 4
lock = threading.Lock()  # to avoid file write conflicts

# ============ LOGIN FUNCTION ============
def login_user(username, position):
    print(f"Logging in as {username}...")

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-save-password-bubble")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")
    options.add_argument(f"--window-size=800,600")
    options.add_argument(f"--window-position={position[0]},{position[1]}")
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    })
    options.set_capability("pageLoadStrategy", "normal")

    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    driver.get("http://accounts.google.com")

    try:
        # Wait for email input
        email_input = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='email']"))
        )
        email_input.clear()
        email_input.send_keys(username)

        # Click Next after email
        next_email = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))
        )
        next_email.click()

        # Check if email failed
        try:
            email_error = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'Ekjuhf')]"))
            )
            print(f"[{username}] Email not found.")
            return
        except:
            pass  # email exists
        # Save successful login
        with lock:
            with open("REAL_ID.txt", "a") as f:
                f.write(username + "\n")

        print(f"[{username}] Login successful!")

    except Exception as e:
        print(f"[{username}] Login failed: {e}")

    finally:
        driver.quit()  # always close browser

# ============ BATCH RUNNER ============
def run_batches(batch_size=4):
    for i in range(0, len(user_ids), batch_size):
        current_batch = user_ids[i:i + batch_size]
        threads = []

        # Start all threads for the batch
        for j, username in enumerate(current_batch):
            position = positions[j % len(positions)]
            thread = threading.Thread(target=login_user, args=(username, position))
            threads.append(thread)
            thread.start()

        # Wait for all threads in batch to finish
        for thread in threads:
            thread.join()

        print(f"Batch {i // batch_size + 1} finished. All windows closed.")

# ============ START SCRIPT ============
if __name__ == "__main__":
    run_batches()
    print("All batches completed. Script finished.")