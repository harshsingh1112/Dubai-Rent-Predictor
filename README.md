# Dubai Rent Predictor 🏙️

A premium AI-powered real estate valuation engine for Dubai, built with Next.js and Python.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
npm install
```

### 2. Run Locally
You need to run both the frontend and the mock API server.

**Terminal 1 (Frontend):**
```bash
npm run dev
```
Open [http://localhost:3000](http://localhost:3000).

**Terminal 2 (API):**
```bash
# Setup Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r api/requirements.txt

# Run server
python start_api.py
```

### 3. Deployment
This project is optimized for **Vercel**.
1. Push to GitHub.
2. Import in Vercel.
3. Vercel automatically deploys the Next.js app and the Python API function.

## 🛠️ Tech Stack
- **Frontend**: Next.js 14, Tailwind CSS, Recharts, Framer Motion aesthetics.
- **Backend**: Python Serverless Function (Flask/BaseHTTP).
- **ML Engine**: Scikit-learn Random Forest (trained on synthetic data).
- **Data**: `data_science/` contains the generation and training scripts.
