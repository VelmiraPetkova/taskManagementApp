from enum import Enum

class TaskStatus(Enum):
    notStarted = "Not Started"
    inProgress = "In Progress"
    completed = "Completed"
    onHold = "Hold"
    blocked = "Blocked"
    readyForReview  = "Ready for Review"
    rejected  = "Rejected"
    accepted = "Accepted"


class UserRole(Enum):
    employee = "Employee"
    superUser = "SuperUser"