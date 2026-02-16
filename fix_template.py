
import os

path = r'e:\github\blood_Group\New folder\blood_deatction\templates\view_report.html'
try:
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    skip_next = False
    
    for i in range(len(lines)):
        if skip_next:
            skip_next = False
            continue
            
        line = lines[i]
        
        # Check for the split pattern
        if 'class="phone-value">{{' in line and (i+1 < len(lines)) and 'analysis.patient.phone' in lines[i+1]:
            print(f"Found split tag at line {i+1}")
            # Construct the fixed line
            # Preserve indentation
            indent = line[:line.find('<div')]
            fixed_line = indent + '<div class="info-value">{{ analysis.patient.email }} <br> <span class="phone-value">{{ analysis.patient.phone }}</span></div>\n'
            new_lines.append(fixed_line)
            skip_next = True # Skip the next line which contained the rest of the tag
        else:
            new_lines.append(line)

    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("File successfully patched.")

except Exception as e:
    print(f"Error: {e}")
