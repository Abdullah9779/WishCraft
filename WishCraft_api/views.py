import os
import json

from django.template.loader import render_to_string
from django.urls import reverse

from django.conf import settings
from django.core.signing import Signer
from django.core.mail import send_mail

from .models import UsersTemplates

from rest_framework.decorators import renderer_classes, api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from .utils import generate_unique_code, validate_image, secure_filename, get_upload_folder


# Create your views here.

# ========== Create Template API ==========

@renderer_classes([JSONRenderer])
@api_view(["POST"])
def create_template_api(request):
    data = request.data

    if not data:
        return Response({"message": "No data provided"}, status=400)

    template_id = data.get("template_id")
    if template_id in [1, 2, 3]:
        required_fields = ['name', 'date', 'wish', 'song', 'images', "template_id"]
    elif template_id in [4]:
        required_fields = ['wish', 'signature', 'name', "template_id"]
    else:
        return Response({"message": "Invalid Template ID!"}, status=400)

    for field in required_fields:
        if field not in data:
            return Response({"message": f"{field} is required"}, status=400)

    if not request.session.session_key:
        request.session.create()  # create a new session if none exists
    request.session.cycle_key()   # rotate session ID without losing data

    # Generate unique code
    code = generate_unique_code()
    name = str(data.get("name"))
    wish = str(data.get("message", data.get("wish", "")))

    # Create user folder
    upload_folder = get_upload_folder()
    user_folder = os.path.join(upload_folder, code)
    os.makedirs(user_folder, exist_ok=True)

    images = []
    if "images" in data:
        if len(data["images"]) > 15:
            return Response({"message": "Too many images. Maximum 15 allowed."}, status=400)

        for idx, img in enumerate(data["images"]):
            img_data = None

            if isinstance(img, dict):
                img_data = img.get("data")
            elif isinstance(img, str):
                img_data = img
            else:
                continue

            # Validate image
            is_valid, result = validate_image(img_data)
            if not is_valid:
                return Response({"message": f"Image {idx + 1}: {result}"}, status=400)

            # Generate secure filename
            image_name = secure_filename(f"img_{code}_{idx}.png")
            image_path = os.path.join(user_folder, image_name)

            # Ensure path is within upload directory
            if not os.path.abspath(image_path).startswith(os.path.abspath(upload_folder)):
                return Response({"message": "Invalid file path"}, status=400)

            # Save validated image
            with open(image_path, "wb") as image_file:
                image_file.write(result)

            image_url = f"{settings.MEDIA_URL}uploads/{code}/{image_name}"
            images.append(image_url)

    # Set default image for template 4
    first_image = images[0] if images else ""
    if template_id == 4 and not first_image:
        first_image = "https://dotcoder.site/static/wishcraft/templates/template-4-pictures/template-4-0.png"

    template_data = {
        "name": name,
        "date": str(data.get("date", "")),
        "wish": wish,
        "signature": str(data.get("signature", "")),
        "font": str(data.get("font", "Arial")),
        "song_url": str(data.get("song", "")),
        "first_image": first_image,
        "images_urls": json.dumps(images[1:] if len(images) > 1 else []),
        "template_id": template_id
    }

    if template_id in [1, 2, 3, 4]:
        html_code = render_to_string(f"wishcraft_templates/template{template_id}.html", {"data": template_data})
    else:
        return Response({"message": "Unsupported template_id"}, status=400)

    # Save HTML file
    html_file_name = "Template.html"
    html_file_path = os.path.join(user_folder, html_file_name)

    with open(html_file_path, "w", encoding="utf-8") as html_file:
        html_file.write(html_code)

    # Create signed token
    signer = Signer()
    token = signer.sign(code)

    # Save template data to the database
    user_template = UsersTemplates.objects.create(
        session_id=request.session.session_key,
        token=token,
        template_code=code,
        template_id=template_id,
        data=template_data
    )

    user_template.save()

    template_db_id = user_template.id

    # Store in session
    if "user-templates" not in request.session:
        request.session["user-templates"] = {}

    request.session["user-templates"][code] = {
        "template_code": code,
        "template_db_id": template_db_id,
        "template_url": request.build_absolute_uri(reverse("show_template", kwargs={"token": token})),
        "template_data": template_data
    }
    request.session.modified = True

    return Response({
        "message": "Template created successfully!",
        "templateUrl": reverse("show_template_url", kwargs={"token": token})
    }, status=200)

# ========== Delete Template API ==========

@renderer_classes([JSONRenderer])
@api_view(["POST"])
def delete_template_api(request):
    data = request.data

    if not data:
        return Response({"message": "No data provided"}, status=400)

    template_code = data.get("template_code")
    if not template_code:
        return Response({"message": "Template code is required"}, status=400)

    user_templates = request.session.get("user-templates", {})
    if template_code not in user_templates:
        return Response({"message": "Template not found in session"}, status=404)

    # Delete template files
    upload_folder = get_upload_folder()
    user_folder = os.path.join(upload_folder, template_code)

    if os.path.exists(user_folder):
        for root, dirs, files in os.walk(user_folder, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(user_folder)


    # Delete from database
    try:
        template_db_id = request.session["user-templates"][template_code].get("template_db_id")
        user_template = UsersTemplates.objects.get(id=template_db_id)
        user_template.delete()
    except UsersTemplates.DoesNotExist:
        pass

    # Remove from session
    del request.session["user-templates"][template_code]
    request.session.modified = True

    return Response({"message": "Template deleted successfully!"}, status=200)

# ========== Contact API ==========

@renderer_classes([JSONRenderer])
@api_view(["POST"])
def contact_api(request):
    data = request.data

    if not data:
        return Response({"message": "No data provided"}, status=400)

    required_fields = ['name', 'email', 'subject', 'message']
    for field in required_fields:
        if field not in data:
            return Response({"message": f"{field} is required"}, status=400)

    send_mail(
        subject="WishCraft Contact Form Submission",
        message=f"""
WishCraft Contact Form Submission Details:

Full Name: {data.get('name')}
Email: {data.get('email')}
Subject: {data.get('subject')}
Message: {data.get('message')}
        """,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.MAIL_SEND_TO],
    )

    return Response({"message": "Thank you for contacting us! We will get back to you shortly."}, status=200)
