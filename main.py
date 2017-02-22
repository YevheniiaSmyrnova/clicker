from selenium import webdriver
import subprocess
import cv2
import numpy as np
import tempfile
import argparse
import logging


parser = argparse.ArgumentParser()
parser.add_argument("url", help="URL to the page")
parser.add_argument("img", help="path to the image")
args = parser.parse_args()


def driver_click(driver, x, y, default_y_offset=66):

    # more broot force click coords via X11 automation tool
    # this doesn't work with tightvnc though
    position = driver.get_window_position()
    x += position['x']
    # need to take into account offset by y that is a constant
    y += position['y'] + default_y_offset
    subprocess.call(["xdotool", "mousemove", "--sync", str(x), str(y), "click", "1"])

    logging.info("x=%d y=%d" % (x, y))

    # click coords with Selenium (may not always work)
    # elem = driver.execute_script("""
    # return document.elementFromPoint(arguments[0], arguments[1]);
    # """, x, y)
    # elem.click()


def get_screenshot(driver):
    temp_file = tempfile.NamedTemporaryFile()
    driver.get_screenshot_as_file(temp_file.name)
    return cv2.imread(temp_file.name)


def get_coordinates_pattern(img_rgb, pattern):
    w, h = pattern.shape[:-1]
    res = cv2.matchTemplate(img_rgb, pattern, cv2.TM_CCOEFF_NORMED)
    threshold = .8
    loc = np.where(res >= threshold)
    points = zip(*loc[::-1])
    if not points:
        return None
    elif len(points) > 1:
        logging.warning("Several occurrences are found, using the first among them.")
    pt = points[0]
    x, y = (pt[0] + w / 2.0, pt[1] + h / 2.0)
    return x, y


def main(url, img):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    img_rgb = get_screenshot(driver)
    pattern = cv2.imread(img)
    coords = get_coordinates_pattern(img_rgb, pattern)
    if coords is None:
        logging.error("Image isn't found.")
        return
    driver_click(driver, coords[0], coords[1])

    # give time for chrome to react
    import time
    time.sleep(5)

    driver.get_screenshot_as_file("result.png")
    logging.info("Result saved to result.png")

    driver.close()
    driver.quit()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    main(args.url, args.img)
