#! /usr/bin/python
# coding: utf-8


import time
from subprocess import call, check_output

STATUS = 2
PERCENT = 3


class BatteryStatus(object):
    def __init__(self):
        self.under_10 = False
        self.under_5 = False
        self.charging = False

    def check_battery_life(self):
        list_output = check_output('acpi').decode().replace(',', '').split(' ')
        status = list_output[STATUS].replace(',', '')
        percent = int(list_output[PERCENT].replace('%', ''))

        if status == 'Charging':
            self.under_10 = False
            self.under_5 = False

            if percent == 100:
                call(['notify-send', 'Battery Status', '{}%'.format(percent)])

            if not self.charging:
                self.charging = True
                call(['notify-send', 'Battery Status', 'Charging {}%'.format(percent)])

        else:
            self.charging = False

            if percent < 10 and not self.under_10:
                self.under_10 = True
                call(['notify-send', 'Battery Status', '{}%'.format(percent), '--icon=notification-battery-low'])

            if percent < 5 and not self.under_5:
                self.under_5 = True
                call(['notify-send', 'Battery Status', '{}%'.format(percent), '--icon=notification-power'])


if __name__ == '__main__':
    bs = BatteryStatus()
    while(True):
        bs.check_battery_life()
        time.sleep(60)
