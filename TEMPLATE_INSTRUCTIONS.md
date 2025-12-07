# Application Template Setup Instructions

To enable the form export functionality, you need to create a Word template file.

## Template Location

Place your template file at:
```
templates/exports/application_template.docx
```

## Template Format

Create a Word document (.docx) that matches your original application form layout. Use the following placeholders where you want data to be inserted:

### Available Placeholders

- `{{ first_name }}` - Applicant's first name
- `{{ middle_name }}` - Applicant's middle name (if provided)
- `{{ last_name }}` - Applicant's last name
- `{{ full_name }}` - Full name (First Middle Last)
- `{{ nationality }}` - Nationality
- `{{ date_of_birth }}` - Date of birth (format: DD/MM/YYYY)
- `{{ age }}` - Age
- `{{ address_line1 }}` - Address line 1
- `{{ address_line2 }}` - Address line 2 (if provided)
- `{{ city }}` - City
- `{{ state }}` - State/Province
- `{{ postal_code }}` - Postal/ZIP code
- `{{ country }}` - Country
- `{{ university }}` - University name
- `{{ department }}` - Department
- `{{ course }}` - Course/Program
- `{{ year_of_study }}` - Year of study
- `{{ email }}` - Email address
- `{{ application_date }}` - Application submission date (format: DD/MM/YYYY)

## Example Template Structure

```
IET MEMBERSHIP APPLICATION FORM

Personal Information:
Name: {{ full_name }}
Date of Birth: {{ date_of_birth }}
Age: {{ age }}
Nationality: {{ nationality }}

Address:
{{ address_line1 }}
{{ address_line2 }}
{{ city }}, {{ state }} {{ postal_code }}
{{ country }}

Academic Information:
University: {{ university }}
Department: {{ department }}
Course: {{ course }}
Year of Study: {{ year_of_study }}

Contact:
Email: {{ email }}

Application Date: {{ application_date }}
```

## Creating the Template

1. Open Microsoft Word or LibreOffice Writer
2. Design your form layout matching the original template
3. Insert placeholders using `{{ variable_name }}` syntax
4. Save as `.docx` format
5. Place the file in `templates/exports/application_template.docx`

## Testing

After creating the template:
1. Log in as staff
2. Go to an application detail page
3. Click "Export Form"
4. The system will generate a filled Word document with applicant data

## Notes

- The template must be in `.docx` format (not `.doc`)
- Placeholders are case-sensitive
- You can use any formatting, fonts, or layout in the template
- The system will preserve all formatting from your template




