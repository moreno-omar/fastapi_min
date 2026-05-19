# imports
from fastapi import Depends, FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.db import User, create_db_and_tables
from app.schemas import UserCreate, UserRead, UserUpdate
from app.users import auth_backend, current_active_user, fastapi_users
from app.payments import router as payments_router, webhook_router

# Setup static files and templates
BASE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")


app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
app.include_router(payments_router)
app.include_router(webhook_router)

# ==================== Web Routes ====================

@app.get("/")
async def landing(request: Request):
    """Landing page"""
    return templates.TemplateResponse(name="index.html", context={"request": request}, request=request)


@app.get("/service")
async def service(request: Request):
    """Service page - PDF to Word converter"""
    return templates.TemplateResponse(name="service.html", context={"request": request}, request=request)


@app.get("/contact")
async def contact(request: Request):
    """Contact page"""
    return templates.TemplateResponse(name="contact.html", context={"request": request}, request=request)


@app.post("/contact")
async def submit_contact(request: Request):
    """Handle contact form submission"""
    try:
        # Get form data
        form_data = await request.form()
        name = form_data.get("name", "").strip()
        email = form_data.get("email", "").strip()
        subject = form_data.get("subject", "").strip()
        message = form_data.get("message", "").strip()
        
        # Validation
        if not all([name, email, subject, message]):
            return templates.TemplateResponse(
                name="contact.html",
                context={
                    "request": request,
                    "error": "All fields are required",
                },
                status_code=400,
                request=request
            )
        
        # TODO: Save to database or send email
        # For now, just log the submission
        print(f"Contact Form Submission: {name} ({email}) - {subject}")
        print(f"Message: {message}")
        
        # Render success message
        return templates.TemplateResponse(
            name="contact.html",
            context={
                "request": request,
                "success_message": "Thank you for your message! We'll get back to you soon.",
            },
            request=request
        )
    
    except Exception as e:
        print(f"Error processing contact form: {e}")
        return templates.TemplateResponse(
            name="contact.html",
            context={
                "request": request,
                "error": "An error occurred. Please try again.",
            },
            status_code=500,
            request=request
        )