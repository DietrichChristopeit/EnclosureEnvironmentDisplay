"""
main.py
"""
import micropython
from dht import DHT11
import st7789
from st7789 import ST7789
import tft_config
import utime
import vga1_bold_16x32 as datafont
import vga2_16x16 as sectionfont
from machine import Pin, SPI
from time import sleep


def displayText(display: ST7789, text: str, font) -> None:
    length = len(text)
    display.text(
        font,
        text,
        display.width() // 2 - length // 2 * font.WIDTH,
        display.height() // 2 - font.HEIGHT,
        st7789.WHITE,
        st7789.RED)
    return


def displayTiles(display: ST7789) -> None:
    display.text(sectionfont, "temp: C", 0, 0)
    display.text(sectionfont, "hum: %", 0, 121)
    display.hline(0, 120, 240, st7789.WHITE)
    return


def main() -> None:
    """main loop"""

    sensorPin: Pin = Pin(13, Pin.IN)
    sensor: DHT11 = DHT11(sensorPin)
    spi: SPI = SPI(2, baudrate=40000000, polarity=1, sck=Pin(18), mosi=Pin(23))
    display: ST7789 = ST7789(spi, 240, 240, reset=Pin(4, Pin.OUT), dc=Pin(2, Pin.OUT), backlight=Pin(10, Pin.OUT), rotation=1)
    display.init()
    display.off()
    displayTiles(display)
    sleep(2)
    display.on()
    last_measure: (int, float) = (0, 0.00)

    while True:
        sensor.measure()
        t, h = sensor.temperature(), sensor.humidity()
        if last_measure[0] != t:
            display.text(datafont, str(t), 0, 17)
        if last_measure[1] != h:
            display.text(datafont, str(h), 0, 139)
        last_measure = (t, h)
        sleep(2)
    return


if __name__ == '__main__':
    main()
