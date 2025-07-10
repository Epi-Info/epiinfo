import epiinfo

# List all methods and attributes in epiinfo
print("=== EpiInfo Module Methods and Attributes ===")
try:
    epiinfo_attributes = dir(epiinfo)
    print(f"Total attributes found: {len(epiinfo_attributes)}")
    
    # Categorize attributes
    methods = []
    classes = []
    constants = []
    
    for attr in epiinfo_attributes:
        if not attr.startswith('_'):  # Skip private attributes
            obj = getattr(epiinfo, attr)
            if callable(obj):
                if isinstance(obj, type):
                    classes.append(attr)
                else:
                    methods.append(attr)
            else:
                constants.append(attr)
    
    print(f"\n--- Classes ({len(classes)}) ---")
    for cls in sorted(classes):
        print(f"  {cls}")
        
    print(f"\n--- Methods/Functions ({len(methods)}) ---")
    for method in sorted(methods):
        print(f"  {method}")
        
    print(f"\n--- Constants/Variables ({len(constants)}) ---")
    for const in sorted(constants):
        print(f"  {const}")
    
    # Show detailed info for classes
    print(f"\n--- Detailed Class Information ---")
    for cls_name in classes:
        cls_obj = getattr(epiinfo, cls_name)
        cls_methods = [m for m in dir(cls_obj) if not m.startswith('_')]
        print(f"{cls_name}: {len(cls_methods)} methods")
        for method in cls_methods[:5]:  # Show first 5 methods
            print(f"    - {method}")
        if len(cls_methods) > 5:
            print(f"    ... and {len(cls_methods) - 5} more")

except Exception as e:
    print(f"Error listing epiinfo methods: {e}")
    print("The epiinfo module may not be properly installed or imported.")


