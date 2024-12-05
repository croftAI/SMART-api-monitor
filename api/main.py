from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import monitoring_routes, analysis_routes
from .middleware.rate_limiter import RateLimiterMiddleware

app = FastAPI(
    title="Smart API Monitor",
    description="Intelligent API Monitoring System",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiting middleware
app.add_middleware(RateLimiterMiddleware)

# Include routers
app.include_router(monitoring_routes.router)
app.include_router(analysis_routes.router)

@app.get("/health")
async def health_check():
    """API health check endpoint."""
    return {"status": "healthy"}