<div align="center">

# 🐈 FeLine

### ⚡ Tu terminal, potenciada por modelos de lenguaje

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![CLI](https://img.shields.io/badge/Interface-CLI-222222?logo=windowsterminal&logoColor=white)](#uso)
[![LLM](https://img.shields.io/badge/Powered%20by-LLMs-7C3AED)](#características)
[![License](https://img.shields.io/badge/License-See%20repository-lightgrey)](#licencia)

*Combina comandos del sistema con la capacidad de análisis de un LLM, directamente desde la línea de comandos.*

</div>

---

**FeLine** es un cliente minimalista de modelos de lenguaje (LLM) para la terminal. Permite enviar consultas a modelos compatibles, mantener conversaciones guardadas y enriquecer los prompts con la salida de comandos del sistema.

Su característica más útil es combinar el razonamiento de un LLM con información actual de tu entorno: por ejemplo, ejecutar comandos para inspeccionar logs, consultar procesos o revisar el estado de servicios y pedirle al modelo que interprete los resultados. Los comandos se ejecutan en tu sistema local, así que revisa siempre lo que incluyes en el prompt antes de enviarlo.

## 🎯 ¿Para qué sirve?

| 🧩 Caso de uso | 💡 Qué puedes hacer |
| --- | --- |
| 📜 **Logs** | Resumir errores, agrupar fallos y detectar patrones en registros. |
| 🖥️ **Diagnóstico** | Interpretar procesos, memoria, disco y servicios. |
| 🧑‍💻 **Desarrollo** | Revisar diffs, explicar comandos y proponer pruebas. |
| 🔍 **Investigación** | Reunir la salida de herramientas locales y pedir un análisis contextual. |

## ✨ Características

- Consultas puntuales desde la línea de comandos.
- Sesiones interactivas.
- Historial de entrada y conversaciones persistentes.
- Reanudación y consulta de chats guardados.
- Selección de modelos y configuración de un modelo predeterminado.
- Inserción de la salida de comandos del sistema mediante `@cmd(...)` o `@command(...)`.
- Soporte configurado para modelos Gemini y modelos compatibles con la API de OpenAI a través del endpoint de Groq.

## 📋 Requisitos

- Python 3.10 o superior.
- Git.
- Una clave API válida para el proveedor del modelo elegido:
  - `GEMINI_API_KEY` para modelos Gemini.
  - `OPENAI_API_KEY` para los modelos de la familia OpenAI/Groq configurados en `models.ini`.

## 🚀 Instalación

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/vizard418/FeLine.git
cd FeLine
```

### 2️⃣ Crear y activar el entorno virtual

Instala `virtualenv` si todavía no lo tienes:

```bash
python -m pip install --user virtualenv
```

Crea el entorno llamado `env`:

```bash
virtualenv env
```

Actívalo según tu sistema:

**Linux / macOS**
```bash
source env/bin/activate
```

**Windows (CMD o PowerShell)**
```powershell
.\env\Scripts\activate
```

**Windows con Git Bash**
```bash
source env/Scripts/activate
```

### 3️⃣ Instalar las dependencias

Con el entorno virtual activado:

```bash
python -m pip install -e .
```

### 4️⃣ Configurar la clave API

FeLine lee la clave API desde una variable de entorno. Configura la variable correspondiente al proveedor que vayas a usar.

**Linux / macOS (sesión actual)**

Para Gemini:
```bash
export GEMINI_API_KEY="tu_clave_api"
```

Para modelos OpenAI/Groq:
```bash
export OPENAI_API_KEY="tu_clave_api"
```

**Windows PowerShell (sesión actual)**

Para Gemini:
```powershell
$env:GEMINI_API_KEY = "tu_clave_api"
```

Para modelos OpenAI/Groq:
```powershell
$env:OPENAI_API_KEY = "tu_clave_api"
```

Si quieres que la variable esté disponible en futuras sesiones, configúrala en el entorno de tu sistema o en el archivo de inicio de tu shell. No escribas la clave directamente en el código ni la subas al repositorio.

### 5️⃣ Agregar FeLine al `PATH`

El lanzador `feline` activa automáticamente el entorno virtual `env` ubicado dentro del directorio del proyecto. Para poder ejecutarlo desde cualquier directorio, agrega la ruta absoluta al directorio de FeLine a tu `PATH`.

**Linux / macOS (sesión actual)**

Reemplaza `/ruta/a/FeLine` por la ruta real del repositorio:

```bash
export PATH="/ruta/a/FeLine:$PATH"
```

Para hacerlo permanente, añade esa línea al archivo de inicio de tu shell, por ejemplo `~/.bashrc` o `~/.zshrc`, y abre una nueva terminal.

**Windows**
- Agrega la ruta absoluta del repositorio a la variable de entorno `Path`.
- En CMD o PowerShell puedes ejecutar el lanzador `feline.bat` desde el directorio del proyecto. Si quieres invocarlo desde cualquier ubicación, asegúrate de que la carpeta del proyecto esté en `Path`.

Abre una terminal nueva o recarga la configuración de la shell después de cambiar el `PATH`.

### 6️⃣ Configurar el modelo predeterminado

Lista los modelos disponibles:

```bash
feline --show-models
```

Configura el modelo predeterminado con `--model-config`:

```bash
feline --model-config gemini-lite
```

Otros identificadores disponibles en la configuración incluida son:

- `gemini-lite`
- `gemini-flash`
- `gemini-pro`
- `gpt-oss-120b`
- `gpt-oss-20b`

Puedes elegir otro modelo para una única consulta con `--model`, sin cambiar el predeterminado:

```bash
feline --model gemini-pro "Explica la diferencia entre un proceso y un hilo."
```

## 💻 Uso

### 💬 Consulta puntual

Pasa el prompt como argumento:

```bash
feline "Explica que hace el comando awk y muestra tres ejemplos."
```

### 🗨️ Chat interactivo

Inicia una sesión interactiva:

```bash
feline --interactive
```

Escribe tu consulta y envíala. Para terminar, envía una entrada vacía dos veces.

### 🔗 Combinar un prompt con comandos del sistema

FeLine reconoce referencias `@cmd(...)` y `@command(...)` en el texto. Ejecuta el comando local e incorpora su salida al prompt antes de enviarlo al modelo.

**Analizar logs recientes de un servicio**

```bash
feline "Analiza estos errores y agrupa las causas probables. Sugiere pasos de diagnostico, sin ejecutar acciones correctivas: @cmd(tail -n 100 /var/log/syslog)"
```

**Investigar errores en un archivo de log**

```bash
feline "Resume los errores por tipo, identifica patrones y señala las marcas de tiempo relevantes: @cmd(grep -iE 'error|failed|critical' /var/log/myapp.log | tail -n 80)"
```

**Revisar recursos del sistema**

```bash
feline "Interpreta el uso de CPU y memoria. Indica que procesos conviene investigar y por que: @cmd(ps aux --sort=-%mem | head -n 15)"
```

**Consultar el espacio en disco**

```bash
feline "Analiza el uso de disco, destaca los puntos de montaje con poco espacio y propone verificaciones seguras: @cmd(df -h)"
```

**Examinar servicios fallidos con systemd**

```bash
feline "Resume los servicios fallidos y sugiere como diagnosticar cada uno. No asumas la causa sin evidencia: @cmd(systemctl --failed --no-pager)"
```

**Analizar cambios en un repositorio**

```bash
feline "Resume los cambios, identifica posibles riesgos y sugiere pruebas relevantes: @cmd(git diff --stat)"
```

> ⚠️ **Nota:** los comandos anteriores son ejemplos para sistemas Unix/Linux. Adapta las rutas y comandos a tu sistema operativo. En Windows, utiliza comandos disponibles en la shell que ejecuta FeLine.

### 🧠 Elegir un modelo para una consulta

```bash
feline --model gemini-flash "Compara estas dos estrategias de cache y explica sus trade-offs."
```

### 📚 Ver los modelos disponibles

```bash
feline --show-models
```

### 🗂️ Ver conversaciones guardadas

```bash
feline --show-chats
```

### 🔎 Mostrar los mensajes de una conversación

Usa el identificador que aparece en `--show-chats`:

```bash
feline --show-chat 1
```

### ▶️ Reanudar una conversación

```bash
feline --resume-chat 1
```

### 🧹 Limpiar el historial local y los chats

```bash
feline --purge
```

🗑️ **Atención:** `--purge` borra el historial de entrada y los registros de conversaciones almacenados localmente. No se puede deshacer.

## 🧰 Opciones de línea de comandos

| Opción | Descripción |
| --- | --- |
| `message` | Texto de la consulta, opcional. |
| `--interactive` | Inicia una sesión interactiva. |
| `--model NAME` | Usa un modelo disponible para esa ejecución. |
| `--model-config NAME` | Cambia el modelo predeterminado. |
| `--show-models` | Muestra los modelos disponibles. |
| `--show-chats` | Lista las conversaciones guardadas. |
| `--show-chat ID` | Muestra los mensajes de una conversación. |
| `--resume-chat ID` | Reanuda una conversación guardada. |
| `--purge` | Borra el historial local y los registros de chats. |
| `--help` | Muestra la ayuda. |

Consulta todas las opciones con:

```bash
feline --help
```

## ⚙️ Cómo funciona la inserción de comandos

Cuando FeLine encuentra una expresión como:

```text
@cmd(comando)
```

ejecuta el comando en la máquina local e inserta su salida en el prompt. También acepta `@command(comando)`. La ejecución tiene un tiempo límite de 30 segundos y la salida estándar y los errores del comando se combinan.

⚠️ **Importante:** las referencias a comandos ejecutan shell local con los permisos de tu usuario. No incluyas comandos destructivos ni prompts con comandos que no hayas revisado. Evita pasar secretos, tokens, datos personales o logs sensibles a un proveedor externo. Para logs grandes, filtra y limita la salida antes de enviarla.

## 🗃️ Configuración y datos locales

FeLine crea archivos de configuración y datos de usuario según el sistema operativo, entre ellos la base de datos de conversaciones y el historial de entrada. El archivo `config/models.ini` del repositorio define los alias de modelos disponibles; la configuración de usuario puede copiarse a una ubicación específica del sistema.

## 🛠️ Solución de problemas

- **No se encuentra `feline`:** comprueba que la carpeta del proyecto esté en `PATH` y abre una terminal nueva.
- **No se encuentra el entorno virtual:** verifica que exista `env` dentro del directorio del proyecto y que hayas creado el entorno con ese nombre.
- **Error de autenticación:** comprueba que definiste la variable correcta (`GEMINI_API_KEY` u `OPENAI_API_KEY`) para el modelo seleccionado.
- **Modelo no disponible:** ejecuta `feline --show-models` y utiliza exactamente uno de los alias listados.
- **El comando integrado falla:** ejecuta el comando por separado en la misma shell para verificar su sintaxis, permisos y disponibilidad.

## 📄 Licencia

Consulta la licencia del repositorio para conocer los términos de uso y distribución.
