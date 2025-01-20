import dspy
from html.parser import HTMLParser

# Clase para validar el HTML generado
class HTMLValidator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.errors = []

    def handle_starttag(self, tag, attrs): # Método para manejar las etiquetas de inicio
        if tag not in ["html", "title", "meta", "link", "head", "body", "div", "a", "button"]:
            self.errors.append(f"Invalid start tag: {tag}")

    def handle_endtag(self, tag): # Método para manejar las etiquetas de cierre
        if tag not in ["html", "title", "head", "body", "div", "a", "button"]:
            self.errors.append(f"Invalid end tag: {tag}")

    def handle_startendtag(self, tag, attrs):
        if tag not in ["br", "img"]: # Etiquetas que pueden ser auto-cerr
            self.errors.append(f"Invalid self-closing tag: {tag}")

    def error_message(self):
        if self.errors:
            return "\n".join(self.errors)
        return "No errors found in the generated HTML."


# Configuración del modelo OpenAI
lm = dspy.LM("openai/gpt-4o-mini", api_key="INSERT YOUR API KEY HERE") # Insertar la clave de la API

# Configurar el modelo dspy con el modelo de lenguaje
dspy.configure(lm=lm)

# Función para generar HTML con Tailwind CSS
def generate_html_with_tailwind(user_description):
    """
    Usa dspy.LM para interpretar instrucciones del usuario y generar HTML con Tailwind CSS.
    """

    # Se agregan mas ejemplos para que el modelo pueda entender mejor las instrucciones
    prompt = """
    You are an assistant that generates HTML elements styled with Tailwind CSS. 
    The user will describe a component, and you will respond with the corresponding HTML code. 
    Always include only the necessary HTML for the element, unless explicitly asked to generate a full document.

    Examples:

    1. User: I want a navbar with links.
    Assistant:
    <nav class="bg-gray-800 p-4">
        <ul class="flex space-x-4">
            <li><a href="#" class="text-white hover:text-gray-400">Home</a></li>
            <li><a href="#" class="text-white hover:text-gray-400">About</a></li>
            <li><a href="#" class="text-white hover:text-gray-400">Contact</a></li>
        </ul>
    </nav>

    2. User: I need a button with a red background.
    Assistant:
    <button class="bg-red-500 text-white font-semibold py-2 px-4 rounded hover:bg-red-600">
        Click Me
    </button>

    3. User: I want a card with a title and an image.
    Assistant:
    <div class="max-w-sm rounded overflow-hidden shadow-lg">
        <img class="w-full" src="https://via.placeholder.com/150" alt="Card image">
        <div class="px-6 py-4">
            <div class="font-bold text-xl mb-2">Card Title</div>
        </div>
    </div>
    """
    
    # Usar el modelo configurado para generar la respuesta
    response = lm(
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_description}
        ]
    )

    # Devolver el contenido generado
    return response[0]

# Interacción del usuario
if __name__ == "__main__":
    print("Describe the HTML element you need (e.g., 'I want a navbar with links').")
    user_input = input("Your description: ")

    # Generar el HTML
    generated_html = generate_html_with_tailwind(user_input)

    # Validar el HTML generado
    validator = HTMLValidator()
    validator.feed(generated_html)
    validation_result = validator.error_message()

    # Mostrar el resultado
    if validation_result == "No errors found in the generated HTML.":
        print("\nGenerated HTML is valid!")
        print("HTML:")
        print(generated_html)
    else:
        print("\nGenerated HTML has errors:")
        print(validation_result)
        print("HTML:")
        print(generated_html)
