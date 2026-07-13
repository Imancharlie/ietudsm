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
    
    # Civil Engineering - Student must select specific department
    'BSc. in Civil Engineering': 'Civil Engineering Department (Select Specific Department)',
   
    # Chemical Engineering Department
    'BSc. in Chemical Engineering': 'Chemical Engineering Department',
    
    # Transportation and Geotechnical Engineering Department
    'BSc. in Geomatic Engineering': 'Transportation and Geotechnical Engineering Department',

    # Metallurgy and Mineral Processing Department
    'BSc. in Metallurgy and Mineral Processing Engineering': 'Metallurgy and Mineral Processing Department',
    
    # Geology and Mining Department
    'BSc. in Mining Engineering': 'Geology and Mining Department',
    'BSc. in Petroleum Engineering': 'Geology and Mining Department',

    # Department Computer Science and Engineering 
    'BSc. in Information Technology and Computer Engineering': 'CoICT',
    #Department Electronics and Telecommunications Engineering
    'BSc. in Electronics Engineering': 'CoICT',
    'BSc. in Telecommunication Engineering': 'CoICT',
    #Department Agricultural Engineering
    'BSc. in Agricultural Engineering': 'CoICT',

}

# Civil Engineering specific departments
CIVIL_ENGINEERING_DEPARTMENTS = [
    'Transportation and Geotechnical Engineering Department',
    'Structural and Construction Engineering Department',
    'Water Resources Engineering Department',
]

# College mapping for programmes
COURSE_COLLEGE_MAPPING = {
    # CoET - College of Engineering and Technology
    'BSc. in Mechanical Engineering': 'CoET',
    'BSc. in Industrial Engineering': 'CoET',
    'BSc. in Textile Design': 'CoET',
    'BSc. in Textile Engineering': 'CoET',
    'BSc. in Electrical Engineering': 'CoET',
    'BSc. in Civil Engineering': 'CoET',
    'BSc. in Chemical Engineering': 'CoET',
    'BSc. in Geomatic Engineering': 'CoET',
    'Bachelor of Architecture': 'CoET',
    'BSc. in Quantity Surveying': 'CoET',

    # SoMG - School of Mines and Geosciences
    'BSc. in Metallurgy and Mineral Processing Engineering': 'SoMG',
    'BSc. in Mining Engineering': 'SoMG',
    'BSc. in Petroleum Engineering': 'SoMG',

    # CoAF - College of Agriculture and Food Sciences
    'BSc. in Agricultural Engineering': 'CoAF',

    # CoICT - College of Information and Communication Technologies
    'BSc. in Information Technology and Computer Engineering': 'CoICT',
    'BSc. in Electronics Engineering and BSc. in Telecommunication Engineering': 'CoICT',
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

def get_college_from_course(course_name):
    """Get college name from course name"""
    return COURSE_COLLEGE_MAPPING.get(course_name, 'General')

def get_all_courses():
    """Get list of all available courses"""
    return sorted(COURSE_DEPARTMENT_MAPPING.keys())

