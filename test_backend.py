from backend.backend import find_programs

result = find_programs(21, "Punjab", "undergraduate", "Yes", 40000)
print(result["program_count"])