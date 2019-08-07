from selenium import webdriver
import os
import time

from selenium.common.exceptions import NoSuchElementException

from utility_methods import *
from selenium.webdriver.common.keys import Keys


class InstagramBot:

    def __init__(self, username, password):
        """
        Initializes an instance of the InstagramBot class.
        Call the login method to authenticate a user with IG.

        Args:
            username:str: The Instagram username of a user
            password:str: The Instagram password of a user
        Attributes:
            driver:Selenium.webdriver.Chrome: the Chromedriver that is used to automate browser action
        """

        self.username = username
        self.password = password

        self.ignore_list = ['']

        self.browser_profile = webdriver.ChromeOptions()
        self.browser_profile.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        self.driver = webdriver.Chrome('./chromedriver.exe', options=self.browser_profile)
        self.base_url = 'https://www.instagram.com'
        self.login()

    @insta_method
    def login(self):
        self.driver.get('{}/accounts/login/'.format(self.base_url))

        username_input = self.driver.find_elements_by_css_selector('form input')[0]
        password_input = self.driver.find_elements_by_css_selector('form input')[1]
        time.sleep(2.3)

        username_input.send_keys(self.username)
        time.sleep(1.7)
        password_input.send_keys(self.password)
        time.sleep(2.15)
        password_input.send_keys(Keys.ENTER)

        time.sleep(1.885)

    @insta_method
    def nav_user(self, user):
        self.driver.get('{}/{}'.format(self.base_url, user))

    @insta_method
    def follow_user(self, username):
        self.driver.get('https://www.instagram.com/' + username + '/')
        time.sleep(2)
        follow_button = self.driver.find_elements_by_css_selector('button')
        for button in follow_button:
            print(button.text)
        follow_button = follow_button[1]
        print(follow_button.text)
        if follow_button.text == 'Follow' or follow_button.text == 'Follow Back':
            follow_button.click()
        else:
            print("You are already following this user")

    @insta_method
    def unfollow_user(self, username):
        self.driver.get('https://www.instagram.com/' + username + '/')
        unfollow_button = self.driver.find_elements_by_css_selector('button')
        for button in unfollow_button:
            print(button.text)
        following = unfollow_button[0]
        requested = unfollow_button[1]
        if following.text == 'Following':
            unfollow_button = following
        elif requested.text == 'Requested':
            unfollow_button = requested
        else:
            print("You are not following this user")
            return
        unfollow_button.click()
        time.sleep(2)
        confirm_button = self.driver.find_element_by_xpath('//button[text() = "Unfollow"]')
        confirm_button.click()

    @insta_method
    def like_latest_posts(self, user, n_posts, like=True):
        """
        Likes a number of a users latest posts, specified by n_posts.
        Args:
            user:str: User whose posts to like or unlike
            n_posts:int: Number of most recent posts to like or unlike
            like:bool: If True, likes recent posts, else if False, unlikes recent posts
        TODO: Currently maxes out around 15.
        """

        action = 'Like' if like else 'Unlike'

        self.nav_user(user)

        imgs = []
        imgs.extend(self.driver.find_elements_by_class_name('_9AhH0'))

        for img in imgs[:n_posts]:
            img.click()
            time.sleep(1)
            try:
                self.driver.find_element_by_xpath("//*[@aria-label='{}']".format(action)).click()
            except Exception as e:
                print(e)

            self.driver.find_elements_by_class_name('ckWGn')[0].click()

    @insta_method
    def find_buttons(self, button_text):
        """
        Finds buttons for following and unfollowing users by filtering follow elements for buttons. Defaults to finding follow buttons.
        Args:
            button_text: Text that the desired button(s) has
        """

        buttons = self.driver.find_elements_by_xpath("//*[text()='{}']".format(button_text))

        return buttons

    def unfollow_batch(self, num, num_already):
        self.nav_user(self.username)
        time.sleep(.8)
        followers_panel = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a')
        followers_panel.click()
        time.sleep(.9)

        # users_arr = []
        # for i in range(1, num + 1):
        #     print(i)
        #     first_user = self.driver.find_elements_by_xpath('/html/body/div[3]/div/div[2]/ul/div/li[{}]/div/div[1]/div/a'.format(i))
        #     if not first_user:
        #         first_user = self.driver.find_elements_by_xpath('/html/body/div[3]/div/div[2]/ul/div/li[{}]/div/div[1]/div[2]/div[1]/a'.format(i))
        #         '//*[@id="fe8710477e86b4"]/div/div/a'
        #         '//*[@id="fe8710477e86b4"]/div/div/a'
        #         '//*[@id="fe8710477e86b4"]'
        #     if not first_user:
        #         print("ERROR")
        #     users_arr.append(first_user[0].get_attribute(("href")))
        # # '/html/body/div[3]/div/div[2]/ul/div/li[1]'
        # # '/html/body/div[3]/div/div[2]/ul/div/li[2]'
        # # '/html/body/div[3]/div/div[2]/ul/div/li[3]/div/div[1]/div[2]/div[1]/a'
        #
        # print(users_arr)
        # first_user.click()

        # '/html/body/div[3]/div/div[2]/ul/div/li[125]/div/div[2]/button'
        # '/html/body/div[3]/div/div[2]/ul/div/li[126]/div/div[2]/button'
        # '/html/body/div[3]/div/div[2]/ul/div/li[2]/div/div[2]/button'

        i = 1
        total_unfollowed = 0
        while total_unfollowed < num:
            # if i % 10 == 0:
            #     time.sleep(30)
            try:
                follower = self.driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/ul/div/li[{}]/div/div[3]/button'.format(i))
                follower.click()

                time.sleep(2)
                confirm_button = self.driver.find_element_by_xpath('//button[text() = "Unfollow"]')
                confirm_button.click()
                time.sleep(2)
                total_unfollowed += 1
                print('Unfollowed #{}.'.format(total_unfollowed + num_already))
                i += 1
            except NoSuchElementException:
                try:
                    follower = self.driver.find_element_by_xpath(
                        '/html/body/div[3]/div/div[2]/ul/div/li[{}]/div/div[2]/button'.format(i))
                    follower.click()

                    time.sleep(2)
                    confirm_button = self.driver.find_element_by_xpath('//button[text() = "Unfollow"]')
                    confirm_button.click()
                    time.sleep(2)
                    total_unfollowed += 1
                    print('Unfollowed #{}.'.format(total_unfollowed + num_already))
                    i += 1
                except NoSuchElementException:
                    print("Got exception. Trying Again.\n")
                    # self.unfollow_batch(num - total_unfollowed, total_unfollowed + num_already)
                    # total_unfollowed = num
                    # i += 20
                    scroll_div = self.driver.find_element_by_xpath('/html/body/div[3]/div/div[2]')
                    scroll_height = self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_div)
                    time.sleep(5)


if __name__ == '__main__':
    ig_bot = InstagramBot('username', 'password')
    # print("Type 'done' once you are logged in: ")
    # input()
    t0 = time.time()
    for i in range(1, 100):
        ig_bot.unfollow_batch(13, 0)
        print('\n{} completed\n'.format(i * 13))
        time.sleep(60)
    # was 1,182
    t1 = time.time()
    print('Unfollowed {} users in {} seconds.'.format(200, (t1 - t0)))
