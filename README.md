# XVMTUX

<h1 align="center">
  <br>
  <img src="https://raw.githubusercontent.com/joaopritter/xvmtux/refs/heads/main/assets/xvmtux_screen.png">
  <br>
</h1>

## About

Application focused on Unix systems to connect to VIRLOC8 devices through BLE via a TUI,
built using Textual and Bleak.

Use the `setup.sh` file to install it to the user path and to update it.

## Sobre

Aplicação focada em sistemas Unix para conectar com dispositivos VIRLOC8 por BLE através
de uma TUI, construído usando Textual e Bleak.

Utilize o arquivo `setup.sh` para instalar a aplicação no path do usuário
e realizar atualizações.

### Shortcuts

To enable command shortcuts, on the application files create a JSON with the following format
inside the program files folder:

Para habilitar atalhos de comandos na aplicação, crie um JSON com o seguinte formato na
pasta dos arquivos do programa:
```
{
  "Speed 0": ">SCT64 0<",
  "Speed 60": ">SCT64 60999<",
  "RPM 0": ">SCT27 0<",
  "RPM 1200": ">SCT27 1200<"
}
```
