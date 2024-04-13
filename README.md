# langchain-Q-A-with-RAG

### How to setup
- Clone the repository:
    ```sh
    git clone https://github.com/berrytern/langchain-Q-A-with-RAG.git
    cd langchain-Q-A-with-RAG
    ```
- Create a virtual environment and activate it:
    ```sh
    python -m venv dev_env # Create virtual environment
    . dev_env/bin/activate # Activate the virtual environment
    ```
- Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
### Usage

- Obtain API keys:
    - Follow the tutorial on this [link](https://www.maisieai.com/help/how-to-get-an-openai-api-key-for-chatgpt)

- Update configuration:
    - Copy the .env.example file to .env
    - Add your ChatOpenApi API key to .env file.
    - Edit the pdf path and the question on .env file.

- Run the :
    ```sh
    python qa_pdf.py
    ```