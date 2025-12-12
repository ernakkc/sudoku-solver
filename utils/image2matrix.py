from google import genai
from google.genai import types
from configparser import ConfigParser



def with_gemini(API_KEY: str, image_path: str):
    image_bytes = open(image_path, "rb").read()

    client = genai.Client(api_key=API_KEY)
    response = client.models.generate_content( 
        model='gemini-2.5-flash',
        contents=[
        types.Part.from_bytes(
            data=image_bytes,
            mime_type='image/png',
        ),
        'Give me sudoku matrix. Represent the empty cells with 0. Respond only with the matrix in list format without any explanation.'
        ],
    )
    output = response.text
    cleaned_output = output.replace('```json', '').replace('```', '').strip()
    matrix = []
    for i, line in enumerate(cleaned_output.splitlines()):
        if line == '[' or line == ']':
            continue
        matrix.append([])
        line = line.replace(' ',"").replace('[', '').replace(']', '')
        for num in line.split(','):
            if num:
                matrix[-1].append(int(num))
    return matrix










if __name__ == "__main__":
    config = ConfigParser()
    config.read('config.ini')
    API_KEY = config.get('GENAI', 'API_KEY')
    image_path = "sudoku_examples/sudoku1.png"
    matrix = with_gemini(API_KEY, image_path)
    for row in matrix:
        print(row)
    print("Done")
