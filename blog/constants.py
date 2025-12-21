from enum import Enum

class BlogStatus(str, Enum):
    DRAFT = "draft"
    PUBLISH = "publish"
    INACTIVE = "inactive"

# blog_status = (
#     ("draft", "Draft"),
#     ("publish", "Publish"),
#     ("inactive", "Inactive"),
# )