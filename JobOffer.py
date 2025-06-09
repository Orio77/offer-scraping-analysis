from typing import Optional

class JobOffer:
    def __init__(self, title: Optional[str], company: Optional[str], location: Optional[str],
                 salary: Optional[str], url: Optional[str], site_id: str, add_info: Optional[str] = None):
        self.title = title
        self.company = company
        self.location = location
        self.salary = salary
        self.url = url
        self.site_id = site_id
        self.add_info = add_info

    def __str__(self):
        return (f"Site: {self.site_id}\n"
                f"Title: {self.title}\n"
                f"Company: {self.company}\n"
                f"Location: {self.location}\n"
                f"Salary: {self.salary}\n"
                f"URL: {self.url}\n"
                f"Additional Info: {self.add_info if self.add_info else 'N/A'}\n" + "-"*20)
