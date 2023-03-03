from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import os
import json
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

config = {}

blur_url = "https://blur.io/"
base_blur_filters = {
    "traits": [],
    "hasAsks": True,
}
furballs_contract_addr = "0x2d004b72d8b7d36f9da2e4a14516618bf53bac57"
blur_furballs_tokens_base_url = f"https://core-api.prod.blur.io/v1/collections/furballs-com-official/tokens"
blur_furballs_collection_url = f"https://core-api.prod.blur.io/v1/collections/furballs-com-official"
blur_1d_chart_url = f"https://core-api.prod.blur.io/v1/charts/everything?collectionId={furballs_contract_addr}&spanMs=86400000&intervalMs=300000"
blur_7d_chart_url = f"https://core-api.prod.blur.io/v1/charts/everything?collectionId={furballs_contract_addr}&spanMs=604800000&intervalMs=3600000"
mm_url = ""
ff_profile_path = ""
mm_pass = ""
polling_freq_min = 5
furballs_info_url = ""
furballs_info_api_key = ""
headless_firefox = False


################################################################################
# main()
################################################################################
def main():
    sleep(3)
    print("Open MetaMask...")
    driver.get(mm_url)
    sleep(3)
    print("Unlock MetaMask...")
    driver.find_element(By.ID, "password").send_keys(mm_pass)
    sleep(3)
    driver.find_element(By.XPATH, '//button[text()="Unlock"]').click()
    sleep(5)
    print("Open blur.io...")
    driver.get(f"{blur_url}collections")
    sleep(5)
    try:
        print("Connect Wallet to blur.io...")
        driver.find_element(By.XPATH, '//button//*[contains(text(), "connect wallet")]').click()
        sleep(3)
        driver.find_element(By.ID, 'METAMASK').click()
    except Exception as e:
        print("Couldn't find Connect Wallet button.  Might already be connected.")
    while True:
        # Reload config here so that some changes can be made without killing the script.
        load_config()
        sleep(5)
        # Try getting collection stats up to 5 times before giving up.
        for _ in range(0, 5):
            collection_stats = get_collection_stats()
            if collection_stats is not None:
                break
            # Wait 30 seconds before retrying
            sleep(30)
        if collection_stats is None:
            print("ERROR: Unable to get collection info from blur.io after 5 retries.")
            print(f"Trying again in {polling_freq_min} minutes...")
            continue
        # Try getting listings up to 5 times before giving up.
        for _ in range(0, 5):
            listings = get_blur_listings()
            if listings is not None:
                break
            # Wait 30 seconds before retrying
            sleep(30)
        if listings is None:
            print("ERROR: Unable to get listings from blur.io after 5 retries.")
            print(f"Trying again in {polling_freq_min} minutes...")
            continue
        # Try getting 1d sales up to 5 times before giving up.
        for _ in range(0, 5):
            num_sales_1d = get_num_sales(blur_1d_chart_url)
            if num_sales_1d is not None:
                collection_stats['num_sales_1d'] = num_sales_1d
                break
            sleep(30)
        # Try getting 7d sales up to 5 times before giving up.
        for _ in range(0, 5):
            num_sales_7d = get_num_sales(blur_7d_chart_url)
            if num_sales_7d is not None:
                collection_stats['num_sales_7d'] = num_sales_7d
                break
            sleep(30)
        if (num_sales_1d is None) or (num_sales_7d is None):
            print("ERROR: Unable to get charts data from blur.io after 5 retries.")
            print(f"Trying again in {polling_freq_min} minutes...")
            continue

        # Try sending listings to furballs.info up to 5 times before giving up.
        for _ in range(0, 5):
            success = send_listings(collection_stats, listings)
            if success:
                break
        sleep(polling_freq_min * 60)


################################################################################
#
################################################################################
def get_collection_stats():
    info = {}
    try:
        url = blur_furballs_collection_url
        driver.get(url)
        response_json = driver.find_element(By.XPATH, '//body').text
        response = json.loads(response_json)
        collection = response['collection']
        owner_pct = round(
            (collection['numberOwners'] / collection['totalSupply']) * 100, 1)
        info = {
            "floor_price": round(float(collection['floorPrice']['amount']), 3),
            "total_supply": collection['totalSupply'],
            "num_owners": collection['numberOwners'],
            "owner_pct": owner_pct,
            "volume_1d": round(float(collection['volumeOneDay']['amount']), 3),
            "volume_7d": round(float(collection['volumeOneWeek']['amount']), 3),
        }
    except Exception as e:
        print("ERROR: Failed to get collection info from blur.io.")
        print(e)
        info = None
    return info


################################################################################
#
################################################################################
def get_blur_listings():
    next_page = True
    cursor = None
    listings = []
    try:
        while next_page:
            filters = base_blur_filters.copy()
            if cursor is not None:
                filters['cursor'] = cursor
            print(filters)
            url = f"{blur_furballs_tokens_base_url}?filters={json.dumps(filters)}"
            driver.get(url)
            response_json = driver.find_element(By.XPATH, '//body').text
            response = json.loads(response_json)
            total_count = response['totalCount']
            tokens = response['tokens']
            listings.extend(tokens)
            print(f"Total Count: {total_count}")
            print(f"{len(tokens)} Listings on Current Page")
            print(f"{len(listings)} Total Listings")
            if (total_count - len(listings)) > 0:
                sleep(1)
                last_token = tokens[-1]
                cursor = {
                    "price": {
                        "amount": last_token['price']['amount'],
                        "unit": last_token['price']['unit'],
                        "time": last_token['price']['listedAt'],
                    },
                    "tokenId": last_token['tokenId']
                }
            else:
                next_page = False
    except Exception as e:
        print("ERROR: Failed to get listings from blur.io.")
        print(e)
        listings = None

    return listings


################################################################################
#
################################################################################
def get_num_sales(url):
    num_sales = 0
    try:
        driver.get(url)
        response_json = driver.find_element(By.XPATH, '//body').text
        response = json.loads(response_json)
        intervals = response['intervals']
        for interval in intervals:
            num_sales += len(interval['sales'])
    except Exception as e:
        print("ERROR: Failed to get sales from blur.io.")
        print(e)
        num_sales = None

    return num_sales


################################################################################
#
################################################################################
def send_listings(collection_stats, listings):
    success = True
    try:
        data = {
            "api_key": furballs_info_api_key,
            "collection_stats": collection_stats,
            "tokens": listings,
        }
        response = requests.post(furballs_info_url, json={
                                 'data': data}, verify=False)
        print(response.json())
    except Exception as e:
        print("ERROR: Failed to send listings to furballs.info.")
        print(e)
        success = False
    return success


################################################################################
# Load Config JSON File
################################################################################
def load_config():
    global config
    global mm_url
    global mm_pass
    global ff_profile_path
    global polling_freq_min
    global furballs_info_url
    global furballs_info_api_key
    global headless_firefox
    print("Load blur_listings_config.json...")
    with open("blur_listings_config.json", "r") as f:
        config = json.load(f)

    mm_url = config['mm_url']
    mm_pass = config['mm_pass']
    ff_profile_path = config['ff_profile_path']
    polling_freq_min = config['blur_polling_freq_min']
    furballs_info_url = config['furballs_info_url']
    furballs_info_api_key = config['furballs_info_api_key']
    headless_firefox = config['headless']


################################################################################
# Configure Selenium Webdriver
################################################################################
def configure_driver():
    global options
    global driver
    options = Options()
    options.add_argument("-profile")
    options.add_argument(ff_profile_path)
    if headless_firefox:
        options.add_argument("-headless")
    #options.headless = headless_firefox
    driver = webdriver.Firefox(options=options)


################################################################################
# Script Entry Point
################################################################################
if __name__ == '__main__':
    load_config()
    if not os.path.isdir(ff_profile_path):
        print("Profile not found:")
        print(ff_profile_path)
        exit()
    configure_driver()
    main()
    driver.close()
