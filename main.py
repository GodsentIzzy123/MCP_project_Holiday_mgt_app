from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Optional

# Create MCP server
mcp = FastMCP("High School Holiday Application Manager")

# In-memory "database" of students
students_db: List[Dict] = [
    {
        "name": "Alice Johnson",
        "school_id": "S001",
        "dob": "2007-03-14",
        "grade": "10",
        "holidays_left": 10,
        "holidays_taken": []
    },
    {
        "name": "Bob Smith",
        "school_id": "S002",
        "dob": "2006-09-22",
        "grade": "11",
        "holidays_left": 10,
        "holidays_taken": []
    },
    {
        "name": "Cathy Lin",
        "school_id": "S003",
        "dob": "2008-01-05",
        "grade": "9",
        "holidays_left": 10,
        "holidays_taken": []
    },
    {
        "name": "David Okoro",
        "school_id": "S004",
        "dob": "2005-12-18",
        "grade": "12",
        "holidays_left": 10,
        "holidays_taken": []
    },
    {
        "name": "Ella Thompson",
        "school_id": "S005",
        "dob": "2007-06-30",
        "grade": "10",
        "holidays_left": 7,
        "holidays_taken": ["12-20-2024", "01-01-2025", "01-03-2025"]
    },
]

# Helper function
def find_student(school_id: str) -> Optional[Dict]:
    for student in students_db:
        if student["school_id"] == school_id:
            return student
    return None

# Tool to request leave for specific dates
@mcp.tool()
def request_leave(school_id: str, dates: List[str]) -> str:
    """
    Request leave for a student by providing a list of date strings in MM-DD-YYYY format.
    """
    student = find_student(school_id)
    if not student:
        return "Student not found"

    new_dates = [d for d in dates if d not in student["holidays_taken"]]

    if not new_dates:
        return "All requested dates have already been taken."

    if student["holidays_left"] < len(new_dates):
        return f"Leave denied. Only {student['holidays_left']} day(s) left."

    student["holidays_taken"].extend(new_dates)
    student["holidays_left"] -= len(new_dates)

    return f"Leave approved for {len(new_dates)} day(s). Holidays left: {student['holidays_left']}."

# Tool to check student leave status
@mcp.tool()
def check_leave_status(school_id: str) -> Dict:
    """
    Retrieve a student's leave status and info.
    """
    student = find_student(school_id)
    if not student:
        return {"error": "Student not found"}
    
    return {
        "name": student["name"],
        "school_id": student["school_id"],
        "grade": student["grade"],
        "holidays_left": student["holidays_left"],
        "holidays_taken": student["holidays_taken"]
    }
    
# Tool to cancel previously booked holidays
@mcp.tool()
def cancel_leave(school_id: str, dates: List[str]) -> str:
    """
    Cancel previously booked leave dates for a student.
    Dates should be in MM-DD-YYYY format.
    """
    student = find_student(school_id)
    if not student:
        return "Student not found"

    cancelable_dates = [d for d in dates if d in student["holidays_taken"]]
    
    if not cancelable_dates:
        return "None of the requested dates are in the student's holiday list."

    for date in cancelable_dates:
        student["holidays_taken"].remove(date)
    
    student["holidays_left"] += len(cancelable_dates)

    return (
        f"Successfully cancelled {len(cancelable_dates)} holiday date(s). "
        f"Holidays left: {student['holidays_left']}."
    )
 

# Example greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}! Welcome to the Leave Management System."

if __name__ == "__main__":
    mcp.run()