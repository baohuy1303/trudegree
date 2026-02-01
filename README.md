# 🎓 TruDegree

**Your AI Academic Advisor for Truman State University**

TruDegree is an intelligent academic planning assistant that helps Truman State University students plan their courses, stay on track for graduation, and explore academic paths tailored to their interests.
Video Demo: https://drive.google.com/file/d/1L0BMF_Niqk9fJZWkLi_wIiR5AXqBjSSu/view?usp=sharing 

![Screenshot1](https://github.com/baohuy1303/trudegree/blob/main/frontend/public/screenshots/TruDegree4.png?raw=true)
![Screenshot2](https://github.com/baohuy1303/trudegree/blob/main/frontend/public/screenshots/TruDegree5.png?raw=true)

## Features

- **Zero Guesswork**: Get specific course recommendations - no more placeholders or "missing requirements"
- **Personalized Planning**: AI-powered recommendations based on your degree audit and academic interests
- **Lightning Fast**: Get comprehensive academic plans in minutes, not hours
- **Interactive Chat**: Ask questions about your degree requirements, course options, and graduation timeline
- **Smart PDF Parsing**: Upload your DegreeWorks audit PDF and let the AI understand your academic progress
- **Two Modes**:
  - **Quick Q&A Mode** (~30 seconds): Fast answers to specific questions
  - **Long Planning Mode** (~2-3 minutes): Comprehensive 4-year academic planning

## Architecture

### Backend
- **Framework**: FastAPI (Python)
- **AI Engine**: LangChain / LangGraph + OpenAI
- **PDF Parsing**: Custom DegreeWorks parser
- **Agent System**: React-style AI agent with tool use capabilities

### Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **UI Library**: HeroUI + TailwindCSS
- **Routing**: React Router v6
- **HTTP Client**: Axios

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- OpenAI API Key (or compatible API endpoint)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API key:
```
BENCHMARK_KEY=your_openai_api_key_here
```

4. Run the FastAPI server:
```bash
python main.py
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file (optional, defaults to localhost:8000):
```
VITE_API_BASE_URL=http://localhost:8000
```

4. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Usage

1. **Export Your DegreeWorks Audit**
   - Log into your DegreeWorks account
   - Export your degree audit as a PDF (Letter Portrait format recommended)
   - Hide your name if you prefer to not expose that (DegreeWorks audit's only privacy issue is showing your name)

2. **Upload & Ask**
   - Upload your DegreeWorks PDF
   - Choose your mode (Quick Q&A or Long Planning)
   - Ask a question or request a comprehensive plan

3. **Chat & Plan**
   - Review AI recommendations
   - Ask follow-up questions
   - Explore different academic paths
   - Get specific course suggestions

## Example Prompts

- "Create a 4-year plan for me to graduate on time"
- "What courses should I take next semester?"
- "What are my remaining requirements for my major?"
- "Suggest electives that align with a career in data science"
- "Help me plan a study abroad semester"

## API Endpoints

### `POST /api/pdf`
Upload a DegreeWorks PDF and start a new session
- **Parameters**: 
  - `file`: PDF file
  - `prompt`: Initial question/request
  - `is_long_planning_mode`: Boolean for planning mode
- **Returns**: Session ID and initial AI response

### `POST /api/chat`
Continue an existing conversation
- **Parameters**:
  - `session_id`: Session identifier
  - `message`: User message
  - `is_long_planning_mode`: Boolean for planning mode
- **Returns**: AI response with course recommendations

## Project Structure

```
trudegree/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── requirements.txt        # Python dependencies
│   ├── scrape/                # Core scraping & AI logic
│   │   ├── ai.py              # AI agent implementation
│   │   ├── parseStudentDegree_DeepSeekop.py  # PDF parser
│   │   ├── samplePlan.py      # Course planning logic
│   │   ├── scrape.py          # Web scraping utilities
│   │   ├── data/              # Truman degree requirements data
│   │   │   ├── parsedTrumanReq.json
│   │   │   ├── truman_degree.json
│   │   │   └── truman_REQ.json
│   │   └── examples/          # Model documentation
│   ├── data/                  # Sample plans & test data
│   │   ├── sample-plans/      # Sample academic plans
│   │   └── test-pdfs/         # Test DegreeWorks PDFs
│   ├── examples/              # Example outputs (for testing)
│   │   ├── conversation-logs/ # AI conversation logs
│   │   └── parsed-degrees/    # Parsed PDF examples
│   ├── archive/               # Archived/legacy code
│   ├── tests/                 # Test files
│   └── pdfs/                  # Uploaded user PDFs (runtime)
└── frontend/
    ├── src/
    │   ├── pages/
    │   │   ├── index.tsx      # Landing page
    │   │   └── chat.tsx       # Chat interface
    │   ├── components/        # Reusable UI components
    │   ├── context/           # React context (chat state)
    │   └── layouts/           # Layout components
    ├── package.json           # Node dependencies
    └── vite.config.ts         # Vite configuration
```

## Roadmap & Future Enhancements

We're constantly working to make TruDegree even better! Here are some exciting features planned for future releases:

### RateMyProfessor Integration
Automatically scrape and integrate professor ratings to recommend not just *what* courses to take, but *who* to take them with. Get personalized recommendations based on:
- Professor ratings and reviews
- Teaching style matching your learning preferences
- Course difficulty and workload insights

### User Persistence with Redis
Implement Redis-based session management for:
- **Persistent chat history** across devices
- **Saved academic plans** that you can return to anytime
- **Faster session retrieval** and improved performance
- **Multi-device sync** - start planning on your laptop, continue on your phone

### Database for University Catalog (High Priority!)
Implementing a web crawler of the university's entire catalog:

- **10x Faster Queries**: Instant course lookups vs. current text parsing
- **More Accurate Recommendations**: Agent can query the catalog based on needs instead of having to reason and scrape sample plans, degreeworks, and gen-ed courses
- **Smarter Context**: AI agent can understand course descriptions, learning outcomes, and cross-listings
- **Better Planning**: Identify prerequisite chains, co-requisites, and optimal course sequences
- **Real-time Updates**: Sync with university catalog changes automatically

---

## ⚠️ Disclaimer

TruDegree is an AI-powered assistant and should be used as a supplementary planning tool. Always verify your academic plans with your official academic advisor and refer to the [official Truman State University catalog](http://catalog.truman.edu/) for authoritative degree requirements.

---

**Made with ❤️ for Truman State University students from Huy B. Huynh**

