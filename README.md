INFO:     10.10.9.195:62216 - "POST /api/ai-gen/scenarios HTTP/1.1" 500 Internal Server Error
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "C:\OtomasyoTool\backend\venv\Lib\site-packages\uvicorn\protocols\http\httptools_impl.py", line 421, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\OtomasyoTool\backend\venv\Lib\site-packages\uvicorn\middleware\proxy_headers.py", line 62, in __call__
    return await self.app(scope, receive, send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\OtomasyoTool\backend\venv\Lib\site-packages\fastapi\applications.py", line 1162, in __call__
    await super().__call__(scope, receive, send)
  File "C:\OtomasyoTool\backend\venv\Lib\site-packages\starlette\applications.py", line 90, in __call__
    await self.middleware_stack(scope, receive, send)
  File "C:\OtomasyoTool\backend\venv\Lib\site-packages\starlette\middleware\errors.py", line 186, in __call__
    raise exc
  File "C:\OtomasyoTool\backend\venv\Lib\site-packages\starlette\middleware\errors.py", line 164, in __call__
    await self.app(scope, receive, _send)
  File "C:\OtomasyoTool\backend\venv\Lib\site-packages\starlette\middleware\cors.py", line 96, in __call__
    await self.simple_response(scope, receive, send, request_headers=headers)
  File "C:\OtomasyoTool\backend\venv\Lib\site-packages\starlette\middleware\cors.py", line 154, in simple_response
    await self.app(scope, receive, send)
  File "C:\OtomasyoTool\backend\venv\Lib\site-packages\starlette\middleware\exceptions.py", line 63, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "C:\OtomasyoTool\backend\venv\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "C:\OtomasyoTool\backend\venv\Lib\site-packages\starlette\_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "C:\OtomasyoTool\backend\venv\Lib\site-packages\fastapi\middleware\asyncexitstack.py", line 18, in __call__
    await self.app(scope, receive, send)
  File "C:\OtomasyoTool\backend\venv\Lib\site-packages\starlette\routing.py", line 660, in __call__
    await self.middleware_stack(scope, receive, send)
  File "C:\OtomasyoTool\backend\venv\Lib\site-packages\starlette\routing.py", line 680, in app
    await route.handle(scope, receive, send)
  File "C:\OtomasyoTool\backend\venv\Lib\site-packages\fastapi\routing.py", line 1609, in handle
    await self.original_router.handle(scope, receive, send)
  File "C:\OtomasyoTool\backend\venv\Lib\site-packages\fastapi\routing.py", line 2047, in handle
    await included_router._handle_selected(scope, receive, send)
  File "C:\OtomasyoTool\backend\venv\Lib\site-packages\fastapi\routing.py", line 1629, in _handle_selected
    await original_route.handle(scope, receive, send)
  File "C:\OtomasyoTool\backend\venv\Lib\site-packages\fastapi\routing.py", line 1218, in handle
    await app(scope, receive, send)
  File "C:\OtomasyoTool\backend\venv\Lib\site-packages\fastapi\routing.py", line 143, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "C:\OtomasyoTool\backend\venv\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "C:\OtomasyoTool\backend\venv\Lib\site-packages\starlette\_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "C:\OtomasyoTool\backend\venv\Lib\site-packages\fastapi\routing.py", line 129, in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
  File "C:\OtomasyoTool\backend\venv\Lib\site-packages\fastapi\routing.py", line 683, in app
    raw_response = await run_endpoint_function(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\OtomasyoTool\backend\venv\Lib\site-packages\fastapi\routing.py", line 337, in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\OtomasyoTool\backend\routers\ai_test_generator_router.py", line 2998, in save_scenario
    committed = git_service.commit_changes(
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\OtomasyoTool\backend\services\git_service.py", line 327, in commit_changes
    raise GitError(f"Commit failed: {stderr}")
services.git_service.GitError: Commit failed: Committer identity unknown

*** Please tell me who you are.

Run

  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"

to set your account's default identity.
Omit --global to set the identity only in this repository.

fatal: unable to auto-detect email address (got 'kftte@WindowsVm.(none)')

WARNING:  WatchFiles detected changes in 'workspaces\1\test-senaryo\ai_scenarios\BOA\script.py'. Reloading...
