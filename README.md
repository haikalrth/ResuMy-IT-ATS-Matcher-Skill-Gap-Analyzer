# ResuMy

ResuMy is a web application that helps users evaluate a resume against a target
job description. It shows a match score, detected skills, missing skills,
resume improvement suggestions, a learning roadmap for a target role, and a
simple CV builder.

The project is split into three services:

- `front-end`: React + Vite application
- `back-end`: Node.js + Express API
- `ai-service`: FastAPI service for model inference and roadmap generation

## Main Features

- Upload a resume in PDF or DOCX format
- Analyze resume compatibility with a job description
- Extract skills from the resume and job description
- Show missing skills and improvement suggestions
- Generate a learning roadmap for IT or technology roles
- Build a simple CV and download it as PDF

## Tech Stack

- Frontend: React, Vite, React Router, React Icons
- Backend: Node.js, Express, Multer, Mammoth, PDF Parse
- AI service: FastAPI, TensorFlow/Keras, scikit-learn, OpenRouter

## Project Structure

```text
.
|-- ai-service/
|   |-- main.py
|   |-- roadmap_generator.py
|   |-- requirements.txt
|   `-- models/
|-- back-end/
|   |-- app.js
|   |-- server.js
|   |-- controllers/
|   |-- routes/
|   |-- middlewares/
|   `-- services/
`-- front-end/
    |-- src/
    |-- package.json
    `-- vite.config.js
```

## Requirements

Make sure the following tools are installed:

- Node.js 20 or newer
- npm
- Python 3.12 or Python 3.13

The AI model files must be available in `ai-service/models`:

```text
resumy_micro_mlp.keras
resumy_ner_skill_artifacts.json
resumy_ner_skill_model.keras
scaler.pkl
tfidf_vectorizer.pkl
```

## Running Locally

Run the three services in separate terminals in this order.

### 1. AI Service

```powershell
cd ai-service
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Check the service:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

### 2. Backend

```powershell
cd back-end
npm ci
npm start
```

For development with auto reload:

```powershell
npm run dev
```

Check the service:

```powershell
Invoke-RestMethod http://127.0.0.1:5000/api/health
```

### 3. Frontend

```powershell
cd front-end
npm ci
npm run dev
```

Open the URL shown by Vite, usually:

```text
http://localhost:5173
```

## Environment Variables

The default local configuration works without a `.env` file. If you need to
point the services to different URLs, use the variables below.

### Frontend

Create `front-end/.env` if the frontend needs to call a custom backend URL:

```env
VITE_API_BASE_URL=http://127.0.0.1:5000
```

### Backend

```env
PORT=5000
AI_SERVICE_URL=http://127.0.0.1:8000
AI_SERVICE_TIMEOUT_MS=120000
FRONTEND_ORIGIN=http://localhost:5173
ANALYSIS_RECORD_KEY=change-this-admin-key
```

The backend `npm start` script loads `back-end/.env` with Node's
`--env-file-if-exists` flag. Environment variables from the server process still
take priority over values in `.env`.

### AI Service

```env
OPENROUTER_API_KEY=your-api-key
OPENROUTER_MODEL=your-model
AI_SERVICE_ALLOWED_ORIGINS=http://127.0.0.1:5000
```

`OPENROUTER_API_KEY` is required for the roadmap generator feature.

## Local Ports

| Service | Local URL | Health Check |
| --- | --- | --- |
| AI service | `http://127.0.0.1:8000` | `GET /health` |
| Backend | `http://127.0.0.1:5000` | `GET /api/health` |
| Frontend | `http://localhost:5173` | - |

## Main API Endpoints

Endpoints used by the frontend:

- `GET /api/health`: check backend status
- `POST /api/analyze`: upload a resume and job description, analyze it, and
  save the analysis result
- `GET /api/analyze`: retrieve saved analysis records with the `x-admin-key`
  header
- `GET /api/analyze/:id`: retrieve one saved analysis result with the
  `x-admin-key` header
- `POST /api/generate-roadmap`: generate a learning roadmap for a target role

The backend forwards AI-related requests to `ai-service`. Analysis records are
stored in `back-end/data/analysis-records.json` at runtime. Uploaded resume files
are not stored. Record endpoints are disabled unless `ANALYSIS_RECORD_KEY` is
configured on the backend.

## AI Notes

- The match score is not an official score from a commercial ATS product.
- The score is estimated from a model and similarity features between the
  resume and job description.
- Skill extraction uses a NER model and a curated skill list.
- The roadmap generator uses OpenRouter and returns an error if the AI service
  fails instead of returning dummy data.

## Deployment Notes

Recommended deployment setup:

- Frontend: Vercel
- Backend: VPS or Node.js hosting
- AI service: private service on the same server as the backend

For production, the AI service should not be exposed directly to the public.
Run it on the local host:

```bash
uvicorn main:app --host 127.0.0.1 --port 8000
```

The backend can be exposed publicly and call the AI service through:

```env
AI_SERVICE_URL=http://127.0.0.1:8000
```

Make sure the production backend sets `FRONTEND_ORIGIN` to the frontend domain.
See [DEPLOYMENT.md](./DEPLOYMENT.md) for more deployment details.

## Troubleshooting

### Frontend cannot access the backend

Make sure the backend is running at `http://127.0.0.1:5000`. If you use another
URL, set `VITE_API_BASE_URL` in `front-end/.env`, then restart the frontend.

### Backend cannot analyze a resume

Make sure the AI service is running and reachable from the backend:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

### Roadmap generator fails

Make sure `OPENROUTER_API_KEY` is set in the AI service environment. If the API
key is missing, invalid, or rate-limited, the roadmap endpoint will return an
error message.

### AI service installation fails

Make sure the Python version is 3.12 or 3.13:

```powershell
python --version
```

The TensorFlow and Keras versions used by this project are not compatible with
all Python versions, so use a supported version.

## Verification

Useful commands for checking the project:

```powershell
cd front-end
npm run lint
npm run build
```

```powershell
cd ai-service
python -m py_compile main.py roadmap_generator.py
```

## Resources
* [Google Drive Folder AI Models](https://drive.google.com/drive/folders/1xkyOCLrvv_dqnrv9VvYmY1AgDAFSunon?usp=drive_link) - *Folder AI Models di Gdrive
