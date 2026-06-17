
INFO:     127.0.0.1:56849 - "POST /api/admin/repositories HTTP/1.1" 307 Temporary Redirect
INFO:     127.0.0.1:56849 - "POST /api/admin/repositories/ HTTP/1.1" 500 Internal Server Error
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\sqlalchemy\engine\base.py", line 1969, in _exec_single_context
    self.dialect.do_execute(
    ~~~~~~~~~~~~~~~~~~~~~~~^
        cursor, str_statement, effective_parameters, context
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\sqlalchemy\engine\default.py", line 952, in do_execute
    cursor.execute(statement, parameters)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
sqlite3.OperationalError: no such column: repositories.editor_type

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\uvicorn\protocols\http\httptools_impl.py", line 421, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        self.scope, self.receive, self.send
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\uvicorn\middleware\proxy_headers.py", line 62, in __call__
    return await self.app(scope, receive, send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\fastapi\applications.py", line 1162, in __call__
    await super().__call__(scope, receive, send)
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\starlette\applications.py", line 90, in __call__
    await self.middleware_stack(scope, receive, send)
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\starlette\middleware\errors.py", line 186, in __call__
    raise exc
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\starlette\middleware\errors.py", line 164, in __call__
    await self.app(scope, receive, _send)
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\starlette\middleware\cors.py", line 96, in __call__
    await self.simple_response(scope, receive, send, request_headers=headers)
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\starlette\middleware\cors.py", line 154, in simple_response
    await self.app(scope, receive, send)
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\starlette\middleware\exceptions.py", line 63, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\starlette\_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\fastapi\middleware\asyncexitstack.py", line 18, in __call__
    await self.app(scope, receive, send)
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\starlette\routing.py", line 660, in __call__
    await self.middleware_stack(scope, receive, send)
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\starlette\routing.py", line 680, in app
    await route.handle(scope, receive, send)
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\fastapi\routing.py", line 1609, in handle
    await self.original_router.handle(scope, receive, send)
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\fastapi\routing.py", line 2047, in handle
    await included_router._handle_selected(scope, receive, send)
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\fastapi\routing.py", line 1629, in _handle_selected
    await original_route.handle(scope, receive, send)
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\fastapi\routing.py", line 1218, in handle
    await app(scope, receive, send)
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\fastapi\routing.py", line 143, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\starlette\_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\fastapi\routing.py", line 129, in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\fastapi\routing.py", line 683, in app
    raw_response = await run_endpoint_function(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<3 lines>...
    )
    ^
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\fastapi\routing.py", line 337, in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\OtomasyoTool\backend\routers\admin_repositories_router.py", line 89, in create_repository
    existing = db.query(Repository).filter_by(name=body.name).first()
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\sqlalchemy\orm\query.py", line 2766, in first
    return self.limit(1)._iter().first()  # type: ignore
           ~~~~~~~~~~~~~~~~~~~^^
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\sqlalchemy\orm\query.py", line 2864, in _iter
    result: Union[ScalarResult[_T], Result[_T]] = self.session.execute(
                                                  ~~~~~~~~~~~~~~~~~~~~^
        statement,
        ^^^^^^^^^^
        params,
        ^^^^^^^
        execution_options={"_sa_orm_load_options": self.load_options},
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\sqlalchemy\orm\session.py", line 2373, in execute
    return self._execute_internal(
           ~~~~~~~~~~~~~~~~~~~~~~^
        statement,
        ^^^^^^^^^^
    ...<4 lines>...
        _add_event=_add_event,
        ^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\sqlalchemy\orm\session.py", line 2271, in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
                          ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        self,
        ^^^^^
    ...<4 lines>...
        conn,
        ^^^^^
    )
    ^
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\sqlalchemy\orm\context.py", line 306, in orm_execute_statement
    result = conn.execute(
        statement, params or {}, execution_options=execution_options
    )
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\sqlalchemy\engine\base.py", line 1421, in execute
    return meth(
        self,
        distilled_parameters,
        execution_options or NO_OPTIONS,
    )
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\sqlalchemy\sql\elements.py", line 526, in _execute_on_connection
    return connection._execute_clauseelement(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        self, distilled_params, execution_options
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\sqlalchemy\engine\base.py", line 1643, in _execute_clauseelement
    ret = self._execute_context(
        dialect,
    ...<8 lines>...
        cache_hit=cache_hit,
    )
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\sqlalchemy\engine\base.py", line 1848, in _execute_context
    return self._exec_single_context(
           ~~~~~~~~~~~~~~~~~~~~~~~~~^
        dialect, context, statement, parameters
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\sqlalchemy\engine\base.py", line 1988, in _exec_single_context
    self._handle_dbapi_exception(
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        e, str_statement, effective_parameters, cursor, context
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\sqlalchemy\engine\base.py", line 2365, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\sqlalchemy\engine\base.py", line 1969, in _exec_single_context
    self.dialect.do_execute(
    ~~~~~~~~~~~~~~~~~~~~~~~^
        cursor, str_statement, effective_parameters, context
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\sqlalchemy\engine\default.py", line 952, in do_execute
    cursor.execute(statement, parameters)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such column: repositories.editor_type
[SQL: SELECT repositories.id AS repositories_id, repositories.name AS repositories_name, repositories.repo_url AS repositories_repo_url, repositories.repo_type AS repositories_repo_type, repositories.description AS repositories_description, repositories.editor_type AS repositories_editor_type, repositories.provider AS repositories_provider, repositories.git_username AS repositories_git_username, repositories.git_token AS repositories_git_token, repositories.created_by AS repositories_created_by, repositories.created_at AS repositories_created_at, repositories.updated_at AS repositories_updated_at
FROM repositories
WHERE repositories.name = ?
 LIMIT ? OFFSET ?]
[parameters: ('Repo', 1, 0)]
(Background on this error at: https://sqlalche.me/e/20/e3q8)

# Test Automation Scenarios

Bu repository 5 adet test senaryosu içermektedir.

## Senaryolar

`scenarios/` klasöründe JSON formatında saklanmaktadır.

### Senaryo Formatı

```json
{
  "id": 1,
  "name": "Senaryo Adı",
  "description": "Açıklama",
  "type": "web|mobile|desktop",
  "natural_steps": ["Adım 1", "Adım 2"],
  "steps_json": {},
  "config_json": {},
  "tags": ["tag1", "tag2"]
}
```

Son güncelleme: 2026-02-03 11:55:24 UTC
