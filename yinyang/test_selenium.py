
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WebpageTests(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    chrome_options = Options()
    chrome_options.add_argument("--ignore-certificate-errors")
    cls.driver = webdriver.Chrome(options=chrome_options)
  
  def setUp(self):
    self.driver.get("http://127.0.0.1:8000")

  def login(self, username, password):
    self.driver.get("http://127.0.0.1:8000/login")
    username_input = WebDriverWait(self.driver, 10).until(
      EC.presence_of_element_located((By.NAME, "username"))
    )
    username_input.send_keys(username)
    self.driver.find_element(By.NAME, "password").send_keys(password)
    self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Login']").click()

  def logout_if_logged_in(self):
    try:        
      logout_btn = self.driver.find_element(By.LINK_TEXT, "Log Out")
      logout_btn.click()
    except NoSuchElementException:        
      pass

  def test_01_title(self):    
    self.driver.get("http://127.0.0.1:8000")
    self.assertEqual(self.driver.title, "Yin Yang")

  def test_02_welcome_message(self):
    self.logout_if_logged_in()
    self.driver.get("http://127.0.0.1:8000")
    intro_container = WebDriverWait(self.driver, 10).until(
      EC.presence_of_element_located((By.CLASS_NAME, "intro-container"))
    )
    message_el = intro_container.find_element(By.CLASS_NAME, "intro-text")
    self.assertTrue(message_el)

    message_text = message_el.text
    self.assertTrue(message_text)

    expected_text = (
      "Start your journey towards balanced mental health. In YinYang, we believe in embracing both positive and negative thoughts while focusing on the power of positivity. For each negative thought you log, we'll encourage you to reflect and submit a positive one, helping you to build a habit of positive thinking. Let’s begin with your first thought and start achieving a more balanced mind."
    )
    self.assertEqual(message_text, expected_text)
  
  def test_03_login_user(self):    
    self.login("juliaand", "juliaand")
    success = WebDriverWait(self.driver, 10).until(
      EC.presence_of_element_located((By.ID, "negative-form-flex"))
    )
    self.assertTrue(success)

  def test_04_quotes_display(self):
    self.login("juliaand", "juliaand")
    self.driver.get("http://127.0.0.1:8000")
    quote_el = WebDriverWait(self.driver, 10).until(
      EC.presence_of_element_located((By.CLASS_NAME, "random-quote"))
    )
    self.assertTrue(quote_el)

  def test_05_navbar_links_displayed(self):
    self.login("juliaand", "juliaand")
    self.driver.get("http://127.0.0.1:8000")
    navbar = WebDriverWait(self.driver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, ".navbar.navbar-expand-lg"))
    )
    self.assertTrue(navbar)

    # Expected links and their corresponding icons
    expected_links = {
        "Dashboard": "bi-grid-fill",
        "You": "bi-person",
        "Home": "bi-house-door",
        "Log Out": None
    }
    for link_text, icon_class in expected_links.items():
      try:
      # Find each link by its text and assert it exists
        link = self.driver.find_element(By.LINK_TEXT, link_text)
        self.assertIsNotNone(link, f"Link '{link_text}' not found in navbar.")
      except NoSuchElementException:
        # Icons are displayed on smaller screens
        if icon_class:
          icon = self.driver.find_element(By.CSS_SELECTOR, f"i.{icon_class}")
          self.assertIsNotNone(icon, f"Icon for '{link_text}' not found in navbar.")
        else:
          self.fail(f"Link '{link_text}' not found, and no icon expected.")

  def test_06_create_n_and_p_logs(self):
    self.login("juliaand", "juliaand")

    negative_input=WebDriverWait(self.driver, 20).until(
      EC.presence_of_element_located((By.XPATH, "//div[@id='negative-form-flex']//input[@type='text' and @name='entry']"))
    )
    negative_input.send_keys("Testing negative entry")

    tag_dropdown_n = WebDriverWait(self.driver, 10).until(
      EC.presence_of_element_located((By.XPATH, "//div[@id='negative-form-flex']//select[@name='tag']"))
    )
    tag_dropdown_n.find_element(By.XPATH, "//div[@id='negative-form-flex']//option[@value='WORK']").click()

    self.driver.find_element(By.XPATH, "//div[@id='negative-form-flex']//input[@type='submit' and @value='SUBMIT']").click()

    success = WebDriverWait(self.driver, 10).until(
      EC.presence_of_element_located((By.ID, "positive-form-flex"))
    )
    self.assertTrue(success)

    positive_form_visible = WebDriverWait(self.driver, 20).until(
      EC.visibility_of_element_located((By.ID, "positive-form-flex"))
    )  

    positive_input=WebDriverWait(self.driver, 10).until(
      EC.presence_of_element_located((By.XPATH, "//div[@id='positive-form-flex']//input[@type='text' and @name='entry']"))
    )
    positive_input.send_keys("Testing positive entry")

    tag_dropdown_p = WebDriverWait(self.driver, 10).until(
      EC.presence_of_element_located((By.XPATH, "//div[@id='positive-form-flex']//select[@name='tag']"))
    )
    tag_dropdown_p.find_element(By.XPATH, "//div[@id='positive-form-flex']//option[@value='WORK']").click()

    self.driver.find_element(By.XPATH, "//div[@id='positive-form-flex']//input[@type='submit' and @value='SUBMIT']").click()
    success = WebDriverWait(self.driver, 10).until(
      EC.presence_of_element_located((By.CLASS_NAME, "rebound"))
    )
    self.assertTrue(success)

  def test_07_dashboard(self):
    self.login("juliaand", "juliaand")

    self.driver.find_element(By.ID, "dashboard-link").click()
    success = WebDriverWait(self.driver, 10).until(
      EC.presence_of_element_located((By.ID, "logs-grid"))
    )
    self.assertTrue(success)

  def test_08_see_all_logs(self):
    self.login("juliaand", "juliaand")
    self.driver.get("http://127.0.0.1:8000/dashboard/1")

    see_all_btn = WebDriverWait(self.driver, 20).until(
      EC.element_to_be_clickable((By.ID, "see-all-btn"))
    )
    self.driver.execute_script("arguments[0].scrollIntoView(true);", see_all_btn)
    time.sleep(1)
    see_all_btn.click()

    success = WebDriverWait(self.driver, 20).until(
      EC.presence_of_element_located((By.ID, "filter-form"))
    )
    self.assertTrue(success)

  def test_09_load_more_logs(self):
    self.login("juliaand", "juliaand")
    self.driver.get("http://127.0.0.1:8000/dashboard/1/logs")    
    
    logs_container = self.driver.find_element(By.ID, "logs-flex")
    initial_container_height = self.driver.execute_script("return arguments[0].scrollHeight;", logs_container)
    
    try:
      load_more_btn = WebDriverWait(self.driver, 20).until(
        EC.element_to_be_clickable((By.ID, "load-more-btn"))
      )
      self.driver.execute_script("arguments[0].scrollIntoView(true);", load_more_btn )
      time.sleep(1)
      load_more_btn .click()

      time.sleep(2)
      self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      time.sleep(1)
      new_container_height = self.driver.execute_script("return arguments[0].scrollHeight;", logs_container)
      self.assertTrue( new_container_height > initial_container_height)
    except NoSuchElementException:
      new_container_height = self.driver.execute_script("return arguments[0].scrollHeight;", logs_container)
      self.assertEqual( new_container_height, initial_container_height)

  def test_10_filter_logs_negative(self):
    self.login("juliaand", "juliaand")
    self.driver.get("http://127.0.0.1:8000/dashboard/1/logs")

    initial_logs_count_text = self.driver.find_element(By.CSS_SELECTOR, ".total-logs-num").text
    initial_logs_count = int(initial_logs_count_text.split(': ')[1]) # Extract the number after "Results: "

    tag_dropdown = WebDriverWait(self.driver, 10).until(
      EC.presence_of_element_located((By.XPATH, "//form[@id='filter-form']//select[@id='id_thought_type']"))
    )
    tag_dropdown.find_element(By.XPATH, "//form[@id='filter-form']//option[@value='NEGATIVE']").click()
    self.driver.find_element(By.XPATH, "//form[@id='filter-form']//input[@type='submit' and @value='Filter']").click()
    time.sleep(3)

    filtered_logs_count_text = self.driver.find_element(By.CSS_SELECTOR, ".total-logs-num").text
    filtered_logs_count = int(filtered_logs_count_text.split(': ')[1])
    time.sleep(1)
    if initial_logs_count == 1 and filtered_logs_count == 1:
      self.assertEqual(initial_logs_count, filtered_logs_count)
    else:
      self.assertNotEqual(initial_logs_count, filtered_logs_count)
    
  
  def test_11_filter_logs_positive(self):
    self.login("juliaand", "juliaand")
    self.driver.get("http://127.0.0.1:8000/dashboard/1/logs")

    initial_logs_count_text = self.driver.find_element(By.CSS_SELECTOR, ".total-logs-num").text
    initial_logs_count = int(initial_logs_count_text.split(': ')[1])

    tag_dropdown = WebDriverWait(self.driver, 10).until(
      EC.presence_of_element_located((By.XPATH, "//form[@id='filter-form']//select[@id='id_thought_type']"))
    )
    tag_dropdown.find_element(By.XPATH, "//form[@id='filter-form']//option[@value='POSITIVE']").click()
    self.driver.find_element(By.XPATH, "//form[@id='filter-form']//input[@type='submit' and @value='Filter']").click()
    time.sleep(3)

    filtered_logs_count_text = self.driver.find_element(By.CSS_SELECTOR, ".total-logs-num").text
    filtered_logs_count = int(filtered_logs_count_text.split(': ')[1])
    time.sleep(1)
    if initial_logs_count == 1 and filtered_logs_count == 1:
      self.assertEqual(initial_logs_count, filtered_logs_count)
    else:
      self.assertNotEqual(initial_logs_count, filtered_logs_count)

  def test_12_delete_logs(self):
    self.login("juliaand", "juliaand")
    self.driver.get("http://127.0.0.1:8000/dashboard/1")

    positive_log_container = WebDriverWait(self.driver, 10).until(
      EC.presence_of_element_located((By.XPATH, "//p[contains(@class, 'log-entry') and contains(text(), 'Testing positive entry')]"))
    )
    time.sleep(2)
    positive_parent_log_div = positive_log_container.find_element(By.XPATH, "./ancestor::div[contains(@class, 'positive-log')]")
    p_delete_btn = positive_parent_log_div.find_element(By.CLASS_NAME, "delete-log-btn")  
    p_delete_btn.click()
    p_confirm_delete = WebDriverWait(self.driver, 10).until(
      EC.element_to_be_clickable((By.ID, "delete-confirm-btn"))
    )
    p_confirm_delete.click()
    time.sleep(2)
    deleted = WebDriverWait(self.driver, 10).until(
      EC.invisibility_of_element_located((By.XPATH, "//p[contains(@class, 'log-entry') and contains(text(), 'Testing positive entry')]"))
    )
    self.assertTrue(deleted)

    negative_log_container = WebDriverWait(self.driver, 10).until(
      EC.presence_of_element_located((By.XPATH, "//p[contains(@class, 'log-entry') and contains(text(), 'Testing negative entry')]"))
    )
    time.sleep(2)
    negative_parent_log_div =  negative_log_container.find_element(By.XPATH, "./ancestor::div[contains(@class, 'negative-log')]")
    n_delete_btn = negative_parent_log_div.find_element(By.CLASS_NAME, "delete-log-btn")  
    n_delete_btn.click()
    n_confirm_delete = WebDriverWait(self.driver, 10).until(
      EC.element_to_be_clickable((By.ID, "delete-confirm-btn"))
    )
    n_confirm_delete.click()
    time.sleep(2)
    deleted = WebDriverWait(self.driver, 10).until(
      EC.invisibility_of_element_located((By.XPATH, "//p[contains(@class, 'log-entry') and contains(text(), 'Testing negative entry')]"))
    )
    self.assertTrue(deleted)
  
  def test_13_completed_goals_link_displayed(self):
    self.login("juliaand", "juliaand")
    profile_link = WebDriverWait(self.driver, 10).until(
      EC.presence_of_element_located((By.ID, "profile-link"))
    )
    self.assertTrue(profile_link)
    profile_link.click()
    completed_goals_link = WebDriverWait(self.driver, 20).until(
      EC.element_to_be_clickable((By.XPATH, "//h4/a[contains(@href, 'completed_goals_list') and text()[contains(., 'My completed goals')]]"))
    )
    self.driver.execute_script("arguments[0].scrollIntoView(true);", completed_goals_link)    
    WebDriverWait(self.driver, 2).until(EC.visibility_of(completed_goals_link))
    time.sleep(2)
    completed_goals_link.click()
    completed_goals_header = WebDriverWait(self.driver, 10).until(
      EC.presence_of_element_located((By.TAG_NAME, "h2"))
    )
    self.assertTrue(completed_goals_header)
    self.assertEqual(completed_goals_header.text, "My completed goals")
    current_url = self.driver.current_url
    self.assertIn("/completed_goals_list", current_url)


  @classmethod
  def tearDownClass(cls):
    cls.driver.delete_all_cookies()
    cls.driver.quit()

if __name__ == "__main__":
  unittest.main() 
    