from ninja import NinjaAPI
from auth.api import router as auth_router
from courses.api import router as courses_router
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI(
    title="Kamba code API", 
    version="1.0.0", 
    description="API for Kamba code application",
)
api.register_controllers(NinjaJWTDefaultController)
api.add_router("/auth/", auth_router,tags=["Authentication"])
api.add_router("/courses/", courses_router)