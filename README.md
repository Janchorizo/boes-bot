# boes-bot
A Telegram bot implementation for exposing BOE information.

## Cómo está organizado
El paquete telegram implementa un wrapper alrededor de la api HTTP para que sea más cómodo recibir y mandar mensajes.

Hay siete módulos en total, de los cuales varios son sólo para uso interno:
- `telegram.base` Provee la clase base _Method_ que se usa en _method_factory_ para crear funciones HTTP automáticamente.
- `telegram.methods` Tiene una lista de _telegram.base.MethodDesc_ que se pasa a _telegram.base.method_factory_ para crear
   cada llamada HTTP. De esta forma, todas las llamadas HTTP de la API se pueden hacer con este módulo:
   ```python
   from telegram import methods
   
   # Para descargar un documento (max 20MB)
   params = {'file_id': id_del_documento}
   status, file = methods.getFile(token, params=params, verbose=True)
   ```
   Todas las llamadas a peticiciones HTTP tienen el parámetro opcional verbose para que imprima todo por consola.
- `telegram.types` Los updates se pasan como una de estas clases. Esto permite que puedas hacer:
   ```
   from telegram import types
   
   update.type == types.ChosenInlineResult
   ```
- Las llamadas usando `telegram.methods` son un poco coñazo de usar. Por eso hay cuatro módulos que son los que realmente
  están pensados para usarse:
    - `telegram.admin` Provee una serie de utilidades para gestionar el bot. Lo más útil es la clase `Webhook` para usar la conexión
      por webhooks con un _context manager_. Cuando se termina el código de ese bloque, el webhook se quita sólo, así sólo está
      puesto mientras tengas el bot activo.
      ```python
      with admin.Webhook(token, url, max_connections, drop_pending_updates=True) as wb:
        app = crear_tu_app(token)
        app.run()
      ```
    - `telegram.chat` Son utilidades relacionadas con la gestión de chats: cambiar la desc, banear personas, pinnear mensajes, ...
    - `telegram.content` Tiene tres funciones relacionadas con contenido: obtener imágenes de perfil, documentos y actualizaciones.
       También tiene la clase `Update`; getUpdates o las llamadas por webhook mandan una respuesta HTTP al bot, y Update se usa para
       que sea más cómodo comparar el tipo y el contenido.
    - `telegram.messages` Es el módulo que más chicha tiene. En vez de tener funciones con muchos argumentos, son clases: heredan de
       `Content` o `ReplacementContent` en función de si es contenido que se envía o un contenido que se sobreescribe. La forma de usarlo
       es de la siguiente manera:
       ```python
       # creas el contenido que quieres mandar; en este caso con los parámetros opcionales parse_mode para que puedas usar negrita
       # en el texto.
       msg = messages.MessageContent(text=global_options_text, parse_mode='MarkdownV2')
       
       # una vez instanciado se puede enviar tantas veces se quiera
       msg.send(token, chat_id)
       
       # y como cualquier otra petición HTTP, puedes usarlo de forma verbosa:
       msg.send(token, chat_id, verbose=True)
       ```

## ¿Cómo se usaría?
Bien porque tengas una API y uses webhook o bien porque llames a getUpdates y recibas una respuesta HTTP, vas a terminar con un
cuerpo JSON serializado. Parseas el body usando `json.loads` e instancias `telegram.content.Update` con el diccionario que te da. _También puedes usar directamente Update.fromraw(el_cuerpo_de_la_respuesta_sin_decodificar)_.

Un objeto _Update_ tiene un atributo _content_ con toda la info de la llamada al bot. Es del tipo que tenga `update.type`, y se usa como un diccionario.
Adicionalmente, si el update es de tipo `CallbackQuery` o `Message` también tiene un atributo _cid_ que el código del chat; porque el resto de updates
no van asociadas a un chat y no son para responder a una persona:
> Por ejemplo `InlineQuery` es una actualización que usas para implementar búsqueda en el teclado, es lo que te permite buscar emojis: el usuario escribe
> en el teclado se le manda un `InlineQuery` al bot para que devuelva opciones, así puedes picar en un resultado y enviarlo. Por eso no puedes contestar
> perse.

Entonces, **¿Cómo respondo a un mensaje?** Fácil:

1. Recibes el mensaje y creas el objeto update con el cuerpo que te mandan.
2. Creas (o usas un mensaje que ya tengas) el mensaje.
3. Envías el mensaje al mimso chat: `msg.send(token, update.content.cid)`
