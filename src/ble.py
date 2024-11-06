from typing import Union
from bleak import BleakScanner, BleakClient, BLEDevice
import asyncio


class BleClient:
    device_connection: BleakClient = None

    def __init__(self):
        self.found_devices: list[BLEDevice | None] = []
        self.target_devices: Union[BLEDevice, None] = None

    async def discover(self, filter: Union[str, None] = None) -> None:
        query_devices = await BleakScanner.discover()
        if query_devices:
            if filter:
                for device in query_devices:
                    if filter in device.name:
                        self.found_devices.append(device)
            else:
                for device in query_devices:
                    self.found_devices.append(device)

    async def connect(self, address: str) -> BleakClient:
        if (
            not BleClient.device_connection
            or not BleClient.device_connection.is_connected
        ):
            client = BleakClient(address)
            await client.connect()
            BleClient.device_connection = client
            return BleClient.device_connection
        else:
            return BleClient.device_connection

    def tuple_names(self) -> tuple[str, ...]:
        names = []
        for device in self.found_devices:
            names.append(device.name)
        return tuple(names)


if __name__ == "__main__":
    from textual.widgets import OptionList

    OptionList()

    ble = BleClient()
    asyncio.run(ble.discover("VIRTEC"))
    print(ble.tuple_names())
