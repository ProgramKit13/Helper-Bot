from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

WP_LINK = 'https://web.whatsapp.com'

## XPATHS
CONTACTS = '//*[@id="main"]/header/div[2]/div[2]/span'
MESSAGE_BOX = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'
SEND = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button'
NEW_CHAT = '//*[@id="app"]/div/div[2]/div[3]/header/div[2]/div/span/div[4]/div'
HEAVING_CONTACT = '//*[@id="app"]/div/div[2]/div[2]/div[1]/span/div/span/div/div[2]/div/div/div/div[2]/div/div/div[2]'
OTHER_CONTACT = '//*[@id="app"]/div/div[2]/div[2]/div[1]/span/div/span/div/div[2]/div[2]/div[2]'
NEW_CONTACT = '//*[@id="app"]/div/div[2]/div[2]/div[1]/span/div/span/div/div[2]/div[2]/div[2]/div/div'
SEARCH_CONTACT = '//*[@id="app"]/div/div[2]/div[2]/div[1]/span/div/span/div/div[1]/div[2]/div[2]/div/div[1]'
DONT_HAVE_CONTACT = '//*[@id="app"]/div/div[2]/div[2]/div[1]/span/div/span/div/div[2]/div/div'
GET_ARCHIVE = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div/div'
GET_IMG = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div/ul/div/div[2]'
NEW_SEARCH = '//*[@id="app"]/div/div[2]/div[2]/div[1]/span/div/span/div/div[1]/div[2]/button'
SEND_IMG = '//*[@id="app"]/div/div[2]/div[2]/div[2]/span/div/div/div/div[2]/div/div[2]/div[2]/div/div'
TITLE_IMG = '//*[@id="app"]/div/div[2]/div[2]/div[2]/span/div/div/div/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[1]'

class WhatsApp:
    def __init__(self):
        self.driver = self._setup_driver()
        self.driver.get(WP_LINK)
        print("Please scan the QR Code!")

    @staticmethod
    def _setup_driver():
        print('Loading...')
        chrome_options = Options()
        chrome_options.add_argument("disable-infobars")
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

        return driver

    def _get_element(self, xpath, attempts=5, _count=0):
        '''Safe get_element method with multiple attempts'''
        try:
            element = self.driver.find_element(By.XPATH, xpath)
            return element
        except Exception as e:
            if _count < attempts:
                sleep(2)
                self._get_element(xpath, attempts=attempts, _count=_count+1)
            else:
                return None

    def _click(self, xpath):
        el = self._get_element(xpath)
        if el:
            self.driver.execute_script("arguments[0].click();", el)

    def _send_keys(self, xpath, message):
        el = self._get_element(xpath)
        if el:
            el.send_keys(message)

    def write_message(self, message):
        self._click(MESSAGE_BOX)
        caixa = self._get_element(MESSAGE_BOX)
        if not caixa:
            print(f"Message box not found.")
            return
        partes = message.split('\n')
        for i, part in enumerate(partes):
            caixa.send_keys(part)
            if i < len(partes) - 1:
                self.pula_linha()
                sleep(1)
        self._click(SEND)

    def _paste(self):
        el = self._get_element(MESSAGE_BOX)
        el.send_keys(Keys.SHIFT, Keys.INSERT)

    def send_message(self, message):
        self.write_message(message)
        sleep(2)
        self._click(SEND)

    def get_group_numbers(self):
        try:
            el = self.driver.find_element(By.XPATH, CONTACTS)
            return el.text.split(',')
        except Exception as e:
            print("Group header not found.")

    def search_contact(self, keyword):
        self._click(NEW_CHAT)
        search_box = self._get_element(SEARCH_CONTACT)
        if not search_box:
            return False
        search_box.clear()
        self._send_keys(SEARCH_CONTACT, keyword)
        sleep(2)
        heaving_contact = self._get_element(HEAVING_CONTACT)
        if heaving_contact:
            heaving_contact.click()
            return True
        else:
            other_contact = self._get_element(OTHER_CONTACT)
            if other_contact:
                other_contact.click()
                return True
            else:
                self._click(NEW_SEARCH)  # Clique no botão de voltar
                sleep(1)
                return False

    def get_all_messages(self):
        all_messages_element = self.driver.find_elements(By.CLASS_NAME, '_akbu')
        all_messages_text = [e.text for e in all_messages_element]
        return all_messages_text

    def get_last_message(self):
        all_messages = self.get_all_messages()
        return all_messages[-1]

    def search_new_contact(self, keyword):
        self._click(NEW_CHAT)
        self._send_keys(SEARCH_CONTACT, keyword)
        sleep(2)
        try:
            self._click(NEW_CONTACT)
        except Exception as e:
            print("Contact not found")

    def pula_linha(self):
        caixa = self._get_element(MESSAGE_BOX)
        if caixa:
            sleep(0.2)
            caixa.send_keys(Keys.SHIFT, Keys.ENTER)
        else:
            print(f"Message Box not found.")


    def enviar_imagem(self, image_path):
        attach_btn = self._get_element(GET_ARCHIVE)
        if attach_btn:
            attach_btn.click()
            sleep(2)
            image_input = self._get_element('//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
            if image_input:
                image_input.send_keys(image_path)
                sleep(1)
                title_input = self._get_element(TITLE_IMG)
                title_input.click()
                title_input.send_keys(Keys.ENTER)
            else:
                print("Image not found.")
        else:
            print("Archive Button not found.")