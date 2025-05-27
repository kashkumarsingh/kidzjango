"""
Utility functions to simplify view logic.
Handles common patterns like error handling, logging, and responses.
"""

import logging
import traceback
from django.http import HttpResponseServerError, HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404

logger = logging.getLogger('core')

def handle_view_error(message, exception, redirect_url=None):
    """
    Logs an error and returns an appropriate HTTP response.

    Args:
        message (str): The error message to log.
        exception (Exception): The exception that occurred.
        redirect_url (str, optional): URL to redirect to if specified.

    Returns:
        HttpResponse: Either a server error response or a redirect.
    """
    logger.error(f"{message}: {str(exception)}\n{traceback.format_exc()}")
    if redirect_url:
        return redirect(redirect_url)
    return HttpResponseServerError(f"{message}. Please contact the administrator.")

def require_post_method(request, redirect_url):
    """
    Ensures the request method is POST, otherwise redirects.

    Args:
        request: The HTTP request object.
        redirect_url (str): URL to redirect to if not POST.

    Returns:
        HttpResponse: Redirect if not POST, None if POST.
    """
    if request.method != 'POST':
        return redirect(redirect_url)
    return None

def fetch_object_or_error(model, error_message, redirect_url, **kwargs):
    """
    Fetches an object using get_object_or_404, logs and handles errors.

    Args:
        model: The Django model to query.
        error_message (str): The error message to log if the object is not found.
        redirect_url (str): URL to redirect to if the object is not found.
        **kwargs: Query parameters for get_object_or_404.

    Returns:
        Object: The fetched object, or raises an error response.
    """
    try:
        return get_object_or_404(model, **kwargs)
    except model.DoesNotExist:
        logger.error(error_message)
        return redirect(redirect_url)