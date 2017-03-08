from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time
from Twidder import database_helper, app
path = 'driver/chromedriver'


class ChromeTestCase(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Chrome(path)
		self.test_email = "test1337@test.com"
		self.wait = WebDriverWait(self.browser, 5)
	# self.addCleanup(self.browser.quit())

	def test_signup_wrong(self):
		self.browser.get('http://localhost:5000')
		self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'jumbotron')))
		firstname = self.browser.find_element_by_id('firstname')
		familyname = self.browser.find_element_by_id('familyname')
		gender = Select(self.browser.find_element_by_id('gender'))
		city = self.browser.find_element_by_id('city')
		country = self.browser.find_element_by_id('country')
		email = self.browser.find_element_by_id('signup_email')
		password = self.browser.find_element_by_id('signup_password_1')
		password_repeat = self.browser.find_element_by_id('signup_password_2')

		firstname.send_keys("Test")
		familyname.send_keys("Testsson")
		gender.select_by_visible_text("Male")
		city.send_keys("Stockholm")
		country.send_keys("Sweden")
		email.send_keys(self.test_email)
		password.send_keys("password")
		password_repeat.send_keys("another_password")

		self.browser.find_element_by_id("signup_submit").click()
		time.sleep(1)
		alert_text = self.browser.find_element_by_id("signUp-alert")
		assert alert_text.get_attribute("innerHTML") == "Password doesn't match!"
		self.clean_up()

	def test_signup_correct(self):
		with app.app_context():
			database_helper.remove_user(self.test_email)
		self.browser.get('http://localhost:5000')
		self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'jumbotron')))
		firstname = self.browser.find_element_by_id('firstname')
		familyname = self.browser.find_element_by_id('familyname')
		gender = Select(self.browser.find_element_by_id('gender'))
		city = self.browser.find_element_by_id('city')
		country = self.browser.find_element_by_id('country')
		email = self.browser.find_element_by_id('signup_email')
		password = self.browser.find_element_by_id('signup_password_1')
		password_repeat = self.browser.find_element_by_id('signup_password_2')

		pw = "password"
		firstname.send_keys("Test")
		familyname.send_keys("Testsson")
		gender.select_by_visible_text("Male")
		city.send_keys("Stockholm")
		country.send_keys("Sweden")
		email.send_keys(self.test_email)
		password.send_keys(pw)
		password_repeat.send_keys(pw)

		self.browser.find_element_by_id("signup_submit").click()
		try:
			placeholder = WebDriverWait(self.browser, 5).until(
				EC.visibility_of_element_located((By.ID, 'home')))
			assert '<div class="user-info"' in placeholder.get_attribute("innerHTML")
		finally:
			self.clean_up()

	def test_login(self):
		self.add_test_user()
		self.browser.get('http://localhost:5000')
		self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'jumbotron')))
		email = self.browser.find_element_by_id('login_email')
		password = self.browser.find_element_by_id('login_password')

		pw = "password"
		email.send_keys(self.test_email)
		password.send_keys(pw)

		self.browser.find_element_by_id("login_submit").click()
		try:
			placeholder = self.wait.until(
				EC.visibility_of_element_located((By.ID, 'home')))
			assert '<div class="user-info">' in placeholder.get_attribute("innerHTML")
		finally:
			self.clean_up()
			self.browser.quit()

	def test_change_password(self):
		self.add_test_user()
		self.browser.get('http://localhost:5000')
		self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'jumbotron')))
		email = self.browser.find_element_by_id('login_email')
		password = self.browser.find_element_by_id('login_password')

		pw = "password"
		email.send_keys(self.test_email)
		password.send_keys(pw)

		self.browser.find_element_by_id("login_submit").click()

		try:
			elm = self.wait.until(EC.visibility_of_element_located((By.ID, 'home')))
			account_tab = self.browser.find_element_by_id('account-tab')
			account_tab.click()
			old_password = self.wait.until(EC.visibility_of_element_located((By.ID, 'old')))
			new1 = self.browser.find_element_by_id('new1')
			new2 = self.browser.find_element_by_id('new2')

			new_pw = "uuuuuuuu"
			old_password.send_keys(pw)
			new1.send_keys(new_pw)
			new2.send_keys(new_pw)
			self.browser.find_element_by_id("change-submit").click()
			alert_text = self.wait.until(EC.visibility_of_element_located((By.ID, 'changeAlert')))

			assert alert_text.get_attribute("innerHTML") == "Password changed"

		finally:
			self.clean_up()

	def test_logout(self):
		self.add_test_user()
		self.browser.get('http://localhost:5000')
		self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'jumbotron')))
		email = self.browser.find_element_by_id('login_email')
		password = self.browser.find_element_by_id('login_password')

		pw = "password"
		email.send_keys(self.test_email)
		password.send_keys(pw)

		self.browser.find_element_by_id("login_submit").click()

		try:
			elm = self.wait.until(EC.visibility_of_element_located((By.ID, 'home')))
			account_tab = self.browser.find_element_by_id('account-tab')
			account_tab.click()
			logout_button = self.wait.until(EC.visibility_of_element_located((By.ID, 'logout-button')))
			logout_button.click()

			jumbotron = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'jumbotron')))
			assert "Welcome to Twidder!" in jumbotron.get_attribute("innerHTML")

		finally:
			self.clean_up()

	def add_test_user(self):
		with app.app_context():
			database_helper.add_user("test1337@test.com", "password", "Test", "Testsson", "Male", "Stockholm", "Sweden")

	def clean_up(self):
		self.browser.quit()
		with app.app_context():
			database_helper.remove_user(self.test_email)
			database_helper.remove_logged_in_user(self.test_email)

if __name__ == '__main__':
	unittest.main(verbosity=1)
