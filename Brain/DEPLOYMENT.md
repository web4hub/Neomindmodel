# Deployment Guide — Brain

## 🧩 Local Development

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```
🐳 Docker Setup
```bash
docker build -t web4-brain .
docker run -p 8000:8000 web4-brain
```
⚙️ CI/CD
	•	GitHub Actions workflow in .github/workflows/deploy.yml
	•	Automatically builds and deploys to Render, AWS, or other hosts

🔒 Production Setup
	•	Use Gunicorn + Uvicorn for high performance
	•	Set environment variables in .env
	•	Enable HTTPS with Nginx reverse proxy

---

