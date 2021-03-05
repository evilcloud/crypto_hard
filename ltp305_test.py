import sys
import time
from ltp305 import LTP305

fmt = "%M"
address = 0x61
available = {
    "hour": "%H",
    "minute": "%M",
    "second": "%S",
}

if len(sys.argv) > 1:
    try:
        fmt = available[sys.argv[1]]
    except KeyError:
        raise ValueError("{} is not supported".format(sys.argv[1]))

if len(sys.argv) > 2:
    address = int(sys.argv[2], 16)
    if address not in [0x61, 0x62, 0x63]:
        raise ValueError(
            "Invalid i2c address: 0x{:02x}. Run `i2c-detect -y 1` to discover breakouts.".format(
                address
            )
        )

try:
    display = LTP305(address=address)
    display.clear()
    display.show()
except OSError:
    raise OSError(
        "Unable to find LTP305 on i2c address: 0x{:02x}. Run `i2c-detect -y 1 to disvover breakouts`".format(
            address
        )
    )

while True:
    minute = time.strftime(fmt)
    left, right = minute
    display.set_charachter(0, left)
    display.set_charachter(1, right)
    display.show()
    time.sleep(1.0 / 60)