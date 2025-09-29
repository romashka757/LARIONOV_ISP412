ISP-412 Alt

An alternative implementation inspired by `L1fan04/ISP-412` with a different visual style. Backend is built with FastAPI, frontend uses Jinja2 templates and custom CSS.

Getting Started

1. Create and activate a virtual environment.
2. Install dependencies:

```
pip install -r requirements.txt
```

3. Run the server:

```
uvicorn app.main:app --reload
```

4. Open `http://127.0.0.1:8000` in your browser.

Project Structure

```
isp412-alt/
  app/
    __init__.py
    main.py
    templates/
      index.html
    static/
      css/
        style.css
  requirements.txt
  test_api.py
  README.md
```

Notes

- This project keeps similar API functionality but changes the visual design.
- Run tests with:

```
pytest -q
```


