import json

class VUTJsonParser:
    def __init__(self, json_path = "plugins/VUT/data/parsed_data.json"):
        """
        Needs json path to json file, self.data will contain parsed data as list of dicts
        """
        self.json_path = json_path
        self.data = None
    
    def set_new_json_path(self, json_path):
        self.json_path = json_path
    
    def read_json(self):
        with open(self.json_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def get_data(self) -> list:
        return self.data
    
    def search(self, term: str, field: str) -> list:
        """Search for a term in a field
        
        Example:

        >>> parser = VUTJsonParser()
        >>> parser.read_json()
        >>> parser.search("matematika", "subject")
        
        returns a list of dicts that contain "matematika" in the "subject" field
        """
        term = term.lower()
        # Make sure the field exists in data items
        if not self.data or not self.data[0].get(field):
            return []  # or raise error if you want
        return [item for item in self.data if term in str(item.get(field, "")).lower()]


    def get_exam_names(self):
        
        # Dictionary to store the count of each subject
        counter = {}
        # Final list of unique names with their prefixes
        names = []

        for exam in self.data:
            # Get subject 
            subject = exam["subject"]
            # Get the cuurent count for the subject, default to 0, then add 1
            count = counter.get(subject, 0) +1
            # Update the counter
            counter[subject] = count
            names.append(f"{count}) {subject}")
        
        return names