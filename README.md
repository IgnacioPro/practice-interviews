# SRE Learning Tool

A spaced repetition system designed for learning Site Reliability Engineering (SRE) concepts and tools.

## Features

- Multiple choice questions about SRE, DevOps, and related tools
- Self-assessment mode for more focused learning
- Spaced repetition algorithm (SuperMemo 2) for optimal learning intervals
- Progress saving and loading
- Graceful exit handling

## Installation

1. Clone the repository:

git clone https://github.com/yourusername/sre-learning-tool.git
cd sre-learning-tool

2. Install dependencies:

pip install -r requirements.txt

3. Run the script:

python main.py

## Usage

- The script will prompt you to choose between learning mode and self-assessment mode.
- In learning mode, you will be presented with questions and can choose to answer them or skip them.
- In self-assessment mode, you will be asked to rate your knowledge on a scale of 1 to 5 after each question.


## State Saving

The program automatically saves your progress in `estado_preguntas.json`, tracking:

- Question difficulty (EF - Ease Factor)
- Review intervals
- Next review time

## Controls

- Enter the number corresponding to your answer
- Type 'q' at any prompt to quit
- Press Ctrl+C to exit gracefully
- Type 's' to continue after a round, or any other key to exit

## Adding New Questions

Create or modify `preguntas.json` following this format:

```json
{
    "id": 1,
    "pregunta": "Your question here?",
    "opciones": [
        "Option 1",
        "Option 2",
        "Option 3"
    ],
    "respuesta_correcta": 0
}
```
Note: `respuesta_correcta` is zero-based (0 = first option).

## Contributing

1. Fork the repository
2. Create your feature branch (git checkout -b feature/AmazingFeature)
3. Commit your changes (git commit -m 'Add some AmazingFeature')
4. Push to the branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

## Acknowledgments

- SuperMemo 2 algorithm for spaced repetition
- SRE community for question content and best practices
