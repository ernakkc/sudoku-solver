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
        """You are analyzing a preprocessed Sudoku puzzle image. Extract the 9x9 grid.

CRITICAL FORMATTING REQUIREMENTS:
- Each row MUST be on a separate line
- Use integers 1-9 for filled cells, 0 for empty cells
- Output exactly 9 rows, each containing exactly 9 integers
- NO markdown, NO code blocks, NO explanations
- Start with [[ and end with ]]

EXACT OUTPUT FORMAT (each row on new line):
[[5,3,0,0,7,0,0,0,0],
[6,0,0,1,9,5,0,0,0],
[0,9,8,0,0,0,0,6,0],
[8,0,0,0,6,0,0,0,3],
[4,0,0,8,0,3,0,0,1],
[7,0,0,0,2,0,0,0,6],
[0,6,0,0,0,0,2,8,0],
[0,0,0,4,1,9,0,0,5],
[0,0,0,0,8,0,0,7,9]]

Respond with this format only, no other text."""
        ],
    )
    output = response.text
    cleaned_output = output.replace('```json', '').replace('```python', '').replace('```', '').strip()
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
