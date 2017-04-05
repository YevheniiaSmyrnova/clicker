from selenium import webdriver
import subprocess
import cv2
import numpy as np
import tempfile
import argparse
import logging
import imutils


def driver_click(driver, x, y, default_x_offset, default_y_offset):

    # more broot force click coords via X11 automation tool
    # this doesn't work with tightvnc though
    position = driver.get_window_position()
    x += position['x'] + default_x_offset
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


def get_coordinates_pattern(img_rgb, pattern, proportion_img_x, proportion_img_y):
    startX, startY, endX, endY = find_image(img_rgb, pattern)
    w = (endX - startX) / 2.0
    h = (endY - startY) / 2.0
    print (startX, startY, endX, endY)
    x, y = (startX + proportion_img_x * w, startY + proportion_img_y * h)
    return x, y


def find_image(img_rgb, pattern):
    template = cv2.cvtColor(pattern, cv2.COLOR_BGR2GRAY)
    template = cv2.Canny(template, 50, 200)
    (tH, tW) = template.shape[:2]

    gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    found = None
    for scale in np.linspace(0.2, 5.0, 100)[::-1]:
        resized = imutils.resize(gray, width=int(gray.shape[1] * scale))
        r = gray.shape[1] / float(resized.shape[1])

        if resized.shape[0] < tH or resized.shape[1] < tW:
            break

        edged = cv2.Canny(resized, 50, 200)
        result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

        if found is None or maxVal > found[0]:
            found = (maxVal, maxLoc, r)

    (_, maxLoc, r) = found
    (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
    (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))
    return startX, startY, endX, endY


def main(url, img, default_x_offset, default_y_offset, proportion_img_x, proportion_img_y, delay):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    img_rgb = get_screenshot(driver)
    pattern = cv2.imread(img)
    coords = get_coordinates_pattern(img_rgb, pattern, proportion_img_x, proportion_img_y)
    if coords is None:
        logging.error("Image isn't found.")
        return
    driver_click(driver, coords[0], coords[1], default_x_offset, default_y_offset)

    # give time for chrome to react
    import time
    time.sleep(delay)

    driver.get_screenshot_as_file("result.png")
    logging.info("Result saved to result.png")

    driver.close()
    driver.quit()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="URL to the page")
    parser.add_argument("img", help="path to the image")
    parser.add_argument("--default_x_offset",
                        help="offset on x",
                        default=0,
                        type=float)
    parser.add_argument("--default_y_offset",
                        help="offset on y",
                        default=66,
                        type=float)
    parser.add_argument("--proportion_img_x",
                        help="proportional offset factor of the image on x",
                        default=0.5,
                        type=float)
    parser.add_argument("--proportion_img_y",
                        help="proportional offset factor of the image on y",
                        default=0.5,
                        type=float)
    parser.add_argument("--delay",
                        help="how long it waits after performing the action",
                        default=5,
                        type=float)
    args = parser.parse_args()
    main(args.url, args.img, args.default_x_offset, args.default_y_offset,
         args.proportion_img_x, args.proportion_img_y, args.delay)
