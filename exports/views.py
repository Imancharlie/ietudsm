from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from applications.models import Application
from docxtpl import DocxTemplate
import os
import uuid
import time
import win32com.client
import pythoncom
from django.conf import settings


@user_passes_test(lambda u: u.is_staff)
def export_application_form(request, pk):
    """Export application form as PDF using Word COM automation"""
    application = get_object_or_404(Application, pk=pk)
    
    # Path to template
    template_path = os.path.join(settings.BASE_DIR, 'templates', 'exports', 'application_template.docx')
    
    # If template doesn't exist
    if not os.path.exists(template_path):
        return HttpResponse("Template file not found. Please create application_template.docx in templates/exports/")
    
    # Create temporary file names with absolute paths
    temp_docx = os.path.abspath(os.path.join(settings.BASE_DIR, f"temp_{uuid.uuid4()}.docx"))
    temp_pdf = os.path.abspath(os.path.join(settings.BASE_DIR, f"temp_{uuid.uuid4()}.pdf"))
    
    word = None
    doc = None
    
    try:
        # Initialize COM for this thread
        pythoncom.CoInitialize()
        
        # Load and render template
        template = DocxTemplate(template_path)
        
        # Prepare context data
        context = {
            'first_name': application.first_name,
            'middle_name': application.middle_name or '',
            'last_name': application.last_name,
            'full_name': application.full_name,
            'nationality': application.nationality,
            'date_of_birth': application.date_of_birth.strftime('%d/%m/%Y'),
            'age': application.age,
            'email': application.email,
            'phone_number': application.phone_number,
            'address': application.address,
            'city': application.city,
            'university': application.university,
            'department': application.department,
            'course': application.course,
            'year_of_study': f"{application.year_of_study} year",
            'date_of_admission': application.admission_date_formatted,
            'year_of_graduation': application.year_of_graduation,
            'application_date': application.created_at.strftime('%d/%m/%Y'),
            'status': application.get_status_display(),
            'reference_number': application.payment.reference_number if hasattr(application, 'payment') else 'N/A',
        }
        
        # Render and save DOCX
        template.render(context)
        template.save(temp_docx)
        
        # Small delay to ensure file is fully written
        time.sleep(0.3)
        
        # Convert to PDF using Word COM automation
        word = win32com.client.DispatchEx("Word.Application")
        word.Visible = False
        word.DisplayAlerts = 0  # Disable alerts (wdAlertsNone)
        
        # Open the document
        doc = word.Documents.Open(temp_docx)
        
        # Export as PDF using ExportAsFixedFormat (more reliable than SaveAs)
        # Format 17 = wdExportFormatPDF
        # Quality 0 = wdExportOptimizeForPrint
        doc.ExportAsFixedFormat(temp_pdf, 17, False, 0)
        
        # Close document
        doc.Close(False)  # False = don't save changes
        doc = None
        
        # Quit Word
        word.Quit()
        word = None
        
        # Small delay to ensure file is written
        time.sleep(0.5)
        
        # Read PDF file
        with open(temp_pdf, 'rb') as f:
            pdf_data = f.read()
        
        # Create response
        response = HttpResponse(pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="IET_Application_{application.full_name.replace(" ", "_")}.pdf"'
        
        return response
        
    except Exception as e:
        # Make sure Word is closed on error
        try:
            if doc:
                doc.Close(False)
        except:
            pass
        try:
            if word:
                word.Quit()
        except:
            pass
        
        import traceback
        error_details = traceback.format_exc()
        return HttpResponse(f"Error generating PDF: {str(e)}\n\nDetails:\n{error_details}", status=500)
        
    finally:
        # Uninitialize COM
        try:
            pythoncom.CoUninitialize()
        except:
            pass
        
        # Wait before cleanup
        time.sleep(0.5)
        
        # Clean up temporary files with retry logic
        for attempt in range(3):
            try:
                if os.path.exists(temp_docx):
                    os.remove(temp_docx)
                if os.path.exists(temp_pdf):
                    os.remove(temp_pdf)
                break
            except (PermissionError, OSError):
                if attempt < 2:
                    time.sleep(1)
                pass




