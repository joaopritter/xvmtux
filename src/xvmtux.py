from textual import on, work
from textual.screen import Screen
from textual.containers import Horizontal, Vertical
from textual.app import ComposeResult, App
from textual.widgets import (
    Button,
    Header,
    OptionList,
    Log,
    Static,
    Input,
)
from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError
from xvm_tools import generate_xvm
import time

WRITE_CHARACTERISTIC_UUID = "0000ff01-0000-1000-8000-00805f9b34fb"
READ_CHARACTERISTIC_UUID = "0000ff01-0000-1000-8000-00805f9b34fb"
NOTIFY_CHARACTERISTIC_UUID = "0000ff01-0000-1000-8000-00805f9b34fb"


class Xvmtux(Screen):
    CSS_PATH = "xvmtux.tcss"
    devices = {}
    current_device_name = None
    current_device_address = ""
    client: BleakClient = None

    def compose(self) -> ComposeResult:
        yield Static(
            "ERROR: NO DEVICE FOUND, TURN ON BLUETOOTH AND REFRESH", id="error_box"
        )
        with Horizontal(id="main_screen"):
            yield Header()
            with Vertical(id="device_tab"):
                yield Static("Devices", id="device_header")
                yield OptionList(id="device_list")
                yield Button("Refresh", id="refresh_button")
            with Vertical(id="messages"):
                yield Log(id="message_log", auto_scroll=True)
                yield Input(placeholder="Input message")

    def on_mount(self):
        error = self.query_one("#error_box")
        error.visible = False
        self.update_device_list()

    @work
    async def update_device_list(self) -> None:
        error = self.query_one("#error_box")
        error.visible = False
        options = self.query_one(OptionList)
        options.clear_options()
        # message_logger = self.query_one(Log)
        try:
            device_list = await BleakScanner.discover()
            for device in device_list:
                if device.name and "VIRTEC" in device.name:
                    self.devices[device.name] = device.address
                    options.add_option(device.name.replace('"', ""))
                    # message_logger.write_line(f"{device.name} - {device.address}")
        except BleakError:
            error.visible = True

    @on(Button.Pressed, "#refresh_button")
    async def refresh_devices(self) -> None:
        self.update_device_list()

    @on(OptionList.OptionSelected, "#device_list")
    async def on_device_selected(self, event: OptionList.OptionSelected) -> None:
        selected_device = event.option.prompt
        if selected_device:
            for dev, add in self.devices.items():
                if selected_device in dev:
                    self.current_device_address = add
                    self.current_device_name = str(selected_device)
            # message_logger = self.query_one("#message_log")
            # message_logger.write_line(self.current_device_name)
            # message_logger.write_line(self.current_device_address)
            self.messaging_service()

    @on(Input.Submitted)
    async def on_message_submit(self, message_input: Input) -> None:
        message_logger = self.query_one("#message_log")
        user_input = message_input.value

        if user_input.strip():
            message_logger.write_line(f"\nMessage submitted: {user_input}")
            if '"' in self.current_device_name:
                copid = self.current_device_name.replace('"', "").split("_")[-1]
            else:
                copid = self.current_device_name.split("_")[-1]
            xvm = generate_xvm(copid, "8000", user_input)
            command_bytes = xvm.encode()

            try:
                if self.client.is_connected:
                    await self.client.write_gatt_char(
                        WRITE_CHARACTERISTIC_UUID, command_bytes
                    )
                else:
                    message_logger.write_line("Device is not connected!")
            except Exception as e:
                message_logger.write_line(f"Failed to send command: {e}")
        else:
            message_logger.write_line("No message entered.")

    @work
    async def messaging_service(self):
        if self.client:
            if self.client.is_connected:
                await self.client.disconnect()
                time.sleep(2)

        message_logger = self.query_one("#message_log")

        try:
            self.client = BleakClient(self.current_device_address)
            connected = await self.client.connect()

            if connected:
                message_logger.write_line(
                    f"\n{'-'*10} Connected to {self.current_device_name} {'-'*10}"
                )

                await self.client.start_notify(
                    NOTIFY_CHARACTERISTIC_UUID, self.notification_handler
                )

            else:
                message_logger.write_line(
                    f"Failed to connect to {self.current_device_name}"
                )

        except Exception as e:
            message_logger.write_line(f"\nError during connection: {e}")

    async def notification_handler(self, sender, data) -> None:
        message_logger = self.query_one("#message_log")
        message_logger.write_line(f"\n>> Reply: {data.decode()}")


class LoggerApp(App):
    def on_mount(self):
        self.title = "XVMTUX"
        self.push_screen(Xvmtux())


app = LoggerApp()

if __name__ == "__main__":
    app.run()
