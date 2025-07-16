#!/usr/bin/env python3
"""
Test the name extraction logic from email addresses
"""

import re

def extract_name_from_email(email):
    """Extract a proper name from an email address"""
    if not email or '@' not in email:
        return None
    
    email_name_part = email.split('@')[0]
    
    # Convert common formats to proper names
    if '.' in email_name_part:
        # Format: first.last@gmail.com -> First Last
        name_parts = email_name_part.split('.')
        name_parts = [part.capitalize() for part in name_parts if part]
        return ' '.join(name_parts)
    else:
        # First remove numbers
        name_parts = re.sub(r'[0-9]', '', email_name_part)
        
        # Try to split by common patterns
        # First, handle underscore separation
        if '_' in name_parts:
            name_parts = name_parts.replace('_', ' ')
        
        # Handle common Indian names that don't have separators (like ayushladdha)
        # This uses a heuristic to find potential word boundaries in names without separators
        if len(name_parts) > 6 and not ' ' in name_parts:
            # Try to find common prefixes/suffixes in Indian names
            common_parts = ['kumar', 'lal', 'singh', 'sharma', 'devi', 'das', 'gupta', 'raj', 'laddha']
            for part in common_parts:
                if part in name_parts.lower():
                    index = name_parts.lower().find(part)
                    if index > 0:  # Not at the beginning
                        name_parts = name_parts[:index] + ' ' + name_parts[index:]
            
            # If still no spaces and longer than 6 chars, try to insert space in the middle
            if len(name_parts) > 6 and not ' ' in name_parts:
                # Try to split after consonant followed by vowel (common pattern in names)
                name_parts = re.sub(r'([bcdfghjklmnpqrstvwxyz])([aeiou])', r'\1 \2', name_parts, flags=re.IGNORECASE, count=1)
        
        # Handle camelCase (johnDoe -> John Doe)
        name_parts = re.sub(r'([a-z])([A-Z])', r'\1 \2', name_parts)
        
        # Capitalize each part
        if name_parts:
            name_parts = ' '.join([part.capitalize() for part in name_parts.split()])
            return name_parts
        else:
            return email_name_part.capitalize()

# Test cases
test_emails = [
    "john.doe@gmail.com",          # Simple dot format
    "jane_smith@yahoo.com",        # Underscore format
    "ayushladdha123@gmail.com",    # Indian name with numbers
    "vikaskumar@gmail.com",        # Indian name with common suffix
    "ramsharma@hotmail.com",       # Indian name with common suffix
    "mikeBrown@hotmail.com",       # CamelCase format
    "sarah.jane.wilson@company.com", # Multiple dots
    "tech.support@example.com",    # Service account with dot
    "john1234@gmail.com",          # With numbers
    "johnDoe@gmail.com",           # Simple CamelCase
    "shreya779@gmail.com",         # Name with numbers
    "amitsingh@yahoo.com",         # Name with common suffix
    "priyaraj87@gmail.com"         # Name with common suffix and numbers
]

print("Email Name Extraction Test:")
print("-" * 50)
for email in test_emails:
    name = extract_name_from_email(email)
    print(f"{email} -> {name}")

if __name__ == "__main__":
    pass
