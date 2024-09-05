# LLM-dockerizing
Aim for making module for LLM API docker image

## folder structure
```bash
llama_api/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── models.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── chat_service.py
│   │   └── pdf_service.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
│
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_chat_service.py
│   └── test_pdf_service.py
│
├── .env
├── .gitignore
├── requirements.txt
├── Dockerfile
└── README.md
```

- `main.py`:
    - Initializes the FastAPI application and includes the router.
    - Imports settings from `config.py`.

- `routes.py`:
    - Defines API endpoints.
    - Receives user requests and forwards them to appropriate services.
    - Utilizes `chat_service.py` and `pdf_service.py`.
    - Uses Pydantic models from `models.py` to validate input data.

- `chat_service.py`:
    - Communicates with the OpenAI API to provide chat functionality.
    - Retrieves API key and settings from `config.py`.

- `pdf_service.py`:
    - Processes and summarizes PDF files.
    - Uses `chat_service.py` for text summarization.

- `config.py`:
    - Manages project-wide settings.
    - Loads environment variables and provides settings to other modules.

- `models.py`:
    - Defines data models for API requests and responses.

## Data Flow

1. User sends an API request (chat message or PDF file).
2. `routes.py` receives the request and forwards it to the appropriate service.
3. Chat requests are handled by `chat_service.py`, while PDF requests are processed by `pdf_service.py`.
4. `chat_service.py` communicates with the OpenAI API to generate responses.
5. `pdf_service.py` processes PDFs and uses `chat_service.py` for summarization when needed.
6. Processed results are returned to the user through `routes.py`.

This structure ensures that each component has clear responsibilities and that data flows logically, enhancing the modularity and maintainability of the code.

``` mermaid
graph TD
    A[main.py] --> B[routes.py]
    B --> C[chat_service.py]
    B --> D[pdf_service.py]
    C --> E[OpenAI API]
    D --> C
    F[config.py] --> A
    F --> C
    F --> D
    G[models.py] --> B
    H[User Request] --> B
    I[PDF File] --> B
    B --> J[API Response]
```
