from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.core.signing import Signer
from django.views.decorators.cache import cache_page
from WishCraft_api.utils import get_upload_folder

import os
import json

# Create your views here.

with open("wishcraft-templates-data/templates.json", "r") as file:
    templates_data = json.load(file)["templates"]

with open("wishcraft-templates-data/templates_pictures.json", "r") as file:
    templates_pictures = json.load(file)["templates_pictures"]

with open("wishcraft-templates-data/songs.json", "r", encoding="utf-8") as file:
    songs = json.load(file)["songs"]


# ========== Home Page ==========

@cache_page(60 * 60 * 24)
def home_page(request):
    return render(request, "home_page.html", {"templates": templates_data})

# ========== View Template Pages ==========

@cache_page(60 * 60 * 24)
def view_template_page(request, template_id):
    if not template_id:
        return HttpResponse("Template ID is required!")

    if template_id not in [1, 2, 3, 4]:
        return HttpResponse("Template not found!")

    template_pics = templates_pictures.get(str(template_id), [])

    return render(request, "view_template_page.html", {"template_pictures": template_pics, "template_id": template_id})

# ========== Create Template Pages ==========

@cache_page(60 * 60 * 24)
def create_template_page(request, template_id):
    if not template_id:
        return HttpResponse("Template ID is required!")

    if template_id in [1, 2, 3]:
        return render(request, "create_template_page.html", {"template_id": template_id, "songs": list(songs.items())})

    elif template_id in [4]:
        return render(request, "create_template_form_page_2.html", {"template_id": template_id, "songs": list(songs.items())})

    return HttpResponse("This is create template page!")

# ========== Show User Template Page ==========

def show_template(request, token):
    """View to display the generated template"""
    try:
        signer = Signer()
        code = signer.unsign(token)

        upload_folder = get_upload_folder()
        html_file_path = os.path.join(upload_folder, code, "Template.html")

        if os.path.exists(html_file_path):
            return FileResponse(open(html_file_path, 'rb'), content_type='text/html')
        else:
            return HttpResponse("Template not found", status=404)
    except Exception as e:
        return HttpResponse("Invalid token", status=400)


# ========== Show Template Url page ==========

def show_template_url(request, token):
    """Redirect to template URL"""
    try:
        signer = Signer()
        code = signer.unsign(token)

        upload_folder = get_upload_folder()
        html_file_path = os.path.join(upload_folder, code, "Template.html")

        if os.path.exists(html_file_path):
            return render(request, "show_template_url_page.html", {"template_url": request.build_absolute_uri(f"/s/{token}/"), "code": code})
        else:
            return render(request, "show_template_url_page.html", {"message": "Template not found"}, status=404)
    except Exception as e:
        return render(request, "show_template_url_page.html", {"message": "Invalid token"}, status=400)

# ========== My Templates Page ==========

def my_templates_page(request):
    user_templates = request.session.get("user-templates", {})
    templates_list = list(user_templates.items())
    return render(request, "my_templates_page.html", {"templates": templates_list})

# ========== About Page ==========

@cache_page(60 * 60 * 24)
def about_page(request):
    return render(request, "about_page.html")


# ========== Contact Page ==========

@cache_page(60 * 60 * 24)
def contact_page(request):
    return render(request, "contact_page.html")


# ========== Privacy Page ==========

@cache_page(60 * 60 * 24)
def privacy_page(request):
    return render(request, "privacy_policy.html")

# ========== Install Page ==========

@cache_page(60 * 60 * 24)
def install_page(request):
    return render(request, "install_page.html")

# ========== Blog Page ============

@cache_page(60 * 60 * 24)
def blog_page(request):
    return render(request, "blog_page.html")

# ======= Dev / preview helpers =======
def page_not_found(request, exception=None):
    """Global 404 handler for Django.

    Django calls this when a 404 is raised and DEBUG=False. Keep the
    signature as (request, exception) to match Django's expectation.
    """
    return render(request, "404.html", status=404)

