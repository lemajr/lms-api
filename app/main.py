from fastapi import FastAPI
from fastapi.responses import HTMLResponse


app = FastAPI(
    title="LMS API",
    description="A simple and modern learning management system backend built with FastAPI and PostgreSQL",
    version="1.0.0"
)


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


