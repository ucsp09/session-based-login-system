from fastapi import APIRouter, Response, Request, status, Depends
from schema.common_schema import ErrorResponseSchema
from schema.login_schema import LoginRequestSchema, LoginResponseSchema, LogoutResponseSchema
from utils import user_utils, uuid_utils, session_utils
from dao.user_dao import UserDao
from core.bootstrap import get_session_store, get_user_dao
from core.adapters.session_store.base_session_store import BaseSessionStore
from core.logger import Logger
from config.constants import SESSION_EXPIRY_SECONDS
login_api_router = APIRouter()
logger = Logger.get_logger(__name__)

@login_api_router.post("/login")
async def login(input_data: LoginRequestSchema, request: Request, response: Response,
                session_store: BaseSessionStore = Depends(get_session_store),
                user_dao: UserDao = Depends(get_user_dao)):
    try:
        logger.info("Login request received.")
        logger.debug(f"Login input data: {input_data}")

        # Check for existing session
        session_id = request.cookies.get("session_id")
        if session_id:
            logger.info(f"Checking existing session_id in cookies: {session_id}")
            existing_session = await session_store.get_session(session_id)
            if existing_session:
                logger.info(f"Session found for session_id: {session_id}, validating expiry.")
                session_expires_at = existing_session.get('expires_at')
                if not session_expires_at:
                    logger.warning(f"Session data malformed for session_id: {session_id}, deleting session.")
                    await session_store.delete_session(session_id)
                elif session_utils.is_session_valid(session_expires_at):
                    logger.info(f"Existing session is valid for session_id: {session_id}.")
                    response.status_code = status.HTTP_200_OK
                    return LoginResponseSchema(message="There is already another active session. Pls logout and then attempt login", session_id=session_id)
                else:
                    logger.info(f"Existing session has expired for session_id: {session_id}, deleting session.")
                    await session_store.delete_session(session_id)    
            else:
                logger.debug(f"No session found in store for session_id: {session_id}")

        # Validate username and password format
        logger.info(f"Validating login input for username: {input_data.username}")
        if not user_utils.is_valid_username(input_data.username):
            logger.error(f"Invalid username format: {input_data.username}")
            response.status_code = status.HTTP_400_BAD_REQUEST
            return ErrorResponseSchema(error="Invalid username format.")
        if not user_utils.is_valid_password(input_data.password):
            logger.error("Invalid password format.")
            response.status_code = status.HTTP_400_BAD_REQUEST
            return ErrorResponseSchema(error="Invalid password format.")

        # Fetch user data
        logger.info(f"Fetching user data for username: {input_data.username}")
        user_data, err = await user_dao.get_user_by_username(input_data.username)
        if err:
            logger.error(f"Error occurred while fetching user data for username: {input_data.username}. Error: {err}")
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return ErrorResponseSchema(error="Failed to retrieve user.")
        if not user_data:
            logger.warning(f"User not found for username: {input_data.username}")
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return ErrorResponseSchema(error="Invalid username or password.")

        # Verify password
        logger.info(f"Verifying password for username: {input_data.username}")
        if not user_utils.verify_password(input_data.password, user_data["password"]):
            logger.warning(f"Invalid password for username: {input_data.username}")
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return ErrorResponseSchema(error="Invalid username or password.")

        # Create new session
        session_id = uuid_utils.generate_uuid()
        session_expires_at = session_utils.get_session_expiration_timestamp(SESSION_EXPIRY_SECONDS)
        logger.info(f"Creating new session for username: {input_data.username}, session_id: {session_id}")
        await session_store.create_session(
            session_id, {"username": user_data["username"], "role": user_data["role"], "expires_at": session_expires_at}
        )
        logger.debug(f"Session created successfully for session_id: {session_id}")

        # Set session cookie
        logger.info(f"Setting session cookie for username: {input_data.username}, session_id: {session_id}")
        response.status_code = status.HTTP_200_OK
        response.set_cookie(key="session_id", value=session_id, httponly=True, max_age=SESSION_EXPIRY_SECONDS)
        logger.info(f"Login successful for username: {input_data.username}, session_id: {session_id}")
        return LoginResponseSchema(message="Login successful.", session_id=session_id)

    except Exception as e:
        logger.exception(f"Unexpected error during login: {str(e)}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorResponseSchema(error="An unexpected error occurred during login.")

@login_api_router.get("/login/status")
async def login_status(request: Request, response: Response, session_store: BaseSessionStore = Depends(get_session_store)):
    try:
        logger.info("Login status request received.")

        # Check for session_id in cookies
        session_id = request.cookies.get("session_id")
        if not session_id:
            logger.warning("No session_id found in cookies.")
            response.status_code = status.HTTP_200_OK
            return LoginResponseSchema(message="Not logged in.", session_id="")

        logger.info(f"Checking session for session_id: {session_id}")
        existing_session = await session_store.get_session(session_id)
        if not existing_session:
            logger.warning(f"No active session found for session_id: {session_id}")
            response.status_code = status.HTTP_200_OK
            return LoginResponseSchema(message="Not logged in.", session_id="")

        # Validate session expiry
        session_expires_at = existing_session.get('expires_at')
        if not session_expires_at or not session_utils.is_session_valid(session_expires_at):
            logger.info(f"Session has expired for session_id: {session_id}, deleting session.")
            await session_store.delete_session(session_id)
            response.status_code = status.HTTP_200_OK
            return LoginResponseSchema(message="Not logged in.", session_id="")

        logger.info(f"Active session found for session_id: {session_id}")
        response.status_code = status.HTTP_200_OK
        return LoginResponseSchema(message="Logged in.", session_id=session_id)
    except Exception as e:
        logger.exception(f"Unexpected error during login status check: {str(e)}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorResponseSchema(error="An unexpected error occurred while checking login status.")


@login_api_router.get("/logout")
async def logout(request: Request, response: Response, session_store: BaseSessionStore = Depends(get_session_store)):
    try:
        logger.info("Logout request received.")

        # Check for session_id in cookies
        session_id = request.cookies.get("session_id")
        if not session_id:
            logger.warning("No session_id found in cookies.")
            response.status_code = status.HTTP_400_BAD_REQUEST
            return ErrorResponseSchema(error="No active session found.")

        logger.info(f"Checking session for session_id: {session_id}")
        existing_session = await session_store.get_session(session_id)
        if not existing_session:
            logger.warning(f"No active session found for session_id: {session_id}")
            response.status_code = status.HTTP_400_BAD_REQUEST
            return ErrorResponseSchema(error="No active session found.")

        # Delete the session
        logger.info(f"Deleting session for session_id: {session_id}")
        await session_store.delete_session(session_id)
        logger.debug(f"Session deleted successfully for session_id: {session_id}")

        # Clear session cookie
        logger.info("Clearing session cookie.")
        response.status_code = status.HTTP_200_OK
        response.delete_cookie(key="session_id")
        logger.info(f"Logout successful for session_id: {session_id}")
        return LogoutResponseSchema(message="Logout successful.")

    except Exception as e:
        logger.exception(f"Unexpected error during logout: {str(e)}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorResponseSchema(error="An unexpected error occurred during logout.")