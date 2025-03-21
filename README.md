# BaronPay

A simple self service point of sale kiosk webapp, using python Django as its backend.

![Example](https://github.com/lonk42/BaronPay/blobl/baronpay_example.png?raw=true)

## Card Scanning

Baronpay is designed to be used with a partnering RFID card reader. Generic card readers often function as simple USB HID devices, outputting a string of characters when reading a card. Baron pay uses a hidden text input field to catch this text input and use it.
