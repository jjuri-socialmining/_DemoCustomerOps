# tools/

Herramientas de apoyo del repo. Se invocan desde la raíz.

---

## `gate_page.py` — dejar una página detrás de una clave

Cifra el contenido de una página y la publica detrás de una portada con clave.
Pensado para el material que vive en `web/` y se sirve por GitHub Pages, donde
todo lo que se sube queda al alcance de cualquiera que tenga el link.

```bash
python3 tools/gate_page.py web/informe/index.html --password 6511
```

**Lo que hace, y por qué no es un `prompt()` de JavaScript.** El HTML resultante
**sólo transporta texto cifrado**: sin la clave no hay nada legible en el código
fuente. Una pantalla que tapa el contenido no sirve de nada en una página
estática — se abre el inspector y ahí está todo.

| | |
|---|---|
| Cifrado | AES-256-GCM |
| Derivación de clave | PBKDF2-SHA256, 600.000 iteraciones, salt aleatorio por página |
| Descifrado | Web Crypto, en el navegador de quien entra. Sin red, sin servidor |

Antes de escribir el archivo, la herramienta **descifra su propio resultado** y
comprueba dos cosas: que el contenido vuelve con esa clave, y que no quedó texto
en claro. Si algo de eso falla, aborta y no escribe nada.

### Opciones

| | |
|---|---|
| `-p, --password` | la clave (obligatoria) |
| `-o, --out` | salida; por defecto sobrescribe el archivo de entrada |
| `--attach ARCHIVO.pdf` | incrusta un PDF **dentro** del contenido cifrado |
| `--attach-label` | texto del botón de descarga |
| `--eyebrow`, `--heading`, `--prompt`, `--title` | textos de la portada |
| `--iterations` | iteraciones de PBKDF2 (por defecto 600.000) |

La portada hereda el `<style>` de la página, así que mantiene su identidad
visual. Si la página no trae estilos, usa una paleta neutra propia.

### El adjunto va adentro, no al lado

```bash
python3 tools/gate_page.py web/caso/index.html -p "Laso-2026" \
  --attach informe.pdf --attach-label "Descargar informe"
```

Un PDF publicado junto a la página vive en una URL adivinable y **deja la puerta
sin sentido**. Con `--attach` el archivo viaja dentro del paquete cifrado y el
botón de descarga aparece recién después de la clave.

### ⚠️ La fuerza la da la clave, no el algoritmo

Cuatro dígitos son diez mil combinaciones y se recorren con un script; las
600.000 iteraciones lo hacen lento, no imposible. Eso **frena al que llega de
casualidad, no al que va a buscar**. Para material sensible, una frase como
`6511-Laso-2026` cambia el orden de magnitud del problema. La herramienta avisa
cuando la clave tiene menos de 8 caracteres.

Y una obviedad que conviene dejar escrita: la clave se manda por otro canal, no
en el mismo mensaje que el link.

**Requiere:** `pip install cryptography`

---

## `watermark_pdf.py` — sello de agua en un PDF

Estampa un sello diagonal en todas las páginas.

```bash
python3 tools/watermark_pdf.py entrada.pdf [salida.pdf] --text "BORRADOR CONFIDENCIAL"
```

Sin salida, sobrescribe la entrada mediante un archivo temporal.
**Requiere:** PyMuPDF (`import fitz`).

---

## `visit-tracker/`

Registro de visitas de las páginas publicadas. Ver su propio directorio.
