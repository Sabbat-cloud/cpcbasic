Modernización del IDE de Amstrad CPC BASIC
Esta es mi propuesta para actualizar el IDE con las características que has pedido.

User Review Required
IMPORTANT

Sobre la pantalla gráfica (Pygame embebido en Tkinter):
El problema de que "se pierde el control" en programas interactivos ocurre porque, en Windows, cuando incrustamos la ventana de Pygame dentro de un panel de Tkinter (usando SDL_WINDOWID), Pygame pierde la capacidad de leer el teclado. El sistema operativo envía las pulsaciones de teclas a Tkinter en lugar de a Pygame, por lo que comandos como INKEY dejan de funcionar.
Solución propuesta: Eliminar el marco embebido negro del IDE y hacer que al pulsar "Ejecutar", el emulador se abra de forma nativa en su propia ventana flotante. Esto garantiza que Pygame tenga el 100% del control del teclado y la gráfica, permitiendo juegos y programas interactivos reales. El IDE quedará como un editor de código puro a pantalla completa o dividida.

Proposed Changes
IDE (ide.py)
[MODIFY] ide.py
Resaltado de Sintaxis: Implementaré un coloreador automático en el ScrolledText. Crearemos etiquetas (tags) para colorear palabras clave (azul), números (naranja), cadenas de texto (verde) y comentarios (gris). Esto se actualizará automáticamente cada vez que modifiques el código.
Desvincular Pygame: Quitaré la variable env['SDL_WINDOWID'] al lanzar el proceso, permitiendo que la gráfica se abra correctamente con control total de teclado e interactividad.
Menú de Herramientas (Chuletas): Añadiré un nuevo menú "Herramientas" en la barra superior con las siguientes ventanas emergentes (Toplevel):
Paleta de Colores: Una ventana interactiva mostrando los 27 colores de la paleta de Amstrad con su número de código para usarlos en INK y PAPER.
Tabla ASCII: Una lista rápida de los caracteres imprimibles y de control.
Guía de Coordenadas: Un esquema visual/texto explicando el sistema de coordenadas de Locomotive BASIC (0-640, 0-400), el origen abajo a la izquierda y las resoluciones de MODE 0, 1, 2.
Verification Plan
Manual Verification
Abrir el IDE y pegar un programa. Verificar que las palabras clave (PRINT, LOCATE, FOR, etc.) cambian de color automáticamente.
Ejecutar un programa interactivo con INKEY (como el del cursor XOR) y confirmar que ahora el teclado sí responde perfectamente.
Abrir las ventanas de ayuda desde el menú superior y comprobar que la información es útil y se muestra bien.
