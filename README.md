This is a small Python structured-text extraction utility. Its principal workflow accepts text and a Pydantic schema, asks Groq for JSON matching that schema, then validates the response into a model instance. The available schemas cover emails, invoices, and resumes. The runtime is concentrated in extractor.py; no README documentation was provided, so the map reflects the excerpted implementation only.

Directory structure:
└── ayushadhikari15-messy-text-to-json/
    ├── extractor.py
    ├── requirements.txt
    ├── tempCodeRunnerFile.py
    ├── test_email.txt
    └── .env.example



