"""
Download all Freeleech torrents from waffles.fm with at least 1 leecher.
"""
from base64 import b64encode
from selenium import webdriver
import os
import time
import transmissionrpc

WAFFLES_USER = os.environ['WAFFLES_USER']
WAFFLES_PASS = os.environ['WAFFLES_PASS']

TRANSMISSION_HOST = os.environ['TRANSMISSION_HOST']
TRANSMISSION_PORT = os.environ['TRANSMISSION_PORT']


def main():
    """
    Download all Freeleech torrents from waffles.fm with at least 1 leecher.
    """
    # Fetch all currently seeding torrents
    try:
        tc = transmissionrpc.Client(TRANSMISSION_HOST, port=TRANSMISSION_PORT)
    except:
        return
    torrents = [x.name for x in tc.get_torrents()]

    print '>>> You are seeding {} torrents...'.format(len(torrents))

    # To prevent download dialog
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.download.dir', os.getcwd())
    profile.set_preference(
        'browser.helperApps.neverAsk.saveToDisk', 'application/x-bittorrent'
    )

    # Boot up Firefox & navigate to waffles.fm
    driver = webdriver.Firefox(profile)
    driver.get('https://waffles.fm/login')

    # Login
    username = driver.find_element_by_id('username')
    password = driver.find_element_by_id('password')
    username.send_keys(WAFFLES_USER)
    password.send_keys(WAFFLES_PASS)
    password.submit()

    # Navigate to Freeleech torrents sorted by number of leechers descending
    driver.get('https://waffles.fm/browse.php?q=is%3Afree&s=leechers&d=desc')

    print '>>> Looking for freeleech torrents with at least 1 leecher...'

    # Loop through each result
    table = driver.find_element_by_id('browsetable')
    for idx, row in enumerate(table.find_elements_by_tag_name('tr')):
        if idx == 0:
            continue

        try:  # If there is at least 1 leecher
            leechers = row.find_element_by_css_selector("a[href*='todlers']")
            if int(leechers.text) < 1:
                continue
        except:
            continue

        # Ensure we're not already seeding this torrent
        title = row.find_element_by_css_selector("a[href*='details.php']")
        if title.text in torrents:
            continue

        print '>>> Found {} with at least {} leecher...'.format(
            title.text, leechers.text
        )

        # Download the torrent
        row.find_element_by_css_selector("a[href*='download.php']").click()

    # Loop through each newly downoaded torrent
    new_torrents = os.listdir(os.getcwd())
    new_torrents = filter(lambda x: x.endswith('.torrent'), new_torrents)
    for path in new_torrents:
        with open(path, 'rb') as f:
            data = b64encode(f.read())

        tc.add_torrent(data, timeout=60 * 2)  # Add the torrent to Transmission
        os.remove(path)  # Remove the torrent from the filesystem

        time.sleep(3)  # Be nice :D


if __name__ == '__main__':
    main()
