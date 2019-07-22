from selenium import webdriver
import os
import time


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

        self.driver = webdriver.Chrome('./chromedriver.exe')
        self.base_url = 'https://www.instagram.com'
        self.login()


    def login(self):
        self.driver.get('{}/accounts/login/'.format(self.base_url))
        self.driver.find_element_by_name('username').send_keys(self.username)
        self.driver.find_element_by_name('password').send_keys(self.password)

        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button/div').click()
        # self.driver.find_elements_by_xpath("//div[contains(text(), 'Log In')]")[0]

        time.sleep(2)

    def nav_user(self, user):
        self.driver.get('{}/{}'.format(self.base_url, user))

    def follow_user(self, user):
        self.nav_user(user)
        follow_buttons = self.find_buttons('Follow')

        for btn in follow_buttons:
            btn.click()

    def unfollow_user(self, user):
        self.nav_user(user)

        unfollow_btns = self.find_buttons('Following')

        if unfollow_btns:
            for btn in unfollow_btns:
                btn.click()
                unfollow_confirmation = self.find_buttons('Unfollow')[0]
                unfollow_confirmation.click()
        else:
            print('No {} buttons were found.'.format('Following'))

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

    def find_buttons(self, button_text):
        """
        Finds buttons for following and unfollowing users by filtering follow elements for buttons. Defaults to finding follow buttons.
        Args:
            button_text: Text that the desired button(s) has
        """

        buttons = self.driver.find_elements_by_xpath("//*[text()='{}']".format(button_text))

        return buttons


if __name__ == '__main__':
    ig_bot = InstagramBot('test_username', 'test_password')

    ig_bot.follow_user('portraits_pet')
