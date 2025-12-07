# CoET Courses and Departments Mapping

## University of Dar es Salaam - College of Engineering and Technology (CoET)

### Official Department Structure

---

## 📚 Course to Department Mapping

### 1. Mechanical and Industrial Engineering Department

**Courses Offered:**
- BSc Mechanical Engineering
- BSc Industrial Engineering
- BSc Textile Design
- BSc Textile Engineering

**Total Programs:** 4

---

### 2. Electrical Engineering Department

**Courses Offered:**
- BSc Electrical Engineering

**Total Programs:** 1

---

### 3. Civil Engineering Department

**Courses Offered:**
- BSc Civil Engineering

**Total Programs:** 1

---

### 4. Chemical Engineering Department

**Courses Offered:**
- BSc Chemical Engineering

**Total Programs:** 1

---

### 5. Transportation and Geotechnical Engineering Department

**Courses Offered:**
- BSc Geomatic Engineering

**Total Programs:** 1

---

### 6. Departments of Structural and Construction Engineering

**Courses Offered:**
- Bachelor of Architecture *(Note: Not BSc)*
- BSc Quantity Surveying

**Total Programs:** 2

---

### 7. Metallurgy and Mineral Processing Department

**Courses Offered:**
- BSc Metallurgy and Mineral Processing Engineering

**Total Programs:** 1

---

### 8. Geology and Mining Department

**Courses Offered:**
- BSc Mining Engineering
- BSc Petroleum Engineering

**Total Programs:** 2

---

## 📊 Summary Statistics

### Total Departments: 8
### Total Programs: 13

### Degree Types:
- **BSc (Bachelor of Science):** 12 programs
- **Bachelor of Architecture:** 1 program

---

## 🎓 Degree Naming Convention

### Standard Format:
```
BSc [Field] Engineering
```

### Examples:
- BSc Mechanical Engineering
- BSc Civil Engineering
- BSc Electrical Engineering

### Special Cases:
1. **Architecture:** Bachelor of Architecture (not BSc)
2. **Textile Design:** BSc Textile Design (not "Engineering")
3. **Quantity Surveying:** BSc Quantity Surveying (not "Engineering")

---

## 📋 Complete Course List (Alphabetical)

1. Bachelor of Architecture
2. BSc Chemical Engineering
3. BSc Civil Engineering
4. BSc Electrical Engineering
5. BSc Geomatic Engineering
6. BSc Industrial Engineering
7. BSc Mechanical Engineering
8. BSc Metallurgy and Mineral Processing Engineering
9. BSc Mining Engineering
10. BSc Petroleum Engineering
11. BSc Quantity Surveying
12. BSc Textile Design
13. BSc Textile Engineering

---

## 🏢 Department Details

### Mechanical and Industrial Engineering Department
**Focus Areas:**
- Mechanical systems and design
- Industrial processes and management
- Textile technology and design
- Manufacturing engineering

**Programs:** 4
- Mechanical Engineering
- Industrial Engineering
- Textile Design
- Textile Engineering

---

### Electrical Engineering Department
**Focus Areas:**
- Power systems
- Electronics
- Control systems
- Electrical machines

**Programs:** 1
- Electrical Engineering

---

### Civil Engineering Department
**Focus Areas:**
- Structural engineering
- Water resources
- Environmental engineering
- Construction management

**Programs:** 1
- Civil Engineering

---

### Chemical Engineering Department
**Focus Areas:**
- Process engineering
- Chemical processes
- Industrial chemistry
- Biochemical engineering

**Programs:** 1
- Chemical Engineering

---

### Transportation and Geotechnical Engineering Department
**Focus Areas:**
- Surveying and mapping
- Geographic information systems
- Land management
- Remote sensing

**Programs:** 1
- Geomatic Engineering

---

### Departments of Structural and Construction Engineering
**Focus Areas:**
- Building design and architecture
- Construction management
- Cost estimation
- Project management

**Programs:** 2
- Architecture
- Quantity Surveying

---

### Metallurgy and Mineral Processing Department
**Focus Areas:**
- Metal extraction and processing
- Mineral beneficiation
- Materials science
- Pyrometallurgy and hydrometallurgy

**Programs:** 1
- Metallurgy and Mineral Processing Engineering

---

### Geology and Mining Department
**Focus Areas:**
- Mining operations
- Petroleum exploration and production
- Geological surveys
- Resource management

**Programs:** 2
- Mining Engineering
- Petroleum Engineering

---

## 🔄 How the System Works

### Application Form Flow:

1. **User Selects Course:**
   ```
   Dropdown: "BSc Mechanical Engineering"
   ```

2. **System Auto-Determines Department:**
   ```
   Department: "Mechanical and Industrial Engineering Department"
   ```

3. **Saved to Database:**
   ```python
   application.course = "BSc Mechanical Engineering"
   application.department = "Mechanical and Industrial Engineering Department"
   ```

### Example Mappings:

```python
# User selects course → System sets department

'BSc Mechanical Engineering' → 'Mechanical and Industrial Engineering Department'
'Bachelor of Architecture' → 'Departments of Structural and Construction Engineering'
'BSc Mining Engineering' → 'Geology and Mining Department'
```

---

## 📱 User Interface

### Application Form Display:

```
┌─────────────────────────────────────┐
│ Course: [Select your course ▼]     │
│                                     │
│ Options:                            │
│ - Bachelor of Architecture          │
│ - BSc Chemical Engineering          │
│ - BSc Civil Engineering             │
│ - BSc Electrical Engineering        │
│ - BSc Geomatic Engineering          │
│ - BSc Industrial Engineering        │
│ - BSc Mechanical Engineering        │
│ - BSc Metallurgy and Mineral...    │
│ - BSc Mining Engineering            │
│ - BSc Petroleum Engineering         │
│ - BSc Quantity Surveying            │
│ - BSc Textile Design                │
│ - BSc Textile Engineering           │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ ℹ️ Note: Your department will be   │
│ automatically determined based on   │
│ your selected course.               │
└─────────────────────────────────────┘
```

---

## 🎯 Validation Rules

### Course Selection:
- ✅ Required field
- ✅ Must select from dropdown
- ✅ Cannot enter custom value

### Department Assignment:
- ✅ Automatic (no user input)
- ✅ Based on course mapping
- ✅ Saved to database

---

## 📊 Department Distribution

```
Mechanical & Industrial: ████████ (4 programs - 31%)
Structural & Construction: ████ (2 programs - 15%)
Geology & Mining: ████ (2 programs - 15%)
Electrical: ██ (1 program - 8%)
Civil: ██ (1 program - 8%)
Chemical: ██ (1 program - 8%)
Transportation & Geotech: ██ (1 program - 8%)
Metallurgy & Mineral: ██ (1 program - 8%)
```

---

## 🔍 Special Notes

### 1. Architecture Degree
- **Different from others:** Bachelor of Architecture (not BSc)
- **Still in CoET:** Part of Structural and Construction Engineering
- **Professional degree:** Leads to professional architecture practice

### 2. Textile Programs
- **Two separate programs:**
  - BSc Textile Design (design focus)
  - BSc Textile Engineering (engineering focus)
- **Same department:** Both under Mechanical and Industrial Engineering

### 3. Mining-Related Programs
- **Split across two departments:**
  - Metallurgy → Metallurgy and Mineral Processing Department
  - Mining → Geology and Mining Department
  - Petroleum → Geology and Mining Department

---

## 🎓 Graduation Year Calculation

### Based on Year of Study:

| Year of Study | Expected Graduation |
|---------------|---------------------|
| First Year | Current Year + 4 |
| Second Year | Current Year + 3 |
| Third Year | Current Year + 2 |
| Fourth Year | Current Year + 1 |
| Fifth Year | Current Year |

**Note:** Most programs are 4 years, but some (like Architecture) may be 5 years.

---

## 📝 Database Structure

### Application Model Fields:

```python
course = "BSc Mechanical Engineering"
department = "Mechanical and Industrial Engineering Department"
year_of_study = "Second Year"
year_of_graduation = 2027  # Calculated
```

---

## ✅ Testing Checklist

### For Each Course:
- [ ] Appears in dropdown
- [ ] Correct department assigned
- [ ] Saves to database correctly
- [ ] Displays in profile
- [ ] Exports to PDF correctly

### Special Cases:
- [ ] Architecture shows "Bachelor of Architecture" (not BSc)
- [ ] All BSc programs show "BSc" prefix
- [ ] Department names are complete and correct

---

## 🔄 Future Updates

### To Add New Course:

1. Open `applications/course_mappings.py`
2. Add to `COURSE_DEPARTMENT_MAPPING`:
```python
'BSc New Engineering': 'Department Name',
```
3. Save and restart server
4. Course appears in dropdown automatically

### To Change Department Name:

1. Update mapping in `course_mappings.py`
2. Existing applications keep old name
3. New applications use new name

---

## 📞 Support

### Questions About Courses:
- Contact CoET administration
- Visit: www.coet.udsm.ac.tz

### Technical Issues:
- Check `applications/course_mappings.py`
- Verify department names match official CoET structure

---

**All 13 CoET programs are now correctly mapped!** ✅

### Quick Reference:
- 8 Departments
- 13 Programs
- 12 BSc degrees
- 1 Bachelor of Architecture






