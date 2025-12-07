"""
Course to Department mapping for University of Dar es Salaam - College of Engineering and Technology (CoET)
"""

COURSE_DEPARTMENT_MAPPING = {
    # Mechanical and Industrial Engineering Department
    'BSc. in Mechanical Engineering': 'Mechanical and Industrial Engineering Department',
    'BSc. in Industrial Engineering': 'Mechanical and Industrial Engineering Department',
    'BSc. in Textile Design': 'Mechanical and Industrial Engineering Department',
    'BSc. in Textile Engineering': 'Mechanical and Industrial Engineering Department',
    
    # Electrical Engineering Department
    'BSc. in Electrical Engineering': 'Electrical Engineering Department',
    
    # Civil Engineering Department
    'BSc. in Civil Engineering': 'Civil Engineering Department',
    
    # Chemical Engineering Department
    'BSc. in Chemical Engineering': 'Chemical Engineering Department',
    
    # Transportation and Geotechnical Engineering Department
    'BSc. in Geomatic Engineering': 'Transportation and Geotechnical Engineering Department',
    
    # Structural and Construction Engineering Department
    'Bachelor of Architecture': 'Departments of Structural and Construction Engineering',
    'BSc. in Quantity Surveying': 'Departments of Structural and Construction Engineering',
    
    # Metallurgy and Mineral Processing Department
    'BSc. in Metallurgy and Mineral Processing Engineering': 'Metallurgy and Mineral Processing Department',
    
    # Geology and Mining Department
    'BSc. in Mining Engineering': 'Geology and Mining Department',
    'BSc. in Petroleum Engineering': 'Geology and Mining Department',
}

YEAR_OF_STUDY_CHOICES = [
    ('1', 'Year 1'),
    ('2', 'Year 2'),
    ('3', 'Year 3'),
    ('4', 'Year 4'),
]

def get_department_from_course(course_name):
    """Get department name from course name"""
    return COURSE_DEPARTMENT_MAPPING.get(course_name, 'General Engineering')

def get_all_courses():
    """Get list of all available courses"""
    return sorted(COURSE_DEPARTMENT_MAPPING.keys())

