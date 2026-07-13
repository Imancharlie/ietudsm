"""
exports/views.py

Handles generation and export of IET membership application forms
(single and bulk) as DOCX/PDF/ZIP files.

DOCX generation uses docxtpl. PDF conversion uses LibreOffice headless
mode via subprocess, making this module fully compatible with Linux
environments (PythonAnywhere, Ubuntu VPS, etc.) with no dependency on
Windows-only libraries such as win32com or pythoncom.
"""

import io
import os

import uuid
import zipfile
from datetime import datetime

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from docxtpl import DocxTemplate


from applications.models import Application, ApplicationStatus

from payments.models import Payment


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Directory used for temporary DOCX/PDF files during export.
# Kept inside BASE_DIR/tmp_exports so it's easy to purge and doesn't
# clutter the project root.
EXPORT_TMP_DIR = os.path.join(settings.BASE_DIR, "tmp_exports")

# Path to the LibreOffice binary. On most Linux servers (including
# PythonAnywhere and Ubuntu) "soffice" is the correct executable name;
# override via Django settings if your environment differs.
LIBREOFFICE_BIN = getattr(settings, "LIBREOFFICE_BIN", "soffice")


def _ensure_tmp_dir():
    """Ensure the temporary export directory exists."""
    os.makedirs(EXPORT_TMP_DIR, exist_ok=True)


def _safe_remove(*paths):
    """Remove files if they exist, silently ignoring errors."""
    for path in paths:
        try:
            if path and os.path.exists(path):
                os.remove(path)
        except OSError:
            pass


def _convert_docx_to_pdf(docx_path, outdir):
    """
    Convert a DOCX file to PDF using LibreOffice headless mode.

    Returns the path to the generated PDF file.
    Raises RuntimeError with a descriptive message if conversion fails.
    """
    try: 
        result = subprocess.run(
            [
                LIBREOFFICE_BIN,
                "--headless",
                "--convert-to",
                "pdf",
                docx_path,
                "--outdir",
                outdir,
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )
    except FileNotFoundError:
        raise RuntimeError(
            f"LibreOffice executable '{LIBREOFFICE_BIN}' was not found on this "
            "server. Please install LibreOffice or configure LIBREOFFICE_BIN "
            "in Django settings."
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError("LibreOffice PDF conversion timed out.")

    if result.returncode != 0:
        raise RuntimeError(
            "LibreOffice PDF conversion failed "
            f"(exit code {result.returncode}): {result.stderr.strip() or result.stdout.strip()}"
        )

    expected_pdf = os.path.join(
        outdir, os.path.splitext(os.path.basename(docx_path))[0] + ".pdf"
    )

    if not os.path.exists(expected_pdf):
        raise RuntimeError(
            "LibreOffice reported success but the expected PDF file was not "
            f"found at {expected_pdf}."
        )

    return expected_pdf


def _build_application_context(application):
    """Build the docxtpl context dict for a single application."""
    return {
        "first_name": application.first_name,
        "middle_name": application.middle_name or "",
        "last_name": application.last_name,
        "full_name": application.full_name,
        "nationality": application.nationality,
        "date_of_birth": application.date_of_birth.strftime("%d/%m/%Y"),
        "age": application.age,
        "email": application.email,
        "phone_number": application.phone_number,
        "address": application.address,
        "city": application.city,
        "university": application.university,
        "department": application.department,
        "course": application.course,
        "year_of_study": f"{application.year_of_study} year",
        "date_of_admission": application.admission_date_formatted,
        "year_of_graduation": application.year_of_graduation,
        "application_date": application.created_at.strftime("%d/%m/%Y"),
        "status": application.get_status_display(),
        "reference_number": (
            application.payment.reference_number
            if hasattr(application, "payment")
            else "N/A"
        ),
    }


# ---------------------------------------------------------------------------
# Single application export
# ---------------------------------------------------------------------------
@user_passes_test(lambda u: u.is_staff)
def export_application_form(request, pk):
    """
    Export application form as DOCX using a docxtpl template.
    No PDF conversion required.
    """

    application = get_object_or_404(Application, pk=pk)

    # Path to DOCX template
    template_path = os.path.join(
        settings.BASE_DIR,
        "templates",
        "exports",
        "application_template.docx"
    )

    # Check template exists
    if not os.path.exists(template_path):
        return HttpResponse(
            "Template file not found. Please create application_template.docx "
            "inside templates/exports/",
            status=500
        )

    # Create temporary directory
    export_dir = os.path.join(settings.BASE_DIR, "tmp_exports")
    os.makedirs(export_dir, exist_ok=True)

    file_id = uuid.uuid4()

    temp_docx = os.path.join(
        export_dir,
        f"application_{file_id}.docx"
    )

    try:
        # Load template
        template = DocxTemplate(template_path)

        # Prepare data
        context = {
            "first_name": application.first_name,
            "middle_name": application.middle_name or "",
            "last_name": application.last_name,

            "full_name": application.full_name,

            "nationality": application.nationality,

            "date_of_birth": (
                application.date_of_birth.strftime("%d/%m/%Y")
                if application.date_of_birth
                else ""
            ),

            "age": application.age,

            "email": application.email,

            "phone_number": application.phone_number,

            "address": application.address,

            "city": application.city,

            "university": application.university,

            "department": application.department,

            "course": application.course,

            "year_of_study": (
                f"{application.year_of_study} year"
                if application.year_of_study
                else ""
            ),

            "date_of_admission": application.admission_date_formatted,

            "year_of_graduation": application.year_of_graduation,

            "application_date": (
                application.created_at.strftime("%d/%m/%Y")
            ),

            "status": application.get_status_display(),

            "reference_number": (
                application.payment.reference_number
                if hasattr(application, "payment")
                else "N/A"
            ),
        }

        # Fill template placeholders
        template.render(context)

        # Save completed document
        template.save(temp_docx)


        # Read generated DOCX
        with open(temp_docx, "rb") as file:
            docx_data = file.read()


        # Return DOCX response
        response = HttpResponse(
            docx_data,
            content_type=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            )
        )

        filename = (
            f"IET_Application_{application.full_name.replace(' ', '_')}.docx"
        )

        response["Content-Disposition"] = (
            f'attachment; filename="{filename}"'
        )

        return response


    except Exception as e:
        import traceback

        error_details = traceback.format_exc()

        return HttpResponse(
            f"""
            Error generating document:
            
            {str(e)}
            
            Details:
            {error_details}
            """,
            status=500
        )


    finally:
        # Delete temporary generated file
        try:
            if os.path.exists(temp_docx):
                os.remove(temp_docx)
        except Exception:
            pass

# ---------------------------------------------------------------------------
# Bulk export views
# ---------------------------------------------------------------------------

@user_passes_test(lambda u: u.is_staff)

def bulk_export_form(request):
    """Display form for bulk application form export with filters."""
    departments = (
        Application.objects.values_list("department", flat=True)
        .distinct()
        .order_by("department")
    )
    years_of_study = (
        Application.objects.values_list("year_of_study", flat=True)
        .distinct()
        .order_by("year_of_study")
    )

    context = {
        "departments": departments,
        "years_of_study": years_of_study,
        "status_choices": ApplicationStatus.choices,
    }
    return render(request, "exports/bulk_export_form.html", context)


@user_passes_test(lambda u: u.is_staff)

def bulk_export_zip(request):
    """Export application forms as a ZIP file with individual PDFs."""
    applications = get_filtered_applications(request)

    if not applications:
        return HttpResponse("No applications match the selected filters.", status=400)

    unconfirmed = [
        app
        for app in applications
        if not hasattr(app, "payment") or not app.payment.is_confirmed
    ]
    if unconfirmed:
        return HttpResponse(
            f"Cannot export application forms. {len(unconfirmed)} application(s) "
            "do not have confirmed payments.",
            status=400,
        )

    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for app in applications:
            # Placeholder content until per-application PDF generation is
            # wired into the bulk ZIP flow.
            filename = f"{app.full_name.replace(' ', '_')}_Application.txt"
            content = (
                f"IET Membership Application Form\n\n"
                f"Name: {app.full_name}\n"
                f"Department: {app.department}\n"
                f"Course: {app.course}\n"
                f"Status: {app.get_status_display()}"
            )
            zip_file.writestr(filename, content)

    zip_buffer.seek(0)

    # log_activity(
    #     user=request.user,
    #     action_type="bulk_export_applications",
    #     description=f"Bulk exported {len(applications)} application forms as ZIP",
    #     object_type="Application",
    #     ip_address=getattr(request, "audit_ip", None),
    #     user_agent=getattr(request, "audit_user_agent", None),
    #     additional_data={
    #         "format": "ZIP",
    #         "count": len(applications),
    #         "filters": dict(request.GET),
    #     },)

    response = HttpResponse(zip_buffer.getvalue(), content_type="application/zip")
    response["Content-Disposition"] = (
        f'attachment; filename="IET_Application_Forms_'
        f'{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip"'
    )
    return response


@user_passes_test(lambda u: u.is_staff)

def bulk_export_pdf(request):
    """Export application forms as a combined PDF with a cover page."""
    applications = get_filtered_applications(request)

    if not applications:
        return HttpResponse("No applications match the selected filters.", status=400)

    unconfirmed = [
        app
        for app in applications
        if not hasattr(app, "payment") or not app.payment.is_confirmed
    ]
    if unconfirmed:
        return HttpResponse(
            f"Cannot export application forms. {len(unconfirmed)} application(s) "
            "do not have confirmed payments.",
            status=400,
        )

    cover_content = generate_cover_page(request, applications, "PDF")

    # Placeholder text content until true combined-PDF rendering
    # (e.g. via LibreOffice merge or reportlab) is implemented.
    content = f"{cover_content}\n\n" + "\n\n".join(
        [
            f"Application Form for {app.full_name}\n"
            f"Department: {app.department}\n"
            f"Course: {app.course}\n"
            f"Status: {app.get_status_display()}"
            for app in applications
        ]
    )

    # log_activity(
    #     user=request.user,
    #     action_type="bulk_export_applications",
    #     description=(
    #         f"Bulk exported {len(applications)} application forms as combined PDF"
    #     ),
    #     object_type="Application",
    #     ip_address=getattr(request, "audit_ip", None),
    #     user_agent=getattr(request, "audit_user_agent", None),
    #     additional_data={
    #         "format": "PDF",
    #         "count": len(applications),
    #         "filters": dict(request.GET),
    #     },
    #)

    response = HttpResponse(content, content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="IET_Application_Forms_Combined_'
        f'{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf"'
    )
    return response


@user_passes_test(lambda u: u.is_staff)

def bulk_export_word(request):
    """Export application forms as a combined Word document with a cover page."""
    applications = get_filtered_applications(request)

    if not applications:
        return HttpResponse("No applications match the selected filters.", status=400)

    unconfirmed = [
        app
        for app in applications
        if not hasattr(app, "payment") or not app.payment.is_confirmed
    ]
    if unconfirmed:
        return HttpResponse(
            f"Cannot export application forms. {len(unconfirmed)} application(s) "
            "do not have confirmed payments.",
            status=400,
        )

    cover_content = generate_cover_page(request, applications, "Word")

    # Placeholder text content until true combined-DOCX rendering
    # (e.g. via python-docx) is implemented.
    content = f"{cover_content}\n\n" + "\n\n".join(
        [
            f"Application Form for {app.full_name}\n"
            f"Department: {app.department}\n"
            f"Course: {app.course}\n"
            f"Status: {app.get_status_display()}"
            for app in applications
        ]
    )

    # log_activity(
    #     user=request.user,
    #     action_type="bulk_export_applications",
    #     description=(
    #         f"Bulk exported {len(applications)} application forms as combined "
    #         "Word document"
    #     ),
    #     object_type="Application",
    #     ip_address=getattr(request, "audit_ip", None),
    #     user_agent=getattr(request, "audit_user_agent", None),
    #     additional_data={
    #         "format": "Word",
    #         "count": len(applications),
    #         "filters": dict(request.GET),
    #     },
	#)

    response = HttpResponse(
        content,
        content_type=(
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ),
    )
    response["Content-Disposition"] = (
        f'attachment; filename="IET_Application_Forms_Combined_'
        f'{datetime.now().strftime("%Y%m%d_%H%M%S")}.docx"'
    )
    return response


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def get_filtered_applications(request):
    """Get applications based on filter parameters in the request."""
    queryset = Application.objects.all()

    department = request.GET.get("department")
    year_of_study = request.GET.get("year_of_study")
    status = request.GET.get("status")
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")
    payment_status = request.GET.get("payment_status")

    if department:
        queryset = queryset.filter(department=department)
    if year_of_study:
        queryset = queryset.filter(year_of_study=year_of_study)
    if status:
        queryset = queryset.filter(status=status)
    if date_from:
        queryset = queryset.filter(created_at__gte=date_from)
    if date_to:
        queryset = queryset.filter(created_at__lte=date_to)
    if payment_status:
        if payment_status == "confirmed":
            queryset = queryset.filter(payment__is_confirmed=True)
        elif payment_status == "pending":
            queryset = queryset.filter(
                payment__is_confirmed=False, payment__is_rejected=False
            )
        elif payment_status == "rejected":
            queryset = queryset.filter(payment__is_rejected=True)

    return queryset.select_related("payment", "user")


def generate_cover_page(request, applications, format_type):
    """Generate cover page content for bulk exports."""
    filters = {
        "Department": request.GET.get("department", "All"),
        "Year of Study": request.GET.get("year_of_study", "All"),
        "Status": request.GET.get("status", "All"),
        "Payment Status": request.GET.get("payment_status", "All"),
        "Date From": request.GET.get("date_from", "All"),
        "Date To": request.GET.get("date_to", "All"),
    }

    filter_summary = [
        f"{key}: {value}" for key, value in filters.items() if value and value != "All"
    ]

    name_list = "\n".join(
        [f"{i + 1}. {app.full_name}" for i, app in enumerate(applications)]
    )

    cover_content = f"""
IET Membership Application Forms Export
{'=' * 50}

Export Summary:
{'-' * 30}
Export Format: {format_type}
Total Application Forms: {len(applications)}
Exported by: {request.user.get_full_name() or request.user.email}
Date: {datetime.now().strftime('%d %b %Y')}

Applied Filters:
{'-' * 30}
{chr(10).join(filter_summary) if filter_summary else 'No filters applied'}

Application List:
{'-' * 30}
{name_list}
"""

    return cover_content