import dspy
from html.parser import HTMLParser

# 1. Clase validadora de HTML
class HTMLValidator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.errors = []
    
    def handle_starttag(self, tag, attrs):
        allowed_tags = ["html", "title", "meta", "head", "body", "div", "a", "button", "nav", "ul", "li"]
        if tag not in allowed_tags:
            self.errors.append(f"Etiqueta no permitida: {tag}")
    
    def is_valid(self):
        return len(self.errors) == 0

# 2. Métrica actualizada (¡corrección clave!)
def html_validador(example, prediction, trace=None):  # <-- Añade trace=None
    validador = HTMLValidator()
    try:
        validador.feed(prediction.html)
        return 1.0 if validador.is_valid() else 0.0
    except Exception as e:
        print(f"Error de validación: {e}")
        return 0.0

# 3. Ejemplos de entrenamiento
ejemplos = [
    dspy.Example(
        description="Un botón rojo con texto grande",
        html='<button class="bg-red-500 text-white text-xl p-2 rounded">Click</button>'
    ).with_inputs('description'),
    
    dspy.Example(
        description="Una barra de navegación con enlaces",
        html='<nav class="bg-gray-800 p-4"><a href="#" class="text-white">Home</a></nav>'
    ).with_inputs('description')
]

# 4. Firma y módulo
class GenerateHTML(dspy.Signature):
    description = dspy.InputField()
    html = dspy.OutputField()

class HTMLGenerator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.generate = dspy.Predict(GenerateHTML)
    
    def forward(self, description):
        return self.generate(description=description)

# 5. Configuración actualizada (¡nuevo formato DSPy 2.5!)
turbo = dspy.LM("openai/gpt-4o-mini", api_key="INSERT YOUR API KEY HERE")  # <-- Usa dspy.LM
dspy.configure(lm=turbo)

# 6. Compilación y ejecución
teleprompter = dspy.BootstrapFewShot(metric=html_validador)
compiled_generator = teleprompter.compile(HTMLGenerator(), trainset=ejemplos)

if __name__ == "__main__":
    user_input = input("Describe el elemento HTML: ")
    prediction = compiled_generator(description=user_input)
    print("HTML generado:", prediction.html)