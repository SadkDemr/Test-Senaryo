PS C:\OtomasyoTool> Remove-Item -Recurse -Force C:\OtomasyoTool\backend\venv
PS C:\OtomasyoTool> py -3.11 -m venv C:\OtomasyoTool\backend\venv
PS C:\OtomasyoTool>

(venv) C:\OtomasyoTool\backend>pip install -r C:\OtomasyoTool\backend\requirements.txt
Requirement already satisfied: fastapi>=0.104.1 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from -r C:\OtomasyoTool\backend\requirements.txt (line 2)) (0.137.1)
Requirement already satisfied: uvicorn>=0.24.0 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from uvicorn[standard]>=0.24.0->-r C:\OtomasyoTool\backend\requirements.txt (line 3)) (0.49.0)
Requirement already satisfied: python-multipart>=0.0.6 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from -r C:\OtomasyoTool\backend\requirements.txt (line 4)) (0.0.32)
Requirement already satisfied: pydantic>=2.5.2 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from pydantic[email]>=2.5.2->-r C:\OtomasyoTool\backend\requirements.txt (line 5)) (2.13.4)
Requirement already satisfied: sqlalchemy>=2.0.23 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from -r C:\OtomasyoTool\backend\requirements.txt (line 8)) (2.0.51)
Requirement already satisfied: python-jose>=3.3.0 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from python-jose[cryptography]>=3.3.0->-r C:\OtomasyoTool\backend\requirements.txt (line 11)) (3.5.0)
Requirement already satisfied: bcrypt>=4.0.0 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from -r C:\OtomasyoTool\backend\requirements.txt (line 12)) (5.0.0)
Requirement already satisfied: selenium>=4.15.2 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from -r C:\OtomasyoTool\backend\requirements.txt (line 15)) (4.45.0)
Requirement already satisfied: webdriver-manager>=4.0.1 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from -r C:\OtomasyoTool\backend\requirements.txt (line 16)) (4.1.2)
Requirement already satisfied: Appium-Python-Client>=3.1.0 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from -r C:\OtomasyoTool\backend\requirements.txt (line 19)) (5.3.1)
Requirement already satisfied: requests>=2.31.0 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from -r C:\OtomasyoTool\backend\requirements.txt (line 22)) (2.34.2)
Requirement already satisfied: httpx>=0.24.0 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from -r C:\OtomasyoTool\backend\requirements.txt (line 23)) (0.28.1)
Requirement already satisfied: openpyxl>=3.1.2 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from -r C:\OtomasyoTool\backend\requirements.txt (line 26)) (3.1.5)
Requirement already satisfied: pandas>=2.2.0 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from -r C:\OtomasyoTool\backend\requirements.txt (line 27)) (3.0.3)
Requirement already satisfied: starlette>=0.46.0 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from fastapi>=0.104.1->-r C:\OtomasyoTool\backend\requirements.txt (line 2)) (1.3.1)
Requirement already satisfied: typing-extensions>=4.8.0 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from fastapi>=0.104.1->-r C:\OtomasyoTool\backend\requirements.txt (line 2)) (4.15.0)
Requirement already satisfied: typing-inspection>=0.4.2 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from fastapi>=0.104.1->-r C:\OtomasyoTool\backend\requirements.txt (line 2)) (0.4.2)
Requirement already satisfied: annotated-doc>=0.0.2 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from fastapi>=0.104.1->-r C:\OtomasyoTool\backend\requirements.txt (line 2)) (0.0.4)
Requirement already satisfied: click>=7.0 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from uvicorn>=0.24.0->uvicorn[standard]>=0.24.0->-r C:\OtomasyoTool\backend\requirements.txt (line 3)) (8.4.1)
Requirement already satisfied: h11>=0.8 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from uvicorn>=0.24.0->uvicorn[standard]>=0.24.0->-r C:\OtomasyoTool\backend\requirements.txt (line 3)) (0.16.0)
Requirement already satisfied: annotated-types>=0.6.0 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from pydantic>=2.5.2->pydantic[email]>=2.5.2->-r C:\OtomasyoTool\backend\requirements.txt (line 5)) (0.7.0)
Requirement already satisfied: pydantic-core==2.46.4 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from pydantic>=2.5.2->pydantic[email]>=2.5.2->-r C:\OtomasyoTool\backend\requirements.txt (line 5)) (2.46.4)
Requirement already satisfied: greenlet>=1 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from sqlalchemy>=2.0.23->-r C:\OtomasyoTool\backend\requirements.txt (line 8)) (3.5.1)
Requirement already satisfied: ecdsa!=0.15 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from python-jose>=3.3.0->python-jose[cryptography]>=3.3.0->-r C:\OtomasyoTool\backend\requirements.txt (line 11)) (0.19.2)
Requirement already satisfied: rsa!=4.1.1,!=4.4,<5.0,>=4.0 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from python-jose>=3.3.0->python-jose[cryptography]>=3.3.0->-r C:\OtomasyoTool\backend\requirements.txt (line 11)) (4.9.1)
Requirement already satisfied: pyasn1>=0.5.0 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from python-jose>=3.3.0->python-jose[cryptography]>=3.3.0->-r C:\OtomasyoTool\backend\requirements.txt (line 11)) (0.6.3)
Requirement already satisfied: certifi>=2026.2.25 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from selenium>=4.15.2->-r C:\OtomasyoTool\backend\requirements.txt (line 15)) (2026.5.20)
Requirement already satisfied: trio<1.0,>=0.31.0 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from selenium>=4.15.2->-r C:\OtomasyoTool\backend\requirements.txt (line 15)) (0.33.0)
Requirement already satisfied: trio-websocket<1.0,>=0.12.2 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from selenium>=4.15.2->-r C:\OtomasyoTool\backend\requirements.txt (line 15)) (0.12.2)
Requirement already satisfied: urllib3<3.0,>=2.6.3 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from urllib3[socks]<3.0,>=2.6.3->selenium>=4.15.2->-r C:\OtomasyoTool\backend\requirements.txt (line 15)) (2.7.0)
Requirement already satisfied: websocket-client<2.0,>=1.8.0 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from selenium>=4.15.2->-r C:\OtomasyoTool\backend\requirements.txt (line 15)) (1.9.0)
Requirement already satisfied: attrs>=23.2.0 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from trio<1.0,>=0.31.0->selenium>=4.15.2->-r C:\OtomasyoTool\backend\requirements.txt (line 15)) (26.1.0)
Requirement already satisfied: sortedcontainers in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from trio<1.0,>=0.31.0->selenium>=4.15.2->-r C:\OtomasyoTool\backend\requirements.txt (line 15)) (2.4.0)
Requirement already satisfied: idna in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from trio<1.0,>=0.31.0->selenium>=4.15.2->-r C:\OtomasyoTool\backend\requirements.txt (line 15)) (3.18)
Requirement already satisfied: outcome in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from trio<1.0,>=0.31.0->selenium>=4.15.2->-r C:\OtomasyoTool\backend\requirements.txt (line 15)) (1.3.0.post0)
Requirement already satisfied: sniffio>=1.3.0 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from trio<1.0,>=0.31.0->selenium>=4.15.2->-r C:\OtomasyoTool\backend\requirements.txt (line 15)) (1.3.1)
Requirement already satisfied: cffi>=1.14 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from trio<1.0,>=0.31.0->selenium>=4.15.2->-r C:\OtomasyoTool\backend\requirements.txt (line 15)) (2.0.0)
Requirement already satisfied: wsproto>=0.14 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from trio-websocket<1.0,>=0.12.2->selenium>=4.15.2->-r C:\OtomasyoTool\backend\requirements.txt (line 15)) (1.3.2)
Requirement already satisfied: pysocks!=1.5.7,<2.0,>=1.5.6 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from urllib3[socks]<3.0,>=2.6.3->selenium>=4.15.2->-r C:\OtomasyoTool\backend\requirements.txt (line 15)) (1.7.1)
Requirement already satisfied: python-dotenv in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from webdriver-manager>=4.0.1->-r C:\OtomasyoTool\backend\requirements.txt (line 16)) (1.2.2)
Requirement already satisfied: packaging in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from webdriver-manager>=4.0.1->-r C:\OtomasyoTool\backend\requirements.txt (line 16)) (26.2)
Requirement already satisfied: charset_normalizer<4,>=2 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from requests>=2.31.0->-r C:\OtomasyoTool\backend\requirements.txt (line 22)) (3.4.7)
Requirement already satisfied: anyio in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from httpx>=0.24.0->-r C:\OtomasyoTool\backend\requirements.txt (line 23)) (4.14.0)
Requirement already satisfied: httpcore==1.* in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from httpx>=0.24.0->-r C:\OtomasyoTool\backend\requirements.txt (line 23)) (1.0.9)
Requirement already satisfied: et-xmlfile in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from openpyxl>=3.1.2->-r C:\OtomasyoTool\backend\requirements.txt (line 26)) (2.0.0)
Requirement already satisfied: numpy>=2.3.3 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from pandas>=2.2.0->-r C:\OtomasyoTool\backend\requirements.txt (line 27)) (2.4.6)
Requirement already satisfied: python-dateutil>=2.8.2 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from pandas>=2.2.0->-r C:\OtomasyoTool\backend\requirements.txt (line 27)) (2.9.0.post0)
Requirement already satisfied: tzdata in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from pandas>=2.2.0->-r C:\OtomasyoTool\backend\requirements.txt (line 27)) (2026.2)
Requirement already satisfied: pycparser in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from cffi>=1.14->trio<1.0,>=0.31.0->selenium>=4.15.2->-r C:\OtomasyoTool\backend\requirements.txt (line 15)) (3.0)
Requirement already satisfied: colorama in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from click>=7.0->uvicorn>=0.24.0->uvicorn[standard]>=0.24.0->-r C:\OtomasyoTool\backend\requirements.txt (line 3)) (0.4.6)
Requirement already satisfied: six>=1.9.0 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from ecdsa!=0.15->python-jose>=3.3.0->python-jose[cryptography]>=3.3.0->-r C:\OtomasyoTool\backend\requirements.txt (line 11)) (1.17.0)
Requirement already satisfied: email-validator>=2.0.0 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from pydantic[email]>=2.5.2->-r C:\OtomasyoTool\backend\requirements.txt (line 5)) (2.3.0)
Requirement already satisfied: dnspython>=2.0.0 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from email-validator>=2.0.0->pydantic[email]>=2.5.2->-r C:\OtomasyoTool\backend\requirements.txt (line 5)) (2.8.0)
Requirement already satisfied: cryptography>=3.4.0 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from python-jose[cryptography]>=3.3.0->-r C:\OtomasyoTool\backend\requirements.txt (line 11)) (49.0.0)
Requirement already satisfied: httptools>=0.8.0 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from uvicorn[standard]>=0.24.0->-r C:\OtomasyoTool\backend\requirements.txt (line 3)) (0.8.0)
Requirement already satisfied: pyyaml>=5.1 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from uvicorn[standard]>=0.24.0->-r C:\OtomasyoTool\backend\requirements.txt (line 3)) (6.0.3)
Requirement already satisfied: watchfiles>=0.20 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from uvicorn[standard]>=0.24.0->-r C:\OtomasyoTool\backend\requirements.txt (line 3)) (1.2.0)
Requirement already satisfied: websockets>=10.4 in C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages (from uvicorn[standard]>=0.24.0->-r C:\OtomasyoTool\backend\requirements.txt (line 3)) (16.0)

(venv) C:\OtomasyoTool\backend>python -c "import pywinauto; print('OK')"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import pywinauto; print('OK')
    ^^^^^^^^^^^^^^^^
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\pywinauto\__init__.py", line 89, in <module>
    from . import findwindows
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\pywinauto\findwindows.py", line 42, in <module>
    from . import controls
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\pywinauto\controls\__init__.py", line 36, in <module>
    from . import uiawrapper # register "uia" back-end (at the end of uiawrapper module)
    ^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\pywinauto\controls\uiawrapper.py", line
 42, in <module>
    from .. import backend
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\pywinauto\backend.py", line 35, in <module>
    from .base_wrapper import BaseWrapper
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\pywinauto\base_wrapper.py", line 46
    except (ImportError, OSError):
                                  ^
IndentationError: unindent does not match any outer indentation level

(venv) C:\OtomasyoTool\backend>python -c "import pywin32; print('OK')"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import pywin32; print('OK')
    ^^^^^^^^^^^^^^
ModuleNotFoundError: No module named 'pywin32'

(venv) C:\OtomasyoTool\backend>
