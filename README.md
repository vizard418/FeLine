## FeLine - A command-line client for AI models.
![banner](img/banner.png)

### Introduction
FeLine is a command-line tool that lets you interact with a language model in a powerful way: it allows you to include the output of terminal (Bash) commands directly in your conversations. Imagine getting real-time system information, analyzing data, running scripts, and more — all within a natural conversation.

### Install
1. Pre-requisites
- Get your API key on the Google Studio platform
[aistudio](https://aistudio.google.com/app/apikey)

- Install the Python 3 version corresponding to your operative system.
[python](https://www.python.org/downloads/)


2. Download the project:
```bash
# Using curl
sudo rm -rf /opt/FeLine && \
curl -L -o FeLine.zip https://github.com/vizard418/FeLine/archive/refs/heads/main.zip && \
sudo unzip FeLine.zip -d /opt/ && \
sudo mv /opt/FeLine-main /opt/FeLine && \
rm FeLine.zip
```

```powershell
# Powershell
Invoke-WebRequest -Uri "https://github.com/vizard418/FeLine/archive/refs/heads/main.zip" -OutFile "FeLine.zip"; Expand-Archive -Path "FeLine.zip" -DestinationPath "Feline" -Force; Remove-Item "FeLine.zip"
```

3. Create a Python virtual environment:
- Install the `virtualenv` package for Python 3 using pip. If you encounter issues on Linux, you can alternatively try your distribution's package manager.
```shell
python3 -m pip install virtualenv
cd FeLine
python3 -m virtualenv .venv
```

- Activate enviroment & install dependendences:
```bash
# On Unix-based systems
source .venv/bin/activate && \
python -m pip install -r requirements.txt && \
deactivate
```

```powershell
# On Windows
.venv\Scripts\activate
python -m pip install -r requirements.txt
deactivate
```

4. Add to PATH.
- On Unix-based systems, add the following lines to your shell configuration file. (`~/.bashrc`, `~/.profile`, `~/.bash_profile`)
```bash
# FeLine (A command-line AI agent)
export GEMINI_API_KEY="[YourApiKey]"
export PATH="$PATH:/opt/FeLine"
```
- *[Important]* Reload config 
```bash
source ~/.bashrc
```

- On Windows, you need to modify the environment variables to add the project folder path. For example: `C:\Program Files\FeLine`.


### Basic usage:
The most basic FeLine command is to enter interactive chat mode with: `feline -i`
Or you can also view help with the *--help* flag: `feline --help`


### How to use `$` in feline for images and shell commands:
`feline` utilizes the `$` symbol for special instructions within your prompts.  Here's how to use it:

*   **For Image Processing:**  Use `$[path/to/your/image.jpg]` or `$[path/to/your/image.png]` (or any supported image format) to instruct `FeLine` to process the image.  Replace `path/to/your/image.jpg` with the actual path to your image file.  For example:
```bash
feline -i
  FeLine - Imagination is the only limit
► Current LLM model: gemini-2.5-flash-lite

  [User] **Press Return 2 times to exit**
$> Describe this image: $[/home/user/pictures/my_cat.jpg]
$>
```

* **Sinlge-Line Command Prompts**
    - On Unix-based systems (exec `cat` command): `feline.sh "Summarize the key statements from my notes. $(cat notes.md)"`
    - On Windows CMD (exec `type` command): `feline "Summarize the key statements from my notes. $(type notes.md)"`)


* **For Shell Command Execution:** Use `$()` around your shell command. This lets `FeLine` execute the shell command and use its output as context for the prompt. For example:
    - On Unix-based systems: `feline "Summarize the output of the ls -l $(ls -l)" -i`
    - Windows CMD (`dir` command): `feline "Summarize the output of dir /a $(dir /a)"`

```markdown
  [FeLine]
The output shows a detailed listing of the user's home directory contents, including: ...
---
```
**Important Notes:** Be careful with potentially destructive shell commands. Ensure you trust the prompt and the commands you are executing.

### Run feline. Examples:
- Text comprehension: (`feline -i`)
```markdown
  [User] **Press Return 2 times to exit**
$> How does AI work
$>
  [FeLine]
AI, or Artificial Intelligence, is a vast and complex field, but at its core, it's about building computer systems that can perform tasks that typically require human intelligence...
---
```

- Complex tasks: (`feline --model gemini-flash -i` or `feline --model gemini-pro -i`)
```markdown
  [User] **Press Return 2 times to exit**
$> Explains the relationship between climate change and human migration, highlighting both direct and indirect causes, and offers concrete examples from vulnerable regions.
$>
  [FeLine]
## Climate Change and Human Migration: A Complex Relationship
Climate change is increasingly recognized as a significant driver of human migration, influencing both the frequency and scale of population movements globally. This relationship is multifaceted, involving direct impacts of climate-related hazards and indirect consequences that exacerbate existing vulnerabilities and trigger displacement...
---
```

- Image recognition: (`feline -i` or `feline --model {model_keyword} -it`)
```markdown
  [User] **Press Return 2 times to exit**
$> How many animals do you see in the image? $[/home/user/downloads/animals.jpg]
$>
  [FeLine]
I can see 8 animals in the image:
*   Giraffe
*   Lion
*   Zebra
*   Ostrich
*   Elephant
*   Tiger
*   Rhinoceros
---
```

- Extra utils: Can run shell commands: (`feline -it` or `feline --model {model_keyword}` or `feline Translate me into Klingon '$(man chmod)'`)
```markdown
  [User] **Press Return 2 times to exit**
$> Translate me into Klingon $(man chmod)
$>
  [FeLine]
Sure! I'll translate the "chmod" manual into Klingon. It's a challenge, since Klingon is more concise and practical than English or Spanish. Here it is, with its interpretation. I've included some words that might not be directly translatable, with clarifications...
```
