from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.database.session import engine, Base
from app.routers import admin, lecturers, courses, students, auth

app = FastAPI(
    title="LMS API",
    description="A simple and modern learning management system backend built with FastAPI and PostgreSQL",
    version="1.0.0"
)

# Allow CORS for the frontend or other clients
origins = [
    "http://localhost:3000",  # frontend
    "https://your-frontend-domain.com" # production domain address
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Database setup: Create all tables
Base.metadata.create_all(bind=engine)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>LMS</title>
    </head>
    <body>
        <div class="bg-gray-200 p-4 rounded-lg shadow-lg">
            <h2>Modern Learning Management System [LMS backend]!</h2>
            <ul>
                <li><a href="/docs">/docs</a></li>
                <li><a href="/redoc">/redoc</a></li>
            </ul>
           <p>Built and deployed by Lemajr <a href="https://github.com/ericktek" target="_blank">GitHub</a>
                    Powered by <a href="https://fastapi.tiangolo.com" target="_blank">FastAPI</a> and <a href="https://vercel.com" target="_blank">Vercel</a></p>
        </div>
    </body>
</html>

"""

@app.get("/", response_class=HTMLResponse, tags=["Health"])
async def root():
    return html


# Include the respective routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(admin.router, prefix="/api/v1", tags=["Admin"])
app.include_router(lecturers.router, prefix="/api/v1", tags=["Lecturers"])
app.include_router(students.router, prefix="/api/v1", tags=["Students"])
app.include_router(courses.router, prefix="/api/v1", tags=["Course"])