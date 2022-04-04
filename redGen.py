import os
import subprocess
import time

from stem import Signal
from stem.control import Controller

from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver

from selenium.webdriver.common.proxy import Proxy, ProxyType

proxy = Proxy()
proxy.proxy_type = ProxyType.MANUAL
proxy.socks_proxy = "127.0.0.1:9050"
proxy.socksVersion = 5

capabilities = webdriver.DesiredCapabilities.FIREFOX
proxy.add_to_capabilities(capabilities)


def generate_accounts(name: str, password: str):
    subprocess.call("start " + os.getcwd() + "\\tor\\Tor\\tor.exe --defaults-torrc " +
                    os.getcwd() + "\\Tor\\Tor\\torrc", shell=True)
    time.sleep(5)
    controller = Controller.from_port(port=9051)
    controller.authenticate("Passwort")
    print("Successfully connected to tor!")
    controller.signal(Signal.NEWNYM)
    print("New Tor connection processed")

    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), desired_capabilities=capabilities)

    driver.get("https://reddit.com/register")
    email_field = driver.find_element(By.ID, "regEmail")
    email_field.send_keys("mail@mail.com")
    email_field.send_keys(Keys.ENTER)

    username_field = driver.find_element(By.ID, "regUsername")

    username_field.send_keys(name)

    password_field = driver.find_element(By.ID, "regPassword")
    password_field.send_keys(password)

    WebDriverWait(driver, 360).until(EC.presence_of_element_located((By.ID, "SearchDropdown")))

    print("created", name)
