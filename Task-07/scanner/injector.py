import requests
import copy
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse

def inject_payload_in_url(session, url, parameter, payload, headers=None, cookies=None):
    """
    Injects a payload into a specific query parameter in a GET URL and sends the request.
    """
    try:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        
        # Replace the target parameter value with the payload
        # Note: parse_qs returns list values, we replace it with a single string payload
        query_params[parameter] = [payload]
        
        # Reconstruct the URL query string
        new_query = urlencode(query_params, doseq=True)
        new_url_parts = list(parsed_url)
        new_url_parts[4] = new_query
        target_url = urlunparse(new_url_parts)
        
        response = session.get(
            target_url,
            headers=headers,
            cookies=cookies,
            timeout=10,
            allow_redirects=False  # Do not follow redirects so we can analyze the immediate response (especially for XSS or SQLi)
        )
        return target_url, response
    except Exception as e:
        return url, None

def inject_payload_in_form(session, form, parameter_name, payload, headers=None, cookies=None):
    """
    Injects a payload into a specific form input and submits the form.
    """
    url = form['url']
    method = form['method'].upper()
    inputs = form['inputs']
    
    # Prepare the payload form data
    data = {}
    for inp in inputs:
        name = inp['name']
        val = inp['value']
        
        # If it is the target parameter, use the payload. Otherwise, use default/test value.
        if name == parameter_name:
            data[name] = payload
        else:
            # Provide sensible defaults for empty fields to pass basic form validations
            if not val:
                if inp['type'] == 'email':
                    data[name] = 'test@example.com'
                elif inp['type'] == 'number':
                    data[name] = '1'
                elif inp['type'] == 'password':
                    data[name] = 'password123'
                else:
                    data[name] = 'test'
            else:
                data[name] = val
                
    try:
        if method == 'POST':
            response = session.post(
                url,
                data=data,
                headers=headers,
                cookies=cookies,
                timeout=10,
                allow_redirects=False
            )
        else:  # GET method form
            response = session.get(
                url,
                params=data,
                headers=headers,
                cookies=cookies,
                timeout=10,
                allow_redirects=False
            )
        return url, response
    except Exception as e:
        return url, None
