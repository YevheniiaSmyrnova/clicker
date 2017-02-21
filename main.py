from selenium import webdriver
import subprocess
import cv2
import numpy as np
import tempfile


def driver_click(driver, x, y, default_y_offset=96):
    position = driver.get_window_position()
    x += position['x']
    # need to take into account offset by y that is a constant
    y += position['y'] + default_y_offset
    subprocess.call(["xdotool", "mousemove", str(x), str(y)])
    subprocess.call(["xdotool", "click", "1"])


def get_screenshot(driver):
    temp_file = tempfile.NamedTemporaryFile()
    driver.get_screenshot_as_file(temp_file.name)
    return cv2.imread(temp_file.name)


def get_coordinates_pattern(img_rgb, pattern):
    w, h = pattern.shape[:-1]
    res = cv2.matchTemplate(img_rgb, pattern, cv2.TM_CCOEFF_NORMED)
    threshold = .8
    loc = np.where(res >= threshold)
    pt = zip(*loc[::-1])[0]
    x, y = (pt[0] + w / 2.0, pt[1] - h / 2.0)
    return x, y


def main():
    driver = webdriver.Firefox()
    driver.get("https://www.youtube.com/watch?v=ys5hmBkyvag")
    img_rgb = get_screenshot(driver)
    pattern = cv2.imread('pattern.png')
    x, y = get_coordinates_pattern(img_rgb, pattern)
    driver_click(driver, x, y)
    driver.close()
    # driver.quit()


if __name__ == '__main__':
    main()
